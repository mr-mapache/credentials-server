CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS  users (
    pk SERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    user_username VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS passwords (
    pk UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_pk INTEGER NOT NULL,
    password_hash BYTEA NOT NULL,
    password_version INT DEFAULT 1,
    password_is_active BOOLEAN DEFAULT TRUE,
    password_created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), 
    password_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_pk) REFERENCES users(pk) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION bump_passwords_version() RETURNS TRIGGER AS $$
BEGIN
    NEW.password_version = OLD.password_version + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER bump_passwords_version_trigger
BEFORE UPDATE ON passwords
FOR EACH ROW
EXECUTE FUNCTION bump_passwords_version();

CREATE OR REPLACE FUNCTION update_password_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.password_updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_password_updated_at_trigger
BEFORE UPDATE ON passwords
FOR EACH ROW
EXECUTE FUNCTION update_password_updated_at();
 