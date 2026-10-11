package baseline;

import java.io.*;
import java.math.BigDecimal;
import java.nio.file.*;
import java.sql.*;
import java.util.*;
import java.util.concurrent.*;

/**
 * Bounded external workload using the pinned legacy adapter; no application imports.
 */
public final class TradingWorkload {
    private static final BigDecimal FEE = new BigDecimal("24.95");

    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    private static void equalMoney(BigDecimal expected, BigDecimal actual) {
        require(expected.compareTo(actual) == 0, expected + " != " + actual);
    }

    public static void main(String[] args) throws Exception {
        Path output = Paths.get(args[1]);
        if (args[0].equals("sql")) {
            inspect(args[2], output);
            return;
        }
        int workers = Integer.parseInt(args[2]);
        int warmup = 5, measured = 20;
        Properties expectations = new Properties();
        new TradeClient().configure(0, 0);
        ExecutorService pool = Executors.newFixedThreadPool(workers);
        long[] window = new long[2];
        CyclicBarrier ready = new CyclicBarrier(workers, () -> window[0] = System.nanoTime());
        List<Future<String>> results = new ArrayList<>();
        try {
            for (int worker = 0; worker < workers; worker++) {
                final int account = 30 + worker;
                results.add(pool.submit(() -> {
                    TradeClient client = new TradeClient();
                    require(client.login(account).status == 200, "Login failed");
                    BigDecimal cash = BigDecimal.valueOf(10000 + account * 1000).setScale(2);
                    String symbol = "s:" + account;
                    StringBuilder samples = new StringBuilder();
                    for (int i = 0; i < warmup + measured; i++) {
                        if (i == warmup) ready.await(30, TimeUnit.SECONDS);
                        BigDecimal price = client.quote(symbol);
                        cash = cash.subtract(price).subtract(FEE);
                        long start = System.nanoTime();
                        TradeClient.Response response = client.action("action", "buy", "symbol", symbol, "quantity", "1");
                        long end = System.nanoTime();
                        require(response.status == 200, "Purchase HTTP " + response.status);
                        samples.append(account).append(',').append(i >= warmup).append(',')
                                .append(start).append(',').append(end).append(',').append(price).append('\n');
                        if (i == warmup + measured - 1) synchronized (window) {
                            window[1] = Math.max(window[1], end);
                        }
                        Thread.sleep(20);
                    }
                    client.logout();
                    TradeClient fresh = new TradeClient();
                    require(fresh.login(account).status == 200, "Fresh login failed");
                    equalMoney(cash, TradeClient.cash(fresh.account()));
                    List<TradeClient.Order> orders = fresh.orders();
                    List<TradeClient.Holding> holdings = fresh.holdings();
                    require(orders.size() == warmup + measured, "Order count");
                    require(holdings.size() == warmup + measured, "Holding count");
                    BigDecimal debits = BigDecimal.ZERO, holdingValue = BigDecimal.ZERO;
                    Set<Integer> orderIds = new HashSet<>(), holdingIds = new HashSet<>();
                    for (TradeClient.Order order : orders) {
                        require(orderIds.add(order.id), "Duplicate order");
                        require(order.type.equals("buy") && order.status.equals("completed")
                                && order.symbol.equals(symbol), "Order identity/status");
                        equalMoney(BigDecimal.ONE, order.quantity);
                        equalMoney(FEE, order.fee);
                        debits = debits.add(order.price).add(order.fee);
                    }
                    for (TradeClient.Holding holding : holdings) {
                        require(holdingIds.add(holding.id) && holding.symbol.equals(symbol), "Holding identity");
                        equalMoney(BigDecimal.ONE, holding.quantity);
                        holdingValue = holdingValue.add(holding.price);
                    }
                    equalMoney(debits.subtract(FEE.multiply(BigDecimal.valueOf(orders.size()))), holdingValue);
                    equalMoney(BigDecimal.valueOf(10000 + account * 1000).subtract(debits), cash);
                    fresh.logout();
                    synchronized (expectations) {
                        expectations.setProperty(account + ".cash", cash.toPlainString());
                        expectations.setProperty(account + ".count", "" + orders.size());
                    }
                    return samples.toString();
                }));
            }
            StringBuilder csv = new StringBuilder("account,measured,startNanos,endNanos,expectedPrice\n");
            for (Future<String> result : results) csv.append(result.get(120, TimeUnit.SECONDS));
            Files.write(output.resolve("requests.csv"), csv.toString().getBytes("UTF-8"));
            expectations.setProperty("window.startNanos", "" + window[0]);
            expectations.setProperty("window.endNanos", "" + window[1]);
            try (OutputStream out = Files.newOutputStream(output.resolve("expected.properties"))) {
                expectations.store(out, "Expectations computed from pre-purchase quotes; warmup state retained");
            }
            System.out.println("HTTP business invariants pass; workers=" + workers);
        } finally {
            pool.shutdownNow();
            require(pool.awaitTermination(10, TimeUnit.SECONDS), "Workers did not stop");
        }
    }

    private static void inspect(String database, Path output) throws Exception {
        Properties expected = new Properties();
        try (InputStream in = Files.newInputStream(output.resolve("expected.properties"))) {
            expected.load(in);
        }
        Class.forName("org.apache.derby.jdbc.EmbeddedDriver");
        String url = "jdbc:derby:" + database;
        try (Connection c = DriverManager.getConnection(url, "db_username", "db_password")) {
            for (String key : expected.stringPropertyNames()) {
                if (!key.endsWith(".cash")) continue;
                int account = Integer.parseInt(key.split("\\.")[0]);
                int count = Integer.parseInt(expected.getProperty(account + ".count"));
                try (Statement sql = c.createStatement()) {
                    try (ResultSet r = sql.executeQuery("SELECT BALANCE FROM ACCOUNTEJB WHERE ACCOUNTID=" + account)) {
                        require(r.next(), "Missing account");
                        equalMoney(new BigDecimal(expected.getProperty(key)), r.getBigDecimal(1));
                    }
                    for (String table : new String[]{"ORDEREJB", "HOLDINGEJB"}) {
                        try (ResultSet r = sql.executeQuery("SELECT COUNT(*) FROM " + table + " WHERE ACCOUNT_ACCOUNTID=" + account)) {
                            require(r.next() && r.getInt(1) == count, table + " count");
                        }
                    }
                    try (ResultSet r = sql.executeQuery("SELECT COUNT(*) FROM ORDEREJB o JOIN HOLDINGEJB h "
                            + "ON o.HOLDING_HOLDINGID=h.HOLDINGID WHERE o.ACCOUNT_ACCOUNTID=" + account
                            + " AND h.ACCOUNT_ACCOUNTID=" + account + " AND o.ORDERSTATUS='completed'"
                            + " AND o.ORDERTYPE='buy' AND o.QUANTITY=1 AND h.QUANTITY=1"
                            + " AND o.PRICE=h.PURCHASEPRICE AND o.ORDERFEE=24.95")) {
                        require(r.next() && r.getInt(1) == count, "Persisted order/holding links");
                    }
                }
            }
        } finally {
            try {
                DriverManager.getConnection(url + ";shutdown=true");
            } catch (SQLException stopped) {
                if (!"08006".equals(stopped.getSQLState())) throw stopped;
            }
        }
        System.out.println("Stopped-DB financial and order/holding invariants pass");
    }
}
