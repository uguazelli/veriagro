DROP TABLE IF EXISTS sensor_data;
DROP TABLE IF EXISTS sensors;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    senha TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    sensor_id TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    nome TEXT,
    tipo TEXT,
    modelo TEXT,
    fabricante TEXT,
    unidade TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL REFERENCES sensors(sensor_id) ON DELETE CASCADE,
    valor REAL NOT NULL,
    unidade TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
