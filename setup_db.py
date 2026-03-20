import sqlite3
import datetime

DB_NAME = 'inventory_chatbot.db'

def create_schema(cursor):
    cursor.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Customers (
        CustomerId   INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerCode VARCHAR(50)   UNIQUE NOT NULL,
        CustomerName NVARCHAR(200) NOT NULL,
        Email        NVARCHAR(200) NULL,
        Phone        NVARCHAR(50)  NULL,
        BillingAddress1 NVARCHAR(200) NULL,
        BillingCity  NVARCHAR(100) NULL,
        BillingCountry NVARCHAR(100) NULL,
        CreatedAt    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt    DATETIME NULL,
        IsActive     INTEGER  NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Vendors (
        VendorId    INTEGER PRIMARY KEY AUTOINCREMENT,
        VendorCode  VARCHAR(50)   UNIQUE NOT NULL,
        VendorName  NVARCHAR(200) NOT NULL,
        Email       NVARCHAR(200) NULL,
        Phone       NVARCHAR(50)  NULL,
        AddressLine1 NVARCHAR(200) NULL,
        City        NVARCHAR(100) NULL,
        Country     NVARCHAR(100) NULL,
        CreatedAt   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt   DATETIME NULL,
        IsActive    INTEGER  NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Sites (
        SiteId      INTEGER PRIMARY KEY AUTOINCREMENT,
        SiteCode    VARCHAR(50)   UNIQUE NOT NULL,
        SiteName    NVARCHAR(200) NOT NULL,
        AddressLine1 NVARCHAR(200) NULL,
        City        NVARCHAR(100) NULL,
        Country     NVARCHAR(100) NULL,
        TimeZone    NVARCHAR(100) NULL,
        CreatedAt   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt   DATETIME NULL,
        IsActive    INTEGER  NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Locations (
        LocationId       INTEGER PRIMARY KEY AUTOINCREMENT,
        SiteId           INTEGER NOT NULL,
        LocationCode     VARCHAR(50)   NOT NULL,
        LocationName     NVARCHAR(200) NOT NULL,
        ParentLocationId INTEGER NULL,
        CreatedAt        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt        DATETIME NULL,
        IsActive         INTEGER  NOT NULL DEFAULT 1,
        UNIQUE (SiteId, LocationCode),
        FOREIGN KEY (SiteId)           REFERENCES Sites(SiteId),
        FOREIGN KEY (ParentLocationId) REFERENCES Locations(LocationId)
    );

    CREATE TABLE IF NOT EXISTS Items (
        ItemId        INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemCode      NVARCHAR(100) UNIQUE NOT NULL,
        ItemName      NVARCHAR(200) NOT NULL,
        Category      NVARCHAR(100) NULL,
        UnitOfMeasure NVARCHAR(50)  NULL,
        CreatedAt     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt     DATETIME NULL,
        IsActive      INTEGER  NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Assets (
        AssetId      INTEGER PRIMARY KEY AUTOINCREMENT,
        AssetTag     VARCHAR(100)  UNIQUE NOT NULL,
        AssetName    NVARCHAR(200) NOT NULL,
        SiteId       INTEGER NOT NULL,
        LocationId   INTEGER NULL,
        SerialNumber NVARCHAR(200) NULL,
        Category     NVARCHAR(100) NULL,
        Status       VARCHAR(30)   NOT NULL DEFAULT 'Active',
        Cost         DECIMAL(18,2) NULL,
        PurchaseDate DATE NULL,
        VendorId     INTEGER NULL,
        CreatedAt    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt    DATETIME NULL,
        FOREIGN KEY (SiteId)     REFERENCES Sites(SiteId),
        FOREIGN KEY (LocationId) REFERENCES Locations(LocationId),
        FOREIGN KEY (VendorId)   REFERENCES Vendors(VendorId)
    );

    CREATE TABLE IF NOT EXISTS Bills (
        BillId      INTEGER PRIMARY KEY AUTOINCREMENT,
        VendorId    INTEGER NOT NULL,
        BillNumber  VARCHAR(100)  NOT NULL,
        BillDate    DATE NOT NULL,
        DueDate     DATE NULL,
        TotalAmount DECIMAL(18,2) NOT NULL,
        Currency    VARCHAR(10)   NOT NULL DEFAULT 'USD',
        Status      VARCHAR(30)   NOT NULL DEFAULT 'Open',
        CreatedAt   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt   DATETIME NULL,
        UNIQUE (VendorId, BillNumber),
        FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId)
    );

    CREATE TABLE IF NOT EXISTS PurchaseOrders (
        POId      INTEGER PRIMARY KEY AUTOINCREMENT,
        PONumber  VARCHAR(100) UNIQUE NOT NULL,
        VendorId  INTEGER NOT NULL,
        PODate    DATE NOT NULL,
        Status    VARCHAR(30) NOT NULL DEFAULT 'Open',
        SiteId    INTEGER NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId),
        FOREIGN KEY (SiteId)   REFERENCES Sites(SiteId)
    );

    CREATE TABLE IF NOT EXISTS PurchaseOrderLines (
        POLineId    INTEGER PRIMARY KEY AUTOINCREMENT,
        POId        INTEGER NOT NULL,
        LineNumber  INTEGER NOT NULL,
        ItemId      INTEGER NULL,
        ItemCode    NVARCHAR(100) NOT NULL,
        Description NVARCHAR(200) NULL,
        Quantity    DECIMAL(18,4) NOT NULL,
        UnitPrice   DECIMAL(18,4) NOT NULL,
        UNIQUE (POId, LineNumber),
        FOREIGN KEY (POId)   REFERENCES PurchaseOrders(POId),
        FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
    );

    CREATE TABLE IF NOT EXISTS SalesOrders (
        SOId       INTEGER PRIMARY KEY AUTOINCREMENT,
        SONumber   VARCHAR(100) UNIQUE NOT NULL,
        CustomerId INTEGER NOT NULL,
        SODate     DATE NOT NULL,
        Status     VARCHAR(30) NOT NULL DEFAULT 'Open',
        SiteId     INTEGER NULL,
        CreatedAt  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt  DATETIME NULL,
        FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId),
        FOREIGN KEY (SiteId)     REFERENCES Sites(SiteId)
    );

    CREATE TABLE IF NOT EXISTS SalesOrderLines (
        SOLineId    INTEGER PRIMARY KEY AUTOINCREMENT,
        SOId        INTEGER NOT NULL,
        LineNumber  INTEGER NOT NULL,
        ItemId      INTEGER NULL,
        ItemCode    NVARCHAR(100) NOT NULL,
        Description NVARCHAR(200) NULL,
        Quantity    DECIMAL(18,4) NOT NULL,
        UnitPrice   DECIMAL(18,4) NOT NULL,
        UNIQUE (SOId, LineNumber),
        FOREIGN KEY (SOId)   REFERENCES SalesOrders(SOId),
        FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
    );

    CREATE TABLE IF NOT EXISTS AssetTransactions (
        AssetTxnId     INTEGER PRIMARY KEY AUTOINCREMENT,
        AssetId        INTEGER NOT NULL,
        FromLocationId INTEGER NULL,
        ToLocationId   INTEGER NULL,
        TxnType        VARCHAR(30) NOT NULL,
        Quantity       INTEGER     NOT NULL DEFAULT 1,
        TxnDate        DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Note           NVARCHAR(500) NULL,
        FOREIGN KEY (AssetId)        REFERENCES Assets(AssetId),
        FOREIGN KEY (FromLocationId) REFERENCES Locations(LocationId),
        FOREIGN KEY (ToLocationId)   REFERENCES Locations(LocationId)
    );
    """)
    print("Schema created")

def seed_data(cursor):
    # 1. Customers
    customers = [
        ('C001', 'TechCorp Solutions', 'info@techcorp.com', '01012345678', '123 Nile St', 'Cairo', 'Egypt'),
        ('C002', 'Global Logistics', 'contact@globallog.com', '01198765432', '45 Industrial Zone', 'Alexandria', 'Egypt'),
        ('C003', 'Smart Education Inc', 'admin@smartedu.edu', '01234567890', 'Smart Village', 'Giza', 'Egypt'),
        ('C004', 'Alpha Construction', 'ops@alphacon.com', '01555443322', 'New Capital City', 'Cairo', 'Egypt'),
        ('C005', 'Delta Healthcare', 'supply@deltahealth.org', '01000111222', 'Health Square', 'Mansoura', 'Egypt')
    ]
    cursor.executemany("INSERT INTO Customers (CustomerCode, CustomerName, Email, Phone, BillingAddress1, BillingCity, BillingCountry) VALUES (?, ?, ?, ?, ?, ?, ?)", customers)

    # 2. Vendors
    vendors = [
        ('V001', 'Dell Global', 'sales@dell.com', '1-800-DELL', 'Round Rock', 'Texas', 'USA'),
        ('V002', 'Logitech ME', 'me@logitech.com', '971-4-1234', 'Media City', 'Dubai', 'UAE'),
        ('V003', 'Cisco Systems', 'orders@cisco.com', '1-800-CISCO', 'San Jose', 'California', 'USA'),
        ('V004', 'Steelcase Furniture', 'office@steelcase.com', '1-800-STEEL', 'Grand Rapids', 'Michigan', 'USA'),
        ('V005', 'HP Enterprise', 'support@hpe.com', '1-800-HPE', 'Palo Alto', 'California', 'USA')
    ]
    cursor.executemany("INSERT INTO Vendors (VendorCode, VendorName, Email, Phone, AddressLine1, City, Country) VALUES (?, ?, ?, ?, ?, ?, ?)", vendors)

    # 3. Sites
    sites = [
        ('S001', 'Cairo Headquarters', 'New Cairo', 'Cairo', 'EET'),
        ('S002', 'Alexandria Branch', 'Smouha', 'Alexandria', 'EET'),
        ('S003', 'Giza Tech Center', 'Smart Village', 'Giza', 'EET'),
        ('S004', 'Port Said Hub', 'Customs Zone', 'Port Said', 'EET'),
        ('S005', 'Aswan Solar Base', 'Main Road', 'Aswan', 'EET')
    ]
    cursor.executemany("INSERT INTO Sites (SiteCode, SiteName, AddressLine1, City, TimeZone) VALUES (?, ?, ?, ?, ?)", sites)

    # 4. Locations (linked to Sites)
    locations = [
        (1, 'LOC-WH-01', 'Main Warehouse', None),
        (1, 'LOC-IT-01', 'IT Support Lab', 1),
        (2, 'LOC-ALX-01', 'Alexandria Storage', None),
        (3, 'LOC-GZ-01', 'Server Room Alpha', None),
        (5, 'LOC-ASW-01', 'Field Equipment Tent', None)
    ]
    cursor.executemany("INSERT INTO Locations (SiteId, LocationCode, LocationName, ParentLocationId) VALUES (?, ?, ?, ?)", locations)

    # 5. Items
    items = [
        ('ITM-LPT', 'XPS 15 Laptop', 'Hardware', 'Unit'),
        ('ITM-MS', 'MX Master Mouse', 'Peripherals', 'Unit'),
        ('ITM-SVR', 'PowerEdge Server', 'Infrastructure', 'Unit'),
        ('ITM-SW', 'Cisco Switch 24-Port', 'Networking', 'Unit'),
        ('ITM-CHR', 'Ergonomic Office Chair', 'Furniture', 'Unit')
    ]
    cursor.executemany("INSERT INTO Items (ItemCode, ItemName, Category, UnitOfMeasure) VALUES (?, ?, ?, ?)", items)

    # 6. Assets (linked to Sites, Locations, Vendors)
    assets = [
        ('TAG-001', 'XPS Laptop 01', 1, 2, 'Active', 1500.00, 1),
        ('TAG-002', 'XPS Laptop 02', 1, 2, 'Active', 1500.00, 1),
        ('TAG-003', 'MX Mouse 01', 1, 2, 'Active', 100.00, 2),
        ('TAG-004', 'Cisco Switch A', 3, 4, 'Maintenance', 2500.00, 3),
        ('TAG-005', 'Exec Chair 01', 2, 3, 'Active', 450.00, 4)
    ]
    cursor.executemany("INSERT INTO Assets (AssetTag, AssetName, SiteId, LocationId, Status, Cost, VendorId) VALUES (?, ?, ?, ?, ?, ?, ?)", assets)

    # 7. Bills (linked to Vendors)
    bills = [
        (1, 'BILL-101', '2026-03-01', 3000.00, 'Open'),
        (2, 'BILL-102', '2026-03-02', 200.00, 'Paid'),
        (3, 'BILL-103', '2026-03-05', 2500.00, 'Open'),
        (4, 'BILL-104', '2026-03-07', 900.00, 'Pending'),
        (5, 'BILL-105', '2026-03-10', 1200.00, 'Open')
    ]
    cursor.executemany("INSERT INTO Bills (VendorId, BillNumber, BillDate, TotalAmount, Status) VALUES (?, ?, ?, ?, ?)", bills)

    # 8. Purchase Orders (linked to Vendors, Sites)
    pos = [
        ('PO-5001', 1, '2026-02-15', 'Closed', 1),
        ('PO-5002', 2, '2026-02-20', 'Received', 1),
        ('PO-5003', 3, '2026-03-01', 'Open', 3),
        ('PO-5004', 4, '2026-03-05', 'Open', 2),
        ('PO-5005', 5, '2026-03-08', 'Cancelled', 1)
    ]
    cursor.executemany("INSERT INTO PurchaseOrders (PONumber, VendorId, PODate, Status, SiteId) VALUES (?, ?, ?, ?, ?)", pos)

    # 9. PO Lines (linked to POs, Items)
    po_lines = [
        (1, 1, 'ITM-LPT', 2, 1500.00),
        (2, 1, 'ITM-MS', 2, 100.00),
        (3, 1, 'ITM-SW', 1, 2500.00),
        (4, 1, 'ITM-CHR', 2, 450.00),
        (5, 1, 'ITM-SVR', 1, 5000.00)
    ]
    cursor.executemany("INSERT INTO PurchaseOrderLines (POId, LineNumber, ItemCode, Quantity, UnitPrice) VALUES (?, ?, ?, ?, ?)", po_lines)

    # 10. Sales Orders (linked to Customers, Sites)
    sos = [
        ('SO-9001', 1, '2026-03-05', 'Open', 1),
        ('SO-9002', 2, '2026-03-06', 'Pending', 2),
        ('SO-9003', 3, '2026-03-07', 'Closed', 3),
        ('SO-9004', 4, '2026-03-08', 'Open', 1),
        ('SO-9005', 5, '2026-03-09', 'Cancelled', 4)
    ]
    cursor.executemany("INSERT INTO SalesOrders (SONumber, CustomerId, SODate, Status, SiteId) VALUES (?, ?, ?, ?, ?)", sos)

    # 11. SO Lines (linked to SOs, Items)
    so_lines = [
        (1, 1, 'ITM-LPT', 1, 1800.00),
        (2, 1, 'ITM-MS', 1, 150.00),
        (3, 1, 'ITM-SVR', 1, 6500.00),
        (4, 1, 'ITM-CHR', 1, 600.00),
        (5, 1, 'ITM-SW', 1, 3200.00)
    ]
    cursor.executemany("INSERT INTO SalesOrderLines (SOId, LineNumber, ItemCode, Quantity, UnitPrice) VALUES (?, ?, ?, ?, ?)", so_lines)

    # 12. Asset Transactions (linked to Assets, Locations)
    txns = [
        (1, 1, 2, 'Transfer', 'Routine move to IT lab'),
        (2, 2, 1, 'Repair', 'Screen flickering issue'),
        (3, 1, 3, 'Deployment', 'New hire setup'),
        (4, 4, 1, 'Storage', 'Decommissioned for maintenance'),
        (5, 5, 2, 'Audit', 'Physical verification check')
    ]
    cursor.executemany("INSERT INTO AssetTransactions (AssetId, FromLocationId, ToLocationId, TxnType, Note) VALUES (?, ?, ?, ?, ?)", txns)


def main():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    create_schema(cursor)
    seed_data(cursor)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()