import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()


def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )
    return conn


def load_sales_data():
    query = """
        SELECT 
            soh.OrderDate,
            soh.TotalDue,
            p.Name AS Product,
            sp.Name AS State
        FROM Sales.SalesOrderHeader soh
        INNER JOIN Sales.SalesOrderDetail sod
            ON soh.SalesOrderID = sod.SalesOrderID
        INNER JOIN Production.Product p
            ON sod.ProductID = p.ProductID
        INNER JOIN Person.Address a
            ON soh.ShipToAddressID = a.AddressID
        INNER JOIN Person.StateProvince sp
            ON a.StateProvinceID = sp.StateProvinceID
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()

    return df
