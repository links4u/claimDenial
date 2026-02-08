-- ClaimPilot™ Database Initialization
-- PostgreSQL with pgvector extension

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for development only)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS appeals CASCADE;
DROP TABLE IF EXISTS policies CASCADE;
DROP TABLE IF EXISTS claims CASCADE;

-- =====================================================
-- TABLE: claims
-- =====================================================
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id VARCHAR(100) UNIQUE NOT NULL,
    denial_code VARCHAR(50) NOT NULL,
    denial_description TEXT NOT NULL,
    payer_name VARCHAR(200) NOT NULL,
    policy_text TEXT,
    category VARCHAR(50), -- Coverage, Medical Necessity, Coding, Authorization, Other
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_claims_claim_id ON claims(claim_id);
CREATE INDEX idx_claims_payer_name ON claims(payer_name);
CREATE INDEX idx_claims_category ON claims(category);
CREATE INDEX idx_claims_created_at ON claims(created_at);

-- =====================================================
-- TABLE: policies
-- =====================================================
CREATE TABLE policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payer_name VARCHAR(200) NOT NULL,
    section_title VARCHAR(500) NOT NULL,
    section_text TEXT NOT NULL,
    embedding vector(1536), -- OpenAI text-embedding-3-small dimension
    metadata JSONB, -- Additional metadata (version, effective_date, etc.)
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_policies_payer_name ON policies(payer_name);
CREATE INDEX idx_policies_embedding ON policies USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- =====================================================
-- TABLE: appeals
-- =====================================================
CREATE TABLE appeals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    draft_text TEXT NOT NULL,
    policy_citations JSONB, -- Array of policy IDs referenced
    status VARCHAR(50) DEFAULT 'draft', -- draft, approved, rejected, submitted
    approved BOOLEAN DEFAULT FALSE,
    user_feedback TEXT,
    compliance_issues JSONB, -- List of compliance issues if any
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    submitted_at TIMESTAMP,
    version INTEGER DEFAULT 1 -- For appeal versioning
);

CREATE INDEX idx_appeals_claim_id ON appeals(claim_id);
CREATE INDEX idx_appeals_status ON appeals(status);
CREATE INDEX idx_appeals_created_at ON appeals(created_at);

-- =====================================================
-- TABLE: audit_logs
-- =====================================================
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
    appeal_id UUID REFERENCES appeals(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    metadata JSONB, -- reasoning, token_count, latency_ms, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_claim_id ON audit_logs(claim_id);
CREATE INDEX idx_audit_logs_agent_name ON audit_logs(agent_name);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- =====================================================
-- TRIGGERS: Updated timestamp
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_claims_updated_at BEFORE UPDATE ON claims
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VIEWS: Useful queries
-- =====================================================

-- View: Appeals with claim details
CREATE OR REPLACE VIEW v_appeals_with_claims AS
SELECT 
    a.id AS appeal_id,
    a.draft_text,
    a.status,
    a.approved,
    a.created_at AS appeal_created_at,
    c.claim_id,
    c.denial_code,
    c.denial_description,
    c.payer_name,
    c.category
FROM appeals a
JOIN claims c ON a.claim_id = c.id;

-- View: Audit trail by claim
CREATE OR REPLACE VIEW v_audit_trail AS
SELECT 
    al.created_at,
    c.claim_id,
    al.agent_name,
    al.input_data,
    al.output_data,
    al.metadata
FROM audit_logs al
JOIN claims c ON al.claim_id = c.id
ORDER BY al.created_at DESC;

-- =====================================================
-- GRANTS (for application user)
-- =====================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO claimpilot;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO claimpilot;
