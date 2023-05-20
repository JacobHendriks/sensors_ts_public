import psycopg2
import pandas as pd
import timeit as ti

def connect():
    
    CONNECTION = "dbname =sensors_ts user=postgres password=password host=Jacobs-PC port=5432"
    #CONNECTION = "dbname =postgres user=postgres password=password host=206.12.99.100 port=5432"
    #Attempt to connect, abort if connection fails.
    try:
        #print(CONNECTION)
        conn = psycopg2.connect(CONNECTION)
        #print("Connected successful.")
    except:
        print("Connection failed.")
        raise SystemExit(0)
    return conn

def create_db_from_script():
    conn = connect()
    cur = conn.cursor()
    cur.execute(open("sensors_ts_db_creation_script.sql", "r").read())
    conn.commit()

# Read data from PostgreSQL database table and load into a DataFrame 
# Return a tuple of resulting dataframe and the execution time
def query_to_df(query):
    start = ti.time.perf_counter()
    dbconn = connect()
    df = pd.read_sql(query, dbconn)
    end = ti.time.perf_counter()
    exe_time = end - start
    return (df,exe_time)

def add_df(cur, table_name, df):
    
    column_names = list(df.columns)
    
    # Create the INSERT INTO query string with the correct number of placeholders
    num_columns = len(column_names)
    value_placeholders = ", ".join(["%s"] * num_columns)
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({value_placeholders})"
    
    # Convert the DataFrame to a list of tuples
    values = [tuple(x) for x in df.to_numpy()]
    
    # Insert the data into the database
    cur.executemany(insert_query, values)

def get_values(cur, table_name, df):
    # Get the column names from the dataframe
    columns = list(df.columns)
    
    # Create a SQL query to insert the dataframe rows into the table
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
    
    # Convert the dataframe to a list of tuples to use in the insert query
    return [tuple(row) for row in df.to_numpy()]