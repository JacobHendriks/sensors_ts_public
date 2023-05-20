
/*
Q0:

Find all raw data and timestamps related to machine X, sort by most recent

*/
SELECT mc.machine_name
	, m.mtime
	, r.mdata
	, s.sensor_id
FROM raw_data r
	JOIN measurements m ON r.measurement_id = m.measurement_id
	JOIN sensors s ON s.sensor_id=m.sensor_id
	JOIN components c ON c.component_id = s.component_id
	JOIN machines mc ON mc.machine_id = c.machine_id
		AND mc.machine_name = 'Lucas''s gearbox'

/*/////*/
/*
Q1:

Find raw data with time stamps related to component X 
if the related metric Y was over a certain value

*/
SELECT c.component_name
	, m.mtime
	, r.mdata
FROM raw_data r
	JOIN measurements m ON m.measurement_id = r.measurement_id
	JOIN metrics mt ON mt.measurement_id = m.measurement_id
		AND metric_name = 'rms'
		AND metric_value >= 0.975
	JOIN sensors s ON s.sensor_id=m.sensor_id
	JOIN components c ON c.component_id = s.component_id
		AND c.component_name = 'input shaft'
		
/*/////*/
/*
Q2:

Find metric X related to machine Y if 
the measurement timestamp is close to noon and the measurement has tag “running”
 
*/
SELECT mc.machine_name
	, m.mtime
	, mt.metric_name
	, mt.metric_value
FROM raw_data r
	JOIN measurements m ON m.measurement_id = r.measurement_id
		AND m.mtime::time between '11:58' and '12:07'
	JOIN measurement_tags mtg ON mtg.measurement_id = m.measurement_id
		AND mtg.mtag_value = 'faulty'  
	JOIN metrics mt ON mt.measurement_id = m.measurement_id
		AND metric_name = 'rms'
	JOIN sensors s ON s.sensor_id=m.sensor_id
	JOIN components c ON c.component_id = s.component_id
	JOIN machines mc ON mc.machine_id = c.machine_id
		AND mc.machine_name = 'Lucas''s gearbox'

/*/////*/
/*
Q3:

Create rows in measurement tag table with key X, value Y, and machine ID Z, for all machines 
owned by user P created after time T

*/
INSERT INTO measurement_tags
(SELECT gen_random_uuid() AS measurement_tag_id
	, m.measurement_id
	, 1=1 AS ground_truth
	, 'diagnostic' AS measurement_tag_type 
	, 'component' AS measuerement_tag_level
	, 'faulty' AS measurement_tag_value
FROM machines mc
	JOIN components c ON c.machine_id = mc.machine_id
	JOIN sensors s ON s.component_id = c.component_id
	JOIN measurements m ON m.sensor_id = s.sensor_id
		AND m.mtime::time > '2000-01-21 00:00:00'
	JOIN gateways gw ON gw.gateway_id = s.gateway_id
	JOIN users u ON u.user_id = gw.user_id
		AND user_email = 'gking@scott-medina.biz'
WHERE mc.machine_id = '6c834752-35a7-4fc0-81fb-be93a08b84f3')
RETURNING *

/*/////*/
/*
Q4:

Delete raw data, measurements, and metrics related to user X

*/
DELETE FROM raw_data r
USING measurements m 
	JOIN sensors s ON s.sensor_id=m.sensor_id
	JOIN gateways gw ON gw.gateway_id = s.gateway_id
	JOIN users u ON u.user_id = gw.user_id
WHERE r.measurement_id = m.measurement_id
	AND u.user_email = 'egriffith@gonzalez.com'
RETURNING *