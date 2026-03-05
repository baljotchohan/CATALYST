-- CATALYST Database Seed Data
-- Run AFTER schema.sql to populate the 5 default agents

INSERT INTO agents (id, name, type, description, specialization, status, impact_score) VALUES
(
    uuid_generate_v4(),
    'Weather Advisor',
    'weather',
    'Analyzes live weather patterns across South Asia and generates actionable farming advice for smallholder farmers. Powered by Open-Meteo API and Claude AI.',
    'Agricultural meteorology for India, Pakistan, Bangladesh',
    'idle',
    57.4
),
(
    uuid_generate_v4(),
    'Health Tracker',
    'health',
    'Monitors WHO disease surveillance data and news feeds to detect emerging health threats, generates early-warning alerts for authorities.',
    'Communicable disease surveillance, South Asia',
    'idle',
    34.2
),
(
    uuid_generate_v4(),
    'Education Analyst',
    'education',
    'Identifies schools and regions in South Asia with critical education gaps using UNESCO and World Bank data. Recommends targeted interventions.',
    'Primary education access, literacy improvement',
    'idle',
    22.8
),
(
    uuid_generate_v4(),
    'Farm Advisor',
    'farm',
    'Combines weather forecasts, soil moisture data, and commodity market prices to generate precision farming recommendations and optimal market timing.',
    'Crop rotation, irrigation scheduling, market timing',
    'idle',
    89.1
),
(
    uuid_generate_v4(),
    'Security Analyst',
    'security',
    'Monitors real-time news feeds and public databases to detect security trends, generate threat assessments, and alert relevant authorities.',
    'Regional threat analysis, crime pattern recognition',
    'idle',
    15.6
);
