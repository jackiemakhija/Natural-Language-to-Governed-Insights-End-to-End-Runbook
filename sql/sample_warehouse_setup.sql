-- SQL Examples from NL_to_Governed_Insights_End_to_End_Runbook
-- Fabric Warehouse setup for Star Schema: DimDate + FactSales

-- ============================================================
-- STEP 1: Create DimDate Table
-- ============================================================
CREATE TABLE dbo.DimDate (
  DateKey       INT         NOT NULL PRIMARY KEY,
  [Date]        DATE        NOT NULL,
  [Year]        INT         NOT NULL,
  [MonthNumber] INT         NOT NULL,
  [MonthName]   VARCHAR(20) NOT NULL
);

-- ============================================================
-- STEP 2: Create FactSales Table
-- ============================================================
CREATE TABLE dbo.FactSales (
  SalesId  BIGINT        NOT NULL PRIMARY KEY,
  DateKey  INT           NOT NULL REFERENCES dbo.DimDate(DateKey),
  Revenue  DECIMAL(18,2) NOT NULL,
  Cost     DECIMAL(18,2) NOT NULL,
  Quantity INT           NOT NULL
);

-- ============================================================
-- STEP 3: Load Sample Data into DimDate
-- Load last 90 days
-- ============================================================
DECLARE @d DATE = DATEADD(DAY, -89, CAST(GETDATE() AS DATE));
WHILE @d <= CAST(GETDATE() AS DATE)
BEGIN
  INSERT INTO dbo.DimDate (DateKey, [Date], [Year], [MonthNumber], [MonthName])
  VALUES (
    CONVERT(INT, FORMAT(@d,'yyyyMMdd')),
    @d,
    YEAR(@d),
    MONTH(@d),
    DATENAME(MONTH, @d)
  );
  SET @d = DATEADD(DAY, 1, @d);
END;

-- ============================================================
-- STEP 4: Load Sample Data into FactSales
-- Generate 300 random sales records
-- ============================================================
DECLARE @i INT = 1;
WHILE @i <= 300
BEGIN
  DECLARE @dt DATE = DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 90, CAST(GETDATE() AS DATE));
  DECLARE @dateKey INT = CONVERT(INT, FORMAT(@dt,'yyyyMMdd'));
  INSERT INTO dbo.FactSales (SalesId, DateKey, Revenue, Cost, Quantity)
  VALUES (
    @i,
    @dateKey,
    CAST(50 + (ABS(CHECKSUM(NEWID())) % 5000) / 10.0 AS DECIMAL(18,2)),
    CAST(20 + (ABS(CHECKSUM(NEWID())) % 3000) / 10.0 AS DECIMAL(18,2)),
    1 + (ABS(CHECKSUM(NEWID())) % 10)
  );
  SET @i += 1;
END;

-- ============================================================
-- STEP 5: Validate Data
-- ============================================================
SELECT COUNT(*) as TotalDates FROM dbo.DimDate;
SELECT COUNT(*) as TotalSales FROM dbo.FactSales;

-- Sample query
SELECT TOP 10
  d.[Date],
  d.[MonthName],
  f.Revenue,
  f.Cost,
  f.Quantity,
  (f.Revenue - f.Cost) AS Profit
FROM dbo.FactSales f
INNER JOIN dbo.DimDate d ON f.DateKey = d.DateKey
ORDER BY d.[Date] DESC;

-- ============================================================
-- STEP 6: Aggregate Statistics
-- ============================================================
SELECT
  d.[Year],
  d.[MonthName],
  COUNT(f.SalesId) as TotalTransactions,
  SUM(f.Revenue) as TotalRevenue,
  SUM(f.Cost) as TotalCost,
  SUM(f.Revenue - f.Cost) as TotalProfit,
  AVG(f.Revenue) as AvgRevenue,
  SUM(f.Quantity) as TotalQuantity
FROM dbo.FactSales f
INNER JOIN dbo.DimDate d ON f.DateKey = d.DateKey
GROUP BY d.[Year], d.[MonthName]
ORDER BY d.[Year] DESC, d.[MonthNumber] DESC;
