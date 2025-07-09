from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text
import os
import shutil
import os.path

db_server_url = "Server_Name"
db_name = "Database_Name"

sql_engine = create_engine(
    f"mssql+pyodbc://{db_server_url}/{db_name}?driver=SQL Server Native Client 11.0",
    echo=False,
    fast_executemany=False,
    future=True,
)

query = """
SELECT
    FILE_NAME,
    CONCAT(SUBSTRING(FILE_NAME,7,4),'-',SUBSTRING(FILE_NAME,11,2),'-',SUBSTRING(FILE_NAME,13,2)) AS DateFolder
FROM ods.OMD_FILE_LOG
    WHERE LOAD_STATUS IN ('')
"""

with sql_engine.connect() as conn:
    output = pd.read_sql_query(text(query), conn)
    FILE_NAME = output["FILE_NAME"]
    DATE = output["DateFolder"]

x = 0
y = len(output.index)

while x < y:
    print(x)
    source_folder = "source_folder"
    destination_folder = "destination_folder"

    source_file = source_folder + output["FILE_NAME"][x]
    print(source_file)

    destination_folder = destination_folder + output["DateFolder"][x] + "/"
    print(destination_folder)

    destination_file = destination_folder + output["FILE_NAME"][x]
    print(destination_file)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    if os.path.exists(source_file):
        shutil.move(source_file, destination_file)
        print("moved")
        print("")

    else:
        print("file does not exist")

    x = x + 1
