    --
    -- PostgreSQL database dump
    --
    
    -- Dumped from database version 12.3 (Debian 12.3-1.pgdg100+1)
    -- Dumped by pg_dump version 12.3
    
    SET statement_timeout = 0;
    SET lock_timeout = 0;
    SET idle_in_transaction_session_timeout = 0;
    SET client_encoding = 'UTF8';
    SET standard_conforming_strings = on;
    SELECT pg_catalog.set_config('search_path', '', false);
    SET check_function_bodies = false;
    SET xmloption = content;
    SET client_min_messages = warning;
    SET row_security = off;
    
    --
    -- Name: sensors_ts; Type: DATABASE; Schema: -; Owner: postgres
    --
    
    CREATE DATABASE sensors_ts WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';
    
    
    ALTER DATABASE sensors_ts OWNER TO postgres;
    
    --\connect sensors_ts
    
    SET statement_timeout = 0;
    SET lock_timeout = 0;
    SET idle_in_transaction_session_timeout = 0;
    SET client_encoding = 'UTF8';
    SET standard_conforming_strings = on;
    SELECT pg_catalog.set_config('search_path', '', false);
    SET check_function_bodies = false;
    SET xmloption = content;
    SET client_min_messages = warning;
    SET row_security = off;
    
    SET default_tablespace = '';
    
    SET default_table_access_method = heap;
    
    --
    -- Name: components; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.components (
        component_id uuid NOT NULL,
        machine_id uuid,
        component_name character varying,
        component_type character varying,
        install_date timestamp without time zone,
        replaced_by timestamp without time zone
    );
    
    
    ALTER TABLE public.components OWNER TO postgres;
    
    --
    -- Name: events; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.events (
        external_id uuid NOT NULL,
        external_id_type character varying,
        description character varying,
        mtime timestamp without time zone
    );
    
    
    ALTER TABLE public.events OWNER TO postgres;
    
    --
    -- Name: gateways; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.gateways (
        gateway_id uuid NOT NULL,
        user_id uuid,
        model_number character varying,
        serial_number character varying,
        last_transmission timestamp without time zone
    );
    
    
    ALTER TABLE public.gateways OWNER TO postgres;
    
    --
    -- Name: institutions; Type: TABLE; Schema: public; Owner: postgres
    --
     
    CREATE TABLE public.institutions (
        institution_id uuid NOT NULL,
        administrative_user_id uuid,
        institution_name character varying,
        institution character varying
    );
    
    
    ALTER TABLE public.institutions OWNER TO postgres;
    
    --
    -- Name: labels; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.labels (
        label_id uuid NOT NULL,
        measurement_id uuid,
        is_ground_truth boolean,
        label_type character varying,
        label_value character varying
    );
    
    
    ALTER TABLE public.labels OWNER TO postgres;
    
    --
    -- Name: machine_tags; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.machine_tags (
        machine_tag_id uuid NOT NULL,
        machine_id uuid,
        machine_tag_name character varying,
        machine_tag_value character varying
    );
    
    
    ALTER TABLE public.machine_tags OWNER TO postgres;
    
    --
    -- Name: machines; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.machines (
        machine_id uuid NOT NULL,
        machine_name character varying,
        machine_type character varying,
        last_serviced timestamp without time zone,
        next_service timestamp without time zone
    );
    
    
    ALTER TABLE public.machines OWNER TO postgres;
    
    --
    -- Name: measurement_tags; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.measurement_tags (
        measurement_tag_id uuid NOT NULL,
        measurement_id uuid,
        ground_truth boolean,
        mtag_type character varying,
        mtag_level character varying,
        mtag_value character varying
    );
    
    
    ALTER TABLE public.measurement_tags OWNER TO postgres;
    
    --
    -- Name: measurements; Type: TABLE; Schema: public; Owner: postgres
    --
   
    CREATE TABLE public.measurements (
        measurement_id uuid NOT NULL,
        sensor_id uuid,
        mtime timestamp without time zone,
        mtype character varying,
        battery_level double precision
    );
    
    
    ALTER TABLE public.measurements OWNER TO postgres;
    
    --
    -- Name: metrics; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.metrics (
        metric_id uuid NOT NULL,
        mtime timestamp without time zone NOT NULL,
        measurement_id uuid,
        metric_name character varying,
        metric_value double precision
    );
    
    
    ALTER TABLE public.metrics OWNER TO postgres;
    
    --
    -- Name: raw_data; Type: TABLE; Schema: public; Owner: postgres
    --
   
    CREATE TABLE public.raw_data (
        raw_data_id uuid NOT NULL,
        measurement_id uuid,
        mdata json
    );
    
    
    ALTER TABLE public.raw_data OWNER TO postgres;
    
    --
    -- Name: sensor_models; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.sensor_models (
        sensor_model_id uuid NOT NULL,
        property_measured character varying,
        manufacturer character varying,
        model_number character varying
    );
    
    
    ALTER TABLE public.sensor_models OWNER TO postgres;
    
    --
    -- Name: sensors; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.sensors (
        sensor_id uuid NOT NULL,
        component_id uuid,
        sensor_model_id uuid,
        gateway_id uuid,
        serial_number character varying
    );
    
    
    ALTER TABLE public.sensors OWNER TO postgres;
    
    --
    -- Name: users; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.users (
        user_id uuid NOT NULL,
        institution_id uuid,
        user_email character varying,
        user_password character varying,
        institution character varying
    );
    
    
    ALTER TABLE public.users OWNER TO postgres;
    
    --
    -- Name: components components_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.components
        ADD CONSTRAINT components_pkey PRIMARY KEY (component_id);
    
    
    --
    -- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.events
        ADD CONSTRAINT events_pkey PRIMARY KEY (external_id);
    
    
    --
    -- Name: gateways gateway_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.gateways
        ADD CONSTRAINT gateway_pkey PRIMARY KEY (gateway_id);
    
    
    --
    -- Name: institutions institutions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.institutions
        ADD CONSTRAINT institutions_pkey PRIMARY KEY (institution_id);
    
    
    --
    -- Name: machine_tags machine_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.machine_tags
        ADD CONSTRAINT machine_tags_pkey PRIMARY KEY (machine_tag_id);
    
    
    --
    -- Name: machines machines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.machines
        ADD CONSTRAINT machines_pkey PRIMARY KEY (machine_id);
    
    
    --
    -- Name: measurement_tags measurement_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.measurement_tags
        ADD CONSTRAINT measurement_tags_pkey PRIMARY KEY (measurement_tag_id);
    
    
    --
    -- Name: measurements measurements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.measurements
        ADD CONSTRAINT measurements_pkey PRIMARY KEY (measurement_id);
    
    
    --
    -- Name: metrics metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.metrics
        ADD CONSTRAINT metrics_pkey PRIMARY KEY (metric_id);
    
    
    --
    -- Name: raw_data raw_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.raw_data
        ADD CONSTRAINT raw_data_pkey PRIMARY KEY (raw_data_id);
    
    
    --
    -- Name: sensor_models sensor_model_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.sensor_models
        ADD CONSTRAINT sensor_model_pkey PRIMARY KEY (sensor_model_id);
    
    
    --
    -- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.sensors
        ADD CONSTRAINT sensors_pkey PRIMARY KEY (sensor_id);
    
    
    --
    -- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.users
        ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
    
    
    --
    -- Name: events_date_trunc_idx; Type: INDEX; Schema: public; Owner: postgres
    --
    
    CREATE INDEX events_date_trunc_idx ON public.events USING btree (date_trunc('hour'::text, (mtime + '00:30:00'::interval)));
    
    
    --
    -- Name: measurements_date_trunc_idx; Type: INDEX; Schema: public; Owner: postgres
    --
    
    CREATE INDEX measurements_date_trunc_idx ON public.measurements USING btree (date_trunc('hour'::text, (mtime + '00:30:00'::interval)));
    
    
    --
    -- Name: metrics_date_trunc_idx; Type: INDEX; Schema: public; Owner: postgres
    --
    
    CREATE INDEX metrics_date_trunc_idx ON public.metrics USING btree (date_trunc('hour'::text, (mtime + '00:30:00'::interval)));
    
    CREATE INDEX machines_idx ON public.machines USING btree (machine_id);
    CREATE INDEX components_idx ON public.components USING btree (component_id);
    CREATE INDEX events_idx ON public.events USING btree (external_id);
    CREATE INDEX gateways_idx ON public.gateways USING btree (gateway_id);
    CREATE INDEX institutions_idx ON public.institutions USING btree (institution_id);
    CREATE INDEX labels_idx ON public.labels USING btree (label_id);
    CREATE INDEX machine_tags_idx ON public.machine_tags USING btree (machine_tag_id);
    CREATE INDEX measurement_tags_idx ON public.measurement_tags USING btree (measurement_tag_id);
    CREATE INDEX measurements_idx ON public.measurements USING btree (measurement_id);
    CREATE INDEX metrics_idx ON public.metrics USING btree (metric_id);
    CREATE INDEX raw_data_idx ON public.raw_data USING btree (raw_data_id);
    CREATE INDEX sensor_models_idx ON public.sensor_models USING btree (sensor_model_id);
    CREATE INDEX sensors_idx ON public.sensors USING btree (sensor_id);
    CREATE INDEX users_idx ON public.users USING btree (user_id);
    
    --
    -- PostgreSQL database dump complete
    --
    
