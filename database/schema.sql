-- CATALYST PostgreSQL Schema
-- Run this on your Supabase database to create all required tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    github_username VARCHAR(255) UNIQUE,
    avatar_url VARCHAR(500),
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agents table
CREATE TYPE agent_type AS ENUM ('weather', 'health', 'education', 'farm', 'security');
CREATE TYPE agent_status AS ENUM ('active', 'idle', 'running', 'error');

CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type agent_type NOT NULL,
    description TEXT NOT NULL,
    specialization TEXT,
    github_url VARCHAR(500),
    created_by VARCHAR(255),
    status agent_status DEFAULT 'idle',
    impact_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Research logs table
CREATE TABLE IF NOT EXISTS research_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    data_input JSONB,
    result TEXT,
    insights JSONB,
    impact_metric FLOAT DEFAULT 0.0,
    impact_description VARCHAR(500),
    status VARCHAR(50) DEFAULT 'completed',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent data sources table
CREATE TABLE IF NOT EXISTS agent_data_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    data_source_type VARCHAR(100) NOT NULL,
    api_endpoint VARCHAR(500),
    description VARCHAR(255)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(type);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_research_logs_agent_id ON research_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_research_logs_timestamp ON research_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_agent_data_sources_agent_id ON agent_data_sources(agent_id);

-- Auto-update updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
