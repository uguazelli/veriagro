-- ===============================
-- 🧨 DROP ALL (correct dependency order)
-- ===============================
DROP TABLE IF EXISTS alerts;
DROP TABLE IF EXISTS mqtt_topics;
DROP TABLE IF EXISTS mqtt_credentials;
DROP TABLE IF EXISTS sensor_data;
DROP TABLE IF EXISTS sensors;
DROP TABLE IF EXISTS sensor_models;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS company_memberships;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS companies;

-- ===============================
-- 🏢 COMPANIES (Tenants)
-- ===============================
CREATE TABLE companies (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ===============================
-- 👤 USERS (With company membership)
-- ===============================
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ===============================
-- 🔗 COMPANY MEMBERSHIPS (User ↔ Company)
-- ===============================
CREATE TABLE company_memberships (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    role TEXT CHECK (role IN ('admin', 'manager', 'viewer')) NOT NULL DEFAULT 'viewer',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    UNIQUE (user_id, company_id)
);

-- ===============================
-- 📟 DEVICES (Now belong to companies)
-- ===============================
CREATE TABLE devices (
    id UUID PRIMARY KEY,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    model TEXT,
    serial_number TEXT UNIQUE,
    location TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    last_seen TIMESTAMP WITHOUT TIME ZONE,
    registered_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ===============================
-- 🔐 MQTT CREDENTIALS
-- ===============================
CREATE TABLE mqtt_credentials (
    id UUID PRIMARY KEY,
    device_id UUID NOT NULL UNIQUE REFERENCES devices(id) ON DELETE CASCADE,
    mqtt_username TEXT UNIQUE NOT NULL,
    mqtt_password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ===============================
-- 📡 MQTT TOPICS
-- ===============================
CREATE TABLE mqtt_topics (
    id UUID PRIMARY KEY,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    direction TEXT CHECK (direction IN ('publish', 'subscribe')) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ===============================
-- 🧬 SENSOR MODELS (optional normalization)
-- ===============================
CREATE TABLE sensor_models (
    id UUID PRIMARY KEY,
    type TEXT NOT NULL,
    model TEXT NOT NULL,
    manufacturer TEXT,
    unit TEXT
);

-- ===============================
-- 🧪 SENSORS
-- ===============================
CREATE TABLE sensors (
    id UUID PRIMARY KEY,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    name TEXT,
    type TEXT,
    model TEXT,
    manufacturer TEXT,
    model_id UUID REFERENCES sensor_models(id),
    config JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- ===============================
-- 📈 SENSOR DATA
-- ===============================
CREATE TABLE sensor_data (
    id UUID PRIMARY KEY,
    sensor_id UUID NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    unit TEXT,
    value REAL NOT NULL,
    status TEXT, -- e.g., 'normal', 'warning', 'critical'
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 📊 Performance Index
CREATE INDEX idx_sensor_data_sensor_id_timestamp ON sensor_data(sensor_id, timestamp);

-- ===============================
-- 🚨 ALERTS
-- ===============================
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    sensor_id UUID NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    value REAL,
    level TEXT CHECK (level IN ('info', 'warning', 'critical')),
    message TEXT,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
