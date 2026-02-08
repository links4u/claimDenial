import { useState, useEffect } from 'react';
import { auditAPI } from '../services/api';
import { Loader, Shield, ChevronDown, ChevronUp } from 'lucide-react';

export default function AuditLogPage() {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [expandedLog, setExpandedLog] = useState(null);
    const [agents, setAgents] = useState([]);
    const [selectedAgent, setSelectedAgent] = useState('');

    useEffect(() => {
        fetchLogs();
        fetchAgents();
    }, [selectedAgent]);

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const response = await auditAPI.list({
                agent_name: selectedAgent || undefined,
                limit: 50
            });
            const logsData = Array.isArray(response.data) ? response.data : [];
            setLogs(logsData);
        } catch (err) {
            console.error('Failed to fetch audit logs:', err);
            setLogs([]);
        } finally {
            setLoading(false);
        }
    };

    const fetchAgents = async () => {
        try {
            const response = await auditAPI.listAgents();
            const agentsData = Array.isArray(response.data) ? response.data : [];
            setAgents(agentsData);
        } catch (err) {
            console.error('Failed to fetch agents:', err);
            setAgents([]);
        }
    };

    const toggleExpand = (logId) => {
        setExpandedLog(expandedLog === logId ? null : logId);
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
                <Loader size={32} color="var(--color-primary)" style={{ animation: 'spin 1s linear infinite' }} />
            </div>
        );
    }

    return (
        <div>
            <div className="page-header">
                <div className="container">
                    <h1 className="page-title">Audit Log</h1>
                    <p className="page-subtitle">
                        Complete execution trace of all agent activities for compliance, debugging, and system monitoring.
                    </p>
                </div>
            </div>

            <div className="container">
                {/* Filter */}
                <div className="card mb-4" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h3 style={{ fontWeight: '600', marginBottom: '0.25rem' }}>Filter Audit Events</h3>
                        <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', margin: 0 }}>
                            View execution logs by agent type
                        </p>
                    </div>
                    <select
                        value={selectedAgent}
                        onChange={(e) => setSelectedAgent(e.target.value)}
                        className="form-select"
                        style={{ width: '300px' }}
                    >
                        <option value="">All Agents ({logs.length} events)</option>
                        {agents.map((agent) => (
                            <option key={agent.id || agent.name} value={agent.name}>
                                {agent.name}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Logs */}
                <div className="card">
                    {logs.length === 0 ? (
                        <div className="text-center" style={{ padding: '3rem' }}>
                            <Shield size={48} color="var(--color-text-muted)" style={{ margin: '0 auto 1rem' }} />
                            <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                                No Audit Logs
                            </h3>
                            <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem' }}>
                                Process a claim to generate audit trails.
                            </p>
                            <a href="/submit" className="btn btn-primary">Submit Claim</a>
                        </div>
                    ) : (
                        <div>
                            <h3 className="card-header">Execution Timeline</h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                {logs.map((log) => (
                                    <div key={log.id} style={{ border: '1px solid var(--color-border)', borderRadius: '6px', overflow: 'hidden' }}>
                                        <div
                                            onClick={() => toggleExpand(log.id)}
                                            style={{
                                                padding: '1rem',
                                                backgroundColor: 'var(--color-surface)',
                                                cursor: 'pointer',
                                                display: 'flex',
                                                justifyContent: 'space-between',
                                                alignItems: 'center',
                                                transition: 'background-color 0.2s ease'
                                            }}
                                            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--color-background)'}
                                            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--color-surface)'}
                                        >
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1 }}>
                                                <span className="badge badge-primary">
                                                    {log.agent?.replace('Agent', '') || 'System'}
                                                </span>
                                                <div>
                                                    <div style={{ fontWeight: '500', marginBottom: '0.25rem' }}>
                                                        {log.action || 'Execution'}
                                                    </div>
                                                    <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                                        {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'Unknown time'}
                                                    </div>
                                                </div>
                                            </div>

                                            {expandedLog === log.id ? (
                                                <ChevronUp size={20} color="var(--color-text-muted)" />
                                            ) : (
                                                <ChevronDown size={20} color="var(--color-text-muted)" />
                                            )}
                                        </div>

                                        {expandedLog === log.id && (
                                            <div style={{ padding: '1rem', backgroundColor: 'var(--color-background)', borderTop: '1px solid var(--color-border)' }}>
                                                {log.input_data && (
                                                    <div style={{ marginBottom: '1rem' }}>
                                                        <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                                                            Input Data
                                                        </div>
                                                        <pre style={{
                                                            backgroundColor: 'var(--color-surface)',
                                                            border: '1px solid var(--color-border)',
                                                            borderRadius: '4px',
                                                            padding: '0.75rem',
                                                            fontSize: '0.75rem',
                                                            overflow: 'auto',
                                                            margin: 0
                                                        }}>
                                                            {JSON.stringify(log.input_data, null, 2)}
                                                        </pre>
                                                    </div>
                                                )}

                                                {log.output_data && (
                                                    <div style={{ marginBottom: '1rem' }}>
                                                        <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                                                            Output Data
                                                        </div>
                                                        <pre style={{
                                                            backgroundColor: 'var(--color-surface)',
                                                            border: '1px solid var(--color-border)',
                                                            borderRadius: '4px',
                                                            padding: '0.75rem',
                                                            fontSize: '0.75rem',
                                                            overflow: 'auto',
                                                            margin: 0
                                                        }}>
                                                            {JSON.stringify(log.output_data, null, 2)}
                                                        </pre>
                                                    </div>
                                                )}

                                                {log.metadata && (
                                                    <div>
                                                        <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                                                            Metadata
                                                        </div>
                                                        <pre style={{
                                                            backgroundColor: 'var(--color-surface)',
                                                            border: '1px solid var(--color-border)',
                                                            borderRadius: '4px',
                                                            padding: '0.75rem',
                                                            fontSize: '0.75rem',
                                                            overflow: 'auto',
                                                            margin: 0
                                                        }}>
                                                            {JSON.stringify(log.metadata, null, 2)}
                                                        </pre>
                                                    </div>
                                                )}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Compliance Notice */}
                <div className="alert alert-info mt-4">
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <Shield size={24} style={{ flexShrink: 0 }} />
                        <div>
                            <h4 style={{ fontWeight: '600', marginBottom: '0.5rem' }}>HIPAA Compliance & Audit Trail</h4>
                            <p style={{ margin: 0 }}>
                                Every agent execution is logged with complete input, output, and metadata for full traceability.
                                This ensures regulatory compliance (HIPAA, SOC 2) and enables comprehensive debugging of agent decisions.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
