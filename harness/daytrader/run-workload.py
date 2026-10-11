#!/usr/bin/env python3
"""Run the bounded local baseline; reset only the verification-owned fixture."""
import argparse
import csv
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--subject", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--java-home", type=Path, required=True)
parser.add_argument("--gradle-home", type=Path, required=True)
parser.add_argument("--warmup", type=int, default=100)
parser.add_argument("--measured", type=int, default=500)
parser.add_argument("--runtime", type=Path)
parser.add_argument("--server-java-home", type=Path)
parser.add_argument("--gradle-argument", action="append", default=[])
args = parser.parse_args()
subject, output = args.subject.resolve(), args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
env = dict(os.environ, JAVA_HOME=str(args.java_home), GRADLE_USER_HOME=str(args.gradle_home))
source = Path(__file__).resolve().parent
cache = args.gradle_home / "caches/modules-2/files-2.1"


def jar(group, name, version):
    files = list((cache / group / name / version).rglob(name + "-" + version + ".jar"))
    if len(files) != 1:
        raise RuntimeError("Expected one cached dependency: " + name)
    return files[0]


def execute(command, log, environment=env, timeout=180):
    with log.open("w") as stream:
        subprocess.run(command, cwd=subject, env=environment, stdout=stream,
                       stderr=subprocess.STDOUT, check=True, timeout=timeout)


jsoup, derby = jar("org.jsoup", "jsoup", "1.17.2"), jar("org.apache.derby", "derby", "10.10.1.1")
classes = output / "classes"
classes.mkdir()
execute([str(args.java_home / "bin/javac"), "-cp", str(jsoup), "-d", str(classes),
         str(source / "TradingWorkload.java"),
         str(subject / "daytrader3-verification/src/test/java/baseline/TradeClient.java")],
        output / "compile.log")
classpath = os.pathsep.join(map(str, [classes, jsoup, derby]))
server = (args.runtime or subject / "daytrader3-ee6/build/wlp") / "bin/server"
build = subject / "daytrader3-verification/build"
server_java = args.server_java_home or args.java_home
server_env = dict(env, JAVA_HOME=str(server_java), WLP_USER_DIR=str(build / "liberty-user"),
                  WLP_OUTPUT_DIR=str(build / "liberty-output"))
manifest = {"subject": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=subject, text=True).strip(),
            "subjectWorkingTree": subprocess.check_output(["git", "status", "--short"], cwd=subject, text=True),
            "earSha256": hashlib.sha256(
                (subject / "daytrader3-ee6/build/libs/daytrader3-ee6.ear").read_bytes()).hexdigest(),
            "platform": platform.platform(), "machine": platform.machine(), "cpuCount": os.cpu_count(),
            "javaHome": str(args.java_home), "heap": "-Xms256m -Xmx512m",
            "instrumentation": "No JaCoCo, debugger or application tracing",
            "serverJavaHome": str(server_java),
            "workload": {"mode": "Full EJB synchronous independent-account purchases", "warmupPerWorker": args.warmup,
                         "measuredPerWorker": args.measured, "thinkTimeMs": 20},
            "hashes": {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [source / "TradingWorkload.java", source / "run-workload.py", jsoup, derby]}}
