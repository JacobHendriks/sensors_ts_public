import db_utils
import benchmark_utils
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm
import pickle as pkl
import random
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

random.seed(1884)
#%%
#------------------------------------------------------------------------------
# Create an empty database
#------------------------------------------------------------------------------

# This function isn't working - instead I am manually running creation script
# in pgadmin query tool

#db_utils.create_db_from_script()

#------------------------------------------------------------------------------
# Define experimental parameters
#------------------------------------------------------------------------------

params = {
    'num_institutions' : 6,
    'num_sensor_models' : 3,
    'machine_tags_per_machine' : 2,
    'machine_tag_values_per_machine_tag_names' : 4,
    'users_per_institution' : 3,
    'gateways_per_user' : 3,
    'machines_per_gateway' : 3,
    'components_per_machine' : 2,
    'sensors_per_component' : 2,
    'measurement_period' : 5,       # Time interval in minutes
    'metric_names' : ['mean', 'rms', 'kurtosis'] # Len of list det.s # metrics / measurement
    }

# Some additional params are calculated from above:
params['num_users'] = params['num_institutions']*params['users_per_institution']
params['num_gateways'] = params['num_users']*params['gateways_per_user']
params['num_machines'] = params['num_gateways']*params['machines_per_gateway']
params['num_machine_tags'] = params['machine_tags_per_machine']*params['num_machines']
params['num_components'] = params['components_per_machine']*params['num_machines']
params['num_sensors'] = params['sensors_per_component']*params['num_components']
params['sensors_per_gateway'] = params['num_sensors'] / params['num_gateways']

# Enumeration parameters:
params['property_measured_options'] = ['acceleration', 'temperature']
params['machine_type_options'] = ['motor', 'pump', 'gearbox']
params['machine_tag_name_options'] = ['status', 'location', 'model']
params['component_type_options'] = ['bearing', 'gear', 'shaft']

# Test queries to run as the database is populated
with open('measurement_queries.sql','r', encoding="utf-8") as file:
    queries = file.read().split('/*/////*/')
    
# Initialize results dictionary
results = {'query_number' : [],
           'measurements_count' : [],
           'rows_affected' : [],
           'execution_time' : []}
results = pd.DataFrame(results)
# write it, just to get a header
results.to_csv('results.csv', header = True, index = False)
#%%

#------------------------------------------------------------------------------
# Create initial db entries (don't increase with incoming new measurement data)
#------------------------------------------------------------------------------

# Each is a list of dicts and is based on params defined above
# The keys to this dict should be table names and values should be dataframes
# Dataframe column names must match column names in the db; datatypes must als
# match
meta_tables, meta_uuids = benchmark_utils.get_metadata(params)

# Let's add these dfs to the db

# Connect to DB and create a cursor
conn = db_utils.connect()
cur = conn.cursor()

# Iterate through each table in dict and add to db
for table_name, df in meta_tables.items():
    db_utils.add_df(cur, table_name, df)
    
# Commit the changes to the database
conn.commit()

# Close the cursor and database connection
cur.close()
conn.close()

#%%
#------------------------------------------------------------------------------
# Begin to generate measurements, measurement tags, metrics, events, raw_data
#------------------------------------------------------------------------------

# Set first timestamp
nominal_time = '01/01/22 12:00:00'
nominal_time = datetime.strptime(nominal_time, '%m/%d/%y %H:%M:%S')

# Set the nominal time delta between measurements in minutes
delta_time = timedelta(seconds = 5*60)

# Create empty dfs which we will extend each newly generated batch with
data_tables = pd.DataFrame({'measurements' : [],
               'measurement_tags' : [],
               'metrics' : [],
               'raw_data' : []})

#%%
# Add a certain # of time steps, run the test querries, log results, and repeat
# At time of writing, each individual measurement adds 0.2849 kb to measurements
# This code cell can be re-run to generate more batches... By loading pickle file,
# one can resume adding and logging in a new session

num_batches = 5000 # Equals number of time steps that will be added for ea sensor
query_interval = 10

# Write a csv file with a header that we will append to...
pbar = tqdm(range(num_batches))
for batch_idx in pbar:
    
    # A batch contains 1 measurement, 1 raw_data, 1 measurement tag, and
    # len(params['metric_names']) metrics --- per sensor ---
    # Note that events have not been implimented in the benchmark
    pdesc = "Generating data"
    pbar.set_description("{:<25}".format(pdesc))
    new_data = benchmark_utils.get_one_batch(params, meta_tables, nominal_time)

    # Convert those from dicts to data frames
    new_data = benchmark_utils.to_dataframe(new_data)
    
    # Extend our lists. Alternatively, we may wish to upload to the db as they
    # are generated. Or we can generate a few batches and upload those together
    data_tables = benchmark_utils.extend_dict_dfs(data_tables, new_data)
    nominal_time = nominal_time + delta_time
    
    # Let's add these dfs to the db
    
    # Connect to DB and create a cursor    
    conn = db_utils.connect()
    cur = conn.cursor()
    
    # Iterate through each table in dict and add to db
    for table_name, df in new_data.items():
        pdesc = f"Adding {table_name}"
        pbar.set_description("{:<25}".format(pdesc))
        db_utils.add_df(cur, table_name, df)
        
    # Commit the changes to the database    
    conn.commit()
    
    # Close the cursor and database connection
    cur.close()
    conn.close()
    
    # Conditionally run the execution querries
    if (batch_idx+1) % query_interval == 0:        
        batch_results = {'query_number' : [],
                         'measurements_count' : [],
                         'rows_affected' : [],
                         'execution_time' : []}
        for i in range(len(queries)):
            pdesc = f"Test query {i}/{len(queries)}"
            pbar.set_description("{:<25}".format(pdesc))
            
            try:
                res = db_utils.query_to_df(queries[i])
                nrow, et = len(res[0]), res[1]
            except:
                nrow = 'nan'
                et = 'nan'
            results['query_number']
            batch_results['query_number'].append(i)
            batch_results['measurements_count'].append(len(data_tables['measurements']))
            batch_results['rows_affected'].append(nrow)
            batch_results['execution_time'].append(et)
        batch_results = pd.DataFrame(batch_results)            
        batch_results.to_csv('results.csv', mode='a', header=False, index=False)
        results = pd.concat([results, batch_results])
        
with open('vars.pkl', 'wb') as file:
    pkl.dump([meta_tables, data_tables, nominal_time, params, results], file)
    
#%%
with open('vars.pkl', 'rb') as file:
    meta_tables, data_tables, nominal_time, params, results = pkl.load(file)