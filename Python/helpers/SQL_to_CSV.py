import pandas as pd
from sqlalchemy import create_engine


def export_tables_to_csv(engine, tables, output_folder):

    for table in tables:
        try:
            # Read table into a DataFrame
            df = pd.read_sql_table(table, engine)

            # Define CSV file path
            csv_file_path = f"{output_folder}/{table}.csv"

            # Export DataFrame to CSV
            df.to_csv(csv_file_path, index=False)

            print(f"Table {table} exported to {csv_file_path}")
        except Exception as e:
            print(f"An error occurred while exporting table {table}: {e}")


if __name__ == "__main__":
    # Example usage
    db_server_url = "SQL_SERVER"
    db_name = "DATABASE_NAME"
    ENGINE = create_engine(
        f"mssql+pyodbc://{db_server_url}/{db_name}?driver=SQL Server Native Client 11.0",
        echo=False,
        fast_executemany=False,
        future=True,
    )
    TABLES = ["TABLE_1", "TABLE_2"]
    OUTPUT_FOLDER = "C:/Folder/"

    export_tables_to_csv(ENGINE, TABLES, OUTPUT_FOLDER)
