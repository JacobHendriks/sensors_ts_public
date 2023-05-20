Demo code for Structured Data Ontology for AI in Industrial Asset Condition
Monitoring

This can be used to see how results were obtained as well as for reference in creating similar databases.

Requires PostgreSQL - see instructions for running PostgreSQL in Docker here:
https://hub.docker.com/_/postgres

Use sensors_ts_db_creation_script.sql to create schema in database 'sensors_ts' database before running python files.

Summpary of each file in this repo:

run_benchmark.py

The this will populate the DB with generated data according to parameters
defined in the beginning of the script. It reads querys fromeasurement_queries
measurement_queries.sql, executes each of them, and records the result to
results.csv. Results for each query include execution time, rows affected, and number of measurement records in DB.

benchmark_utils.py

Contains utilities used by run_benchmark.py, most notably creating randomly
generated to populate the DB.

db_utils

C0ntains utilities for run_benchmark.py. The connection string used to connect
to the DB is stored here. 

ERD.drawio

A diagram file (read using draw.io) for the entity relation diagram of the DB.

measurement_queries.sql

Contains the queries that will be run in sequence during benchmarking. Queries are seperated by characters:
/*/////*/
Queries that return SQL errors or don't return data won't have their results logged.

results.csv
Results from running benchmark with columns:
query_number	measurements_count	rows_affected	execution_time

results_plots.ipynb

A notebook for viewing and graphing data in results.csv

sensors_ts_db_creation_script.sql

SQL code for creating the database.