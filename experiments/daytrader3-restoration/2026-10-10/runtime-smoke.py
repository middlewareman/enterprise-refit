"""Local DayTrader check; --create-tables / --populate replace sample data."""
import argparse
import http.cookiejar
import json
import re
import urllib.parse
import urllib.request
from html import unescape


def plain(html):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())


def holdings(html):
    result = {}
    for row in re.findall(r"<TR\b[^>]*>(.*?)</TR>", html, re.I | re.S):
        match = re.search(r"action=sell&(?:amp;)?holdingID=(\d+)", row)
        if match:
            result[match[1]] = plain(row)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://localhost:9083/daytrader")
    setup = parser.add_mutually_exclusive_group()
    setup.add_argument("--create-tables", action="store_true")
    setup.add_argument("--populate", action="store_true")
    args = parser.parse_args()
    client = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )

    def request(path, **params):
        payload = urllib.parse.urlencode(params).encode() if params else None
        with client.open(args.base + path, payload, timeout=180) as response:
            assert response.status == 200, response.status
            return response.read().decode("utf-8", errors="replace")

    config = request("/config", action="updateConfig", RunTimeMode=0,
                     OrderProcessingMode=0, MaxUsers=10, MaxQuotes=100)
    assert "DayTrader Configuration Updated" in plain(config), plain(config)
    if args.create_tables:
        tables = request("/config", action="buildDBTables")
        assert "tables successfully created" in plain(tables), plain(tables)
        print(plain(tables))
        return
    if args.populate:
        population = request("/config", action="buildDB")
        assert "10users created" in plain(population), plain(population)
        assert "abort" not in plain(population).lower(), plain(population)
        print(json.dumps({"fixture": "10 users, 100 quotes; randomly generated",
                          "population_response": plain(population)}, indent=2))
        return

    def login():
        html = request("/app", action="login", uid="uid:0", passwd="xxx")
        assert "Welcome uid:0," in plain(html) and "cash balance:" in plain(html), plain(html)

    login()
    quotes = request("/app", action="quotes", symbols="s:0")
    assert "s:0" in plain(quotes), plain(quotes)
    before = holdings(request("/app", action="portfolio"))
    buy = plain(request("/app", action="buy", symbol="s:0", quantity=2))
    assert re.search(r"buy\s+2\.0\s+shares of\s+s:0", buy), buy
    assert "closed" in buy, buy
    after_buy = holdings(request("/app", action="portfolio"))
    added = set(after_buy) - set(before)
    assert len(added) == 1 and len(after_buy) == len(before) + 1, after_buy
    holding_id = added.pop()
    assert re.search(r"s:0\s+2\.0\b", after_buy[holding_id]), after_buy[holding_id]
    request("/app", action="logout")
    login()
    persisted = holdings(request("/app", action="portfolio"))
    assert holding_id in persisted, persisted
    sell = plain(request("/app", action="sell", holdingID=holding_id))
    assert re.search(r"sell\s+2\.0\s+shares of\s+s:0", sell), sell
    assert "closed" in sell, sell
    request("/app", action="logout")
    login()
    final = holdings(request("/app", action="portfolio"))
    assert set(final) == set(before), final
    request("/app", action="logout")
    print(json.dumps({"result": "PASS", "mode": "Full EJB3 / synchronous",
                      "user": "uid:0", "quote": "s:0", "quantity": 2,
                      "holding_id": holding_id, "holdings_before": len(before),
                      "holdings_after_buy": len(after_buy),
                      "holdings_after_sell": len(final),
                      "buy": buy, "sell": sell}, indent=2))


if __name__ == "__main__":
    main()
