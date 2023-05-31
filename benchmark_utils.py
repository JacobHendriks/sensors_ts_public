from faker import Faker
import random
import json
import numpy as np
import pandas as pd
from datetime import timedelta
import random

fake = Faker()
Faker.seed(10)

def uuid_gen(n):
    return [fake.uuid4() for n in range(n)] 

def get_metadata(params):
    
    uuids = {'institutions' : uuid_gen(params['num_institutions']),
              'users' : uuid_gen(params['num_users']),
              'sensor_models' : uuid_gen(params['num_sensor_models']),
              'gateways' : uuid_gen(params['num_gateways']),
              'machines' : uuid_gen(params['num_machines']),
              'machine_tags' : uuid_gen(params['num_machine_tags']),
              'components' : uuid_gen(params['num_components']),
              'sensors' : uuid_gen(params['num_sensors']),
              }
    
    
    # Generate some fake institutions
    institutions = []
    for i in range(params['num_institutions']):
        institutions.append({
            'institution_id' : uuids['institutions'][i],
            'administrative_user_id' : uuids['users'][i*params['users_per_institution']],
            'institution_name' : f"University of {fake.city()}",
            'institution' : 'placeholder'
            })

    # Generate some fake users
    users = []
    for i in range(params['num_users']):
        users.append({
            'user_id' : uuids['users'][i],
            'institution_id' : uuids['institutions'][int(i / params['users_per_institution'])],
            'user_email' : fake.ascii_company_email(),
            'user_password' : fake.word()+fake.word()+str(random.random())[-3:],
            'institution' : 'placeholder'
            })

    # Generate some fake sensor models
    sensor_models = []
    for i in range(params['num_sensor_models']):
        sensor_models.append({
            'sensor_model_id' : uuids['sensor_models'][i],
            'property_measured' : random.choice(params['property_measured_options']),
            'manufacturer' : fake.company(),
            'model_number' : str(random.random())[-5:]
            })
        
    # Generate some fake gateways
    gateways = []
    for i in range(params['num_gateways']):
        gateways.append({
            'gateway_id' : uuids['gateways'][i],
            'user_id' : uuids['users'][int(i/params['gateways_per_user'])],
            'model_number' : str(random.random())[-5:],
            'serial_number' : str(random.random())[-8:],
            'last_transmission' : fake.date()
            })

    # Generate some machines
    machines = []
    for i in range(params['num_machines']):
        machine_type = random.choice(params['machine_type_options'])
        machines.append({
            'machine_id' : uuids['machines'][i],
            'machine_name' : fake.name().split(' ')[0] + "'s " + machine_type,
            'machine_type' : machine_type,
            'last_serviced' : fake.date(),
            'next_service' : fake.date()
            })
        
    # Generate some machine tags
    machine_tags = []
    for i in range(params['num_machine_tags']):
        machine_tag_name = random.choice(params['machine_tag_name_options'])
        machine_tags.append({
            'machine_tag_id' : uuids['machine_tags'][i],
            'machine_id' : uuids['machines'][int(i/params['machine_tags_per_machine'])],
            'machine_name' : machine_tag_name,
            'machine_value' : machine_tag_name + '_' + str(random.choice([x for x in range(params['machine_tag_values_per_machine_tag_names'])]))
            })

    # Generate some fake components
    components = []
    for i in range(params['num_components']):
        component_type = random.choice(params['component_type_options'])
        components.append({
            'component_id' : uuids['components'][i],
            'machine_id' : uuids['machines'][int(i/params['components_per_machine'])],
            'component_name' : random.choice(['input ', 'output ', 'idler ', 'emotional support ']) + component_type,
            'component_type' : component_type,
            'install_date' : fake.date(),
            'replaced_date' : fake.date()
            })

    # Generate some sensors
    sensors = []
    for i in range(params['num_sensors']):
        sensors.append({
            'sensor_id' : uuids['sensors'][i],
            'component_id' : uuids['components'][int(i/params['sensors_per_component'])],
            'sensor_model_id' : random.choice(uuids['sensor_models']),
            'gateway_id' : uuids['gateways'][int(i/params['sensors_per_gateway'])],
            'serial_number' : str(random.random())[-8:]
            })
    
    # Convert all data to be returned into dataframes:
    institutions = pd.DataFrame(institutions)
    users = pd.DataFrame(users)
    sensor_models = pd.DataFrame(sensor_models)
    gateways = pd.DataFrame(gateways)
    machines = pd.DataFrame(machines)
    machine_tags = pd.DataFrame(machine_tags)
    components = pd.DataFrame(components)
    sensors = pd.DataFrame(sensors)
    
    
    tables = {'institutions' : institutions,
              'users' : users,
              'sensor_models' : sensor_models,
              'gateways' : gateways,
              'machines' : machines,
              'machine_tags' : machine_tags,
              'components' : components,
              'sensors' : sensors
              }
    
    return tables, uuids

