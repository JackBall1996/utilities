from sqlalchemy import create_engine


def create_db_engine(db_server_url, db_name):
    """_summary_

    Args:
        db_server_url (_type_): SQL_Server
        db_name (_type_): Database_Name

    Call as:
        import SQL_Connection_Manager as cm
        
        sql_engine = cm.create_db_engine('SERVER','DATABASE')
        
        with sql_engine.connect() as conn:
    """

    engine = create_engine(f'mssql+pyodbc://{db_server_url}/{db_name}?driver=SQL Server Native Client 11.0', echo = False, fast_executemany=False, pool_timeout=36000, pool_size = 500, max_overflow=500)

    try:
        test_connection = engine.connect()
        test_connection.close()
    except Exception as ie:
        #log exception
        print((f'Connection to {db_server_url}/{db_name} failed. Review log for full exception.\n'
                  'Possible reasons include:\n'
                '- The supplied connection string is not accurate.\n' 
                '- The database does not exist.\n'
                '- pyodbc is not installed.\n'
                '- odbc driver is not installed.'))
        raise
    
    return engine