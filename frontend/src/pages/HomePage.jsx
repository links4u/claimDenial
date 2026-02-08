import { Shield, Clock, DollarSign, Users, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function HomePage() {
    return (
        <div>
            {/* Hero Section */}
            <div className="page-header">
                <div className="container">
                    <h1 className="page-title">ClaimPilot™ AI-Powered Appeal Automation</h1>
                    <p className="page-subtitle">
                        Transform denial-to-appeal workflows with intelligent automation.
                        Reduce processing time by 95%, lower costs by 98%, and maintain full regulatory compliance.
                    </p>
                    <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
                        <Link to="/submit" className="btn btn-primary">
                            Submit Claim
                        </Link>
                        <Link to="/appeals" className="btn btn-secondary">
                            Review Appeals
                        </Link>
                    </div>
                </div>
            </div>

            <div className="container">
                {/* KPI Cards */}
                <div className="grid grid-cols-4 mb-5">
                    <div className="kpi-card">
                        <Clock size={40} color="#0066CC" style={{ margin: '0 auto 0.5rem' }} />
                        <div className="kpi-value">&lt; 15s</div>
                        <div className="kpi-label">Avg Processing Time</div>
                        <p className="text-muted" style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
                            vs. 5-7 days manual
                        </p>
                    </div>

                    <div className="kpi-card">
                        <DollarSign size={40} color="#0066CC" style={{ margin: '0 auto 0.5rem' }} />
                        <div className="kpi-value">$0.013</div>
                        <div className="kpi-label">Cost Per Appeal</div>
                        <p className="text-muted" style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
                            vs. $25-50 manual
                        </p>
                    </div>

                    <div className="kpi-card">
                        <Users size={40} color="#0066CC" style={{ margin: '0 auto 0.5rem' }} />
                        <div className="kpi-value">6</div>
                        <div className="kpi-label">Specialized AI Agents</div>
                        <p className="text-muted" style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
                            Claude Sonnet 3.5
                        </p>
                    </div>

                    <div className="kpi-card">
                        <Shield size={40} color="#059669" style={{ margin: '0 auto 0.5rem' }} />
                        <div className="kpi-value" style={{ color: '#059669' }}>100%</div>
                        <div className="kpi-label">Human-in-the-Loop</div>
                        <p className="text-muted" style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
                            Full compliance mode
                        </p>
                    </div>
                </div>

                {/* How It Works */}
                <div className="card mb-5">
                    <h2 className="card-header">How ClaimPilot Works</h2>
                    <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem' }}>
                        A 6-agent AI workflow that automates appeal generation while maintaining full human oversight and regulatory compliance.
                    </p>

                    <div className="grid grid-cols-2" style={{ gap: '1.5rem' }}>
                        {/* Step 1 */}
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <div style={{
                                flexShrink: 0,
                                width: '48px',
                                height: '48px',
                                backgroundColor: 'var(--color-primary-light)',
                                color: 'var(--color-primary)',
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontWeight: '700',
                                fontSize: '1.25rem'
                            }}>
                                1
                            </div>
                            <div>
                                <h3 style={{ fontWeight: '600', marginBottom: '0.25rem', color: 'var(--color-text-primary)' }}>
                                    Intake & Classification
                                </h3>
                                <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.5' }}>
                                    IntentRouter validates claim data. DenialClassifier categorizes denial type
                                    (Coverage, Medical Necessity, Coding, Authorization) using Claude Sonnet.
                                </p>
                            </div>
                        </div>

                        {/* Step 2 */}
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <div style={{
                                flexShrink: 0,
                                width: '48px',
                                height: '48px',
                                backgroundColor: 'var(--color-primary-light)',
                                color: 'var(--color-primary)',
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontWeight: '700',
                                fontSize: '1.25rem'
                            }}>
                                2
                            </div>
                            <div>
                                <h3 style={{ fontWeight: '600', marginBottom: '0.25rem', color: 'var(--color-text-primary)' }}>
                                    Policy Retrieval (RAG)
                                </h3>
                                <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.5' }}>
                                    PolicyRetrieval agent performs semantic search across 1,200+ payer policy documents
                                    using pgvector embeddings to find relevant coverage excerpts.
                                </p>
                            </div>
                        </div>

                        {/* Step 3 */}
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <div style={{
                                flexShrink: 0,
                                width: '48px',
                                height: '48px',
                                backgroundColor: 'var(--color-primary-light)',
                                color: 'var(--color-primary)',
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontWeight: '700',
                                fontSize: '1.25rem'
                            }}>
                                3
                            </div>
                            <div>
                                <h3 style={{ fontWeight: '600', marginBottom: '0.25rem', color: 'var(--color-text-primary)' }}>
                                    Appeal Drafting & Validation
                                </h3>
                                <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.5' }}>
                                    AppealDrafting generates formal appeal letter with policy citations.
                                    ComplianceGuardrail validates tone, citations, and regulatory requirements.
                                </p>
                            </div>
                        </div>

                        {/* Step 4 */}
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <div style={{
                                flexShrink: 0,
                                width: '48px',
                                height: '48px',
                                backgroundColor: '#E6F7F5',
                                color: '#00A896',
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontWeight: '700',
                                fontSize: '1.25rem'
                            }}>
                                4
                            </div>
                            <div>
                                <h3 style={{ fontWeight: '600', marginBottom: '0.25rem', color: 'var(--color-text-primary)' }}>
                                    Human Review & Approval
                                </h3>
                                <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.5' }}>
                                    All appeals require explicit human approval before submission.
                                    Reviewers can approve, reject, or request AI revision with feedback.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Technology Stack */}
                <div className="card mb-5">
                    <h2 className="card-header">Technology Architecture</h2>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
                        <div>
                            <h4 style={{ fontWeight: '600', fontSize: '0.875rem', color: 'var(--color-text-primary)', marginBottom: '0.5rem' }}>
                                AI & LLM
                            </h4>
                            <ul style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.8', paddingLeft: '1.25rem' }}>
                                <li>Claude Sonnet 3.5 (Anthropic)</li>
                                <li>LangGraph multi-agent orchestration</li>
                                <li>Structured output validation</li>
                            </ul>
                        </div>

                        <div>
                            <h4 style={{ fontWeight: '600', fontSize: '0.875rem', color: 'var(--color-text-primary)', marginBottom: '0.5rem' }}>
                                Data & Retrieval
                            </h4>
                            <ul style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.8', paddingLeft: '1.25rem' }}>
                                <li>PostgreSQL with pgvector</li>
                                <li>RAG semantic search</li>
                                <li>1,200+ policy document corpus</li>
                            </ul>
                        </div>

                        <div>
                            <h4 style={{ fontWeight: '600', fontSize: '0.875rem', color: 'var(--color-text-primary)', marginBottom: '0.5rem' }}>
                                Compliance & Audit
                            </h4>
                            <ul style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.8', paddingLeft: '1.25rem' }}>
                                <li>HIPAA-compliant audit logging</li>
                                <li>Full execution traceability</li>
                                <li>Human-in-the-loop approval</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* Enterprise Features */}
                <div className="grid grid-cols-3 mb-5">
                    <div className="card">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                            <CheckCircle2 size={24} color="#0066CC" />
                            <h3 style={{ fontWeight: '600', fontSize: '1rem', margin: 0 }}>Scalable Architecture</h3>
                        </div>
                        <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.6' }}>
                            Containerized deployment with Docker. Supports horizontal scaling for high-volume processing.
                        </p>
                    </div>

                    <div className="card">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                            <CheckCircle2 size={24} color="#0066CC" />
                            <h3 style={{ fontWeight: '600', fontSize: '1rem', margin: 0 }}>Regulatory Compliance</h3>
                        </div>
                        <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.6' }}>
                            Built-in compliance guardrails. Complete audit trails for HIPAA, SOC 2, and regulatory review.
                        </p>
                    </div>

                    <div className="card">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                            <CheckCircle2 size={24} color="#0066CC" />
                            <h3 style={{ fontWeight: '600', fontSize: '1rem', margin: 0 }}>Enterprise Integration</h3>
                        </div>
                        <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', lineHeight: '1.6' }}>
                            RESTful APIs for EHR/RCM integration. Supports batch processing and webhook notifications.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