def get_one_batch(params, meta_tables, nominal_time):
    
    fake = Faker()
    
    # Returns a batch of measurements, measurement_tags, metrics, raw_data
    # based on parameters. Next_ids is used to make sure future batches start
    # where last batch left off in terms of unique ids...
    
    # For every sensor, will generate one row for measurements, and raw_data
    # and some number of rows for metrics, measurement_tags based on parameters
    
    # size of raw data is hardcoded below
    
    sensors = meta_tables['sensors']
    sensor_models = meta_tables['sensor_models']
    
    # Create a dict of sensor_model_ids to be used to make sure measurement
    # type matches the property measured by the associated sensor...
    measurement_types = {}
    for sensor_model in sensor_models.iterrows():
        sensor_model = sensor_model[1].to_dict()
        measurement_types[sensor_model['sensor_model_id']] = sensor_model['property_measured']

    measurements = []
    measurement_tags = []
    metrics = []
    raw_data = []
    
    for sensor in sensors.iterrows():
        
        # Introduce some random variation to the time since sensors would not be perfectly synced...
        current_time = nominal_time + timedelta(seconds=2*(np.random.rand()-0.5))
        
        sensor = sensor[1].to_dict()
        # Measurement
        measurements.append({
            'measurement_id' : fake.uuid4(),
            'sensor_id' : sensor['sensor_id'],
            'mtime' : current_time,
            'mtype' : measurement_types[sensor['sensor_model_id']],
            'battery_level' : 100*random.random()
            })
        
        # Measurement tag
        measurement_tags.append({
            'measurement_tag_id' : fake.uuid4(),
            'measurement_id' : measurements[-1]['measurement_id'],
            'ground_truth' : False,
            'mtag_type' : 'diagnostic',
            'mtag_level' : 'component',
            'mtag_value' : random.choice(['healthy', 'faulty'])
            })
        
        # Raw data
        length_raw_data = 10 # using a very small number here for a test...
        data_json = {'raw' : np.random.rand(length_raw_data).tolist(),
                     'fs' : 45000
                     }
        data_json = json.dumps(data_json)
        
        raw_data.append({
            'raw_data_id' : fake.uuid4(),
            'measurement_id' : measurements[-1]['measurement_id'],
            'mdata' : data_json
            })
        
        # Metrics
        for metric_name in params['metric_names']:
            metrics.append({
                'metric_id' : fake.uuid4(),
                'mtime' : current_time,
                'measurement_id' : measurements[-1]['measurement_id'],
                'metric_name' : metric_name,
                'metric_value' : random.random()            
                })
        
    # Convert all to dataframe
    # measurements = pd.DataFrame(measurements)
    # measurement_tags = pd.DataFrame(measurement_tags)
    # metrics = pd.DataFrame(metrics)
    # raw_data = pd.DataFrame(raw_data)
    
    new_data = {'measurements' : measurements,
                'measurement_tags' : measurement_tags,
                'metrics' : metrics,
                'raw_data' : raw_data}
    
    return new_data

def extend_dict_lists(dict1, dict2):
    # Create an empty dictionary to hold the extended lists
    extended_dict = {}

    # Iterate over the keys in the first dictionary
    for key in dict1.keys():
        # Get the corresponding lists from both dictionaries and concatenate them
        extended_list = dict1[key] + dict2[key]
        
        # Add the extended list to the new dictionary
        extended_dict[key] = extended_list

    return extended_dict

def extend_dict_dfs(dict1, dict2):
    # Create an empty dictionary to hold the extended lists
    extended_dict = {}

    # Iterate over the keys in the first dictionary
    for key in dict1.keys():
        # Get the corresponding lists from both dictionaries and concatenate them
        extended_df = pd.concat([dict1[key], dict2[key]], ignore_index=True)
        
        # Add the extended list to the new dictionary
        extended_dict[key] = extended_df

    return extended_dict

def to_dataframe(tables_dict):
    for table_name, table in tables_dict.items():
        tables_dict[table_name] = pd.DataFrame(tables_dict[table_name])
        
    return tables_dict