CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE usernames (
    pk UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL UNIQUE,
    username_created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), 
    username_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE passwords (
    pk UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username_pk UUID NOT NULL REFERENCES usernames(pk),
    password_hash BYTEA NOT NULL,
    password_version INT DEFAULT 1,
    password_is_active BOOLEAN DEFAULT TRUE,
    password_created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), 
    password_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION bump_passwords_version() RETURNS TRIGGER AS $$
BEGIN
    NEW.password_version = OLD.password_version + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bump_passwords_version_trigger
BEFORE UPDATE ON passwords
FOR EACH ROW
EXECUTE FUNCTION bump_passwords_version();

CREATE OR REPLACE FUNCTION update_password_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.password_updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_password_updated_at_trigger
BEFORE UPDATE ON passwords
FOR EACH ROW
EXECUTE FUNCTION update_password_updated_at();

CREATE OR REPLACE FUNCTION update_username_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.username_updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_username_updated_at_trigger
BEFORE UPDATE ON usernames
FOR EACH ROW
EXECUTE FUNCTION update_username_updated_at();