(output / "environment.json").write_text(json.dumps(manifest, indent=2) + "\n")
execute([str(args.java_home / "bin/java"), "-version"], output / "java-version.txt")
summaries = []
for workers in [1, 4]:
    for repeat in range(1, 4):
        run = output / ("workers-" + str(workers) + "-run-" + str(repeat))
        run.mkdir()
        gradle_arguments = list(args.gradle_argument)
        if args.runtime:
            gradle_arguments.append("-PdaytraderLibertyHome=" + str(args.runtime.resolve()))
        execute(["./gradlew", "--offline", "--no-daemon", "--console=plain"] + gradle_arguments +
                [":daytrader3-verification:loadFixture"], run / "fixture.log")
        jvm = build / "liberty-user/servers/daytrader3_Baseline/jvm.options"
        gc_flags = ("-XX:+PrintGCDetails\n-XX:+PrintGCTimeStamps\n-Xloggc:" + str(run / "gc.log")
                    if server_java == args.java_home else "-Xlog:gc*:file=" + str(
            run / "gc.log") + ":time,uptime,level,tags")
        jvm.write_text("-Xms256m\n-Xmx512m\n" + gc_flags + "\n")
        stop_sampling = threading.Event()
        sampler = None
        try:
            started = time.monotonic()
            execute([str(server), "start", "daytrader3_Baseline"], run / "start.log", server_env)
            pid = int(re.search(r"process ID (\d+)", (run / "start.log").read_text()).group(1))
            deadline = started + 90
            while True:
                try:
                    with urllib.request.urlopen("http://localhost:19083/daytrader/", timeout=1) as response:
                        if response.status == 200:
                            break
                except (OSError, TimeoutError):
                    pass
                if time.monotonic() > deadline:
                    raise RuntimeError("Readiness timeout")
                time.sleep(0.25)
            startup = time.monotonic() - started


            def sample():
                with (run / "resources.csv").open("w") as stream:
                    stream.write("elapsedSeconds,cpuPercent,rssKiB\n")
                    while not stop_sampling.is_set():
                        values = subprocess.check_output(["ps", "-p", str(pid), "-o", "%cpu=", "-o", "rss="],
                                                         text=True).split()
                        if len(values) == 2:
                            stream.write(str(time.monotonic() - started) + "," + ",".join(values) + "\n")
                            stream.flush()
                        stop_sampling.wait(0.1)


            sampler = threading.Thread(target=sample)
            sampler.start()
            execute([str(args.java_home / "bin/java"), "-Ddaytrader.baseUrl=http://localhost:19083/daytrader",
                     "-cp", classpath, "baseline.TradingWorkload", "http", str(run), str(workers), str(args.warmup),
                     str(args.measured)],
                    run / "http.log")
        finally:
            stop_sampling.set()
            if sampler:
                sampler.join(timeout=5)
            execute([str(server), "stop", "daytrader3_Baseline"], run / "stop.log", server_env)
        execute([str(args.java_home / "bin/java"), "-Dderby.stream.error.file=" + str(run / "derby.log"),
                 "-cp", classpath, "baseline.TradingWorkload", "sql", str(run),
                 str(build / "liberty-user/shared/resources/data/tradedb")], run / "sql.log")
        shutil.copyfile(build / "liberty-output/daytrader3_Baseline/logs/messages.log", run / "messages.log")
        rows = list(csv.DictReader((run / "requests.csv").open()))
        measured = [r for r in rows if r["measured"] == "true"]
        latency = sorted((int(r["endNanos"]) - int(r["startNanos"])) / 1e6 for r in measured)
        props = dict(line.strip().split("=", 1) for line in (run / "expected.properties").read_text().splitlines()
                     if line and not line.startswith("#"))
        seconds = (int(props["window.endNanos"]) - int(props["window.startNanos"])) / 1e9


        def percentile(q):
            return latency[max(0, math.ceil(len(latency) * q) - 1)]


        resources = list(csv.DictReader((run / "resources.csv").open()))
        summary = {"workers": workers, "repeat": repeat, "measuredPurchases": len(measured),
                   "measurementSeconds": seconds, "completedPurchasesPerSecond": len(measured) / seconds,
                   "buyResponseMs": {"p50": percentile(.5), "p95": percentile(.95), "p99": percentile(.99)},
                   "startupToHttpReadySeconds": startup,
                   "sampledPeakRssKiB": max(float(r["rssKiB"]) for r in resources),
                   "sampledPeakCpuPercent": max(float(r["cpuPercent"]) for r in resources),
                   "HTTPAndSqlInvariants": "pass"}
        (run / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        summaries.append(summary)
        (output / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
        print(json.dumps(summary), flush=True)
shutil.rmtree(classes)
