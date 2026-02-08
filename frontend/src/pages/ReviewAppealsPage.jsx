import { useState, useEffect } from 'react';
import { appealsAPI } from '../services/api';
import { CheckCircle2, XCircle, Loader, FileText, AlertTriangle } from 'lucide-react';

export default function ReviewAppealsPage() {
    const [appeals, setAppeals] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedAppeal, setSelectedAppeal] = useState(null);
    const [actionLoading, setActionLoading] = useState(false);
    const [feedback, setFeedback] = useState('');

    useEffect(() => {
        fetchAppeals();
    }, []);

    const fetchAppeals = async () => {
        try {
            const response = await appealsAPI.list({ status_filter: 'draft' });
            setAppeals(response.data);
        } catch (err) {
            console.error('Failed to fetch appeals:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleApprove = async (appealId) => {
        setActionLoading(true);
        try {
            await appealsAPI.approve(appealId, true, null);
            fetchAppeals();
            setSelectedAppeal(null);
        } catch (err) {
            alert('Failed to approve appeal: ' + err.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleReject = async (appealId) => {
        if (!feedback.trim()) {
            alert('Please provide feedback for rejection');
            return;
        }

        setActionLoading(true);
        try {
            await appealsAPI.approve(appealId, false, feedback);
            fetchAppeals();
            setSelectedAppeal(null);
            setFeedback('');
        } catch (err) {
            alert('Failed to reject appeal: ' + err.message);
        } finally {
            setActionLoading(false);
        }
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
                    <h1 className="page-title">Review Appeal Drafts</h1>
                    <p className="page-subtitle">
                        Review AI-generated appeal letters. All appeals require human approval before submission.
                    </p>
                </div>
            </div>

            <div className="container">
                {appeals.length === 0 ? (
                    <div className="card text-center" style={{ padding: '3rem' }}>
                        <FileText size={48} color="var(--color-text-muted)" style={{ margin: '0 auto 1rem' }} />
                        <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                            No Pending Appeals
                        </h3>
                        <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem' }}>
                            Submit a claim to generate an appeal draft for review.
                        </p>
                        <a href="/submit" className="btn btn-primary">Submit Claim</a>
                    </div>
                ) : (
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem' }}>
                        {/* Appeals List */}
                        <div>
                            <div className="card" style={{ padding: '1rem' }}>
                                <h3 style={{ fontWeight: '600', marginBottom: '1rem', padding: '0 0.5rem' }}>
                                    Pending Appeals ({appeals.length})
                                </h3>

                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                    {appeals.map((appeal) => (
                                        <div
                                            key={appeal.id}
                                            onClick={() => setSelectedAppeal(appeal)}
                                            style={{
                                                padding: '1rem',
                                                border: `2px solid ${selectedAppeal?.id === appeal.id ? 'var(--color-primary)' : 'var(--color-border)'}`,
                                                backgroundColor: selectedAppeal?.id === appeal.id ? 'var(--color-primary-light)' : 'var(--color-surface)',
                                                borderRadius: '6px',
                                                cursor: 'pointer',
                                                transition: 'all 0.2s ease'
                                            }}
                                        >
                                            <div style={{ marginBottom: '0.5rem' }}>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginBottom: '0.25rem' }}>
                                                    Appeal ID
                                                </div>
                                                <div style={{ fontFamily: 'monospace', fontSize: '0.875rem', fontWeight: '600' }}>
                                                    {appeal.id}
                                                </div>
                                            </div>

                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                <span className="badge badge-primary">Draft</span>
                                                {appeal.compliance_issues && appeal.compliance_issues.length > 0 && (
                                                    <span className="badge badge-warning">
                                                        <AlertTriangle size={12} style={{ display: 'inline', marginRight: '0.25rem' }} />
                                                        {appeal.compliance_issues.length}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Appeal Detail */}
                        {selectedAppeal ? (
                            <div>
                                <div className="card">
                                    <h3 className="card-header">Appeal Draft Review</h3>

                                    <div className="form-group">
                                        <label className="form-label">Draft Text</label>
                                        <div style={{
                                            backgroundColor: 'var(--color-background)',
                                            border: '1px solid var(--color-border)',
                                            borderRadius: '6px',
                                            padding: '1.5rem',
                                            maxHeight: '400px',
                                            overflowY: 'auto'
                                        }}>
                                            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', fontFamily: 'Georgia, serif', fontSize: '0.9375rem', lineHeight: '1.7' }}>
                                                {selectedAppeal.draft_text}
                                            </pre>
                                        </div>
                                    </div>

                                    {selectedAppeal.policy_citations && selectedAppeal.policy_citations.length > 0 && (
                                        <div className="form-group">
                                            <label className="form-label">Policy Citations</label>
                                            <div className="alert alert-info" style={{ marginBottom: 0 }}>
                                                <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
                                                    {selectedAppeal.policy_citations.map((citation, idx) => (
                                                        <li key={idx} style={{ marginBottom: '0.5rem' }}>{citation}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </div>
                                    )}

                                    {selectedAppeal.compliance_issues && selectedAppeal.compliance_issues.length > 0 && (
                                        <div className="form-group">
                                            <label className="form-label">
                                                <AlertTriangle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
                                                Compliance Issues
                                            </label>
                                            <div className="alert" style={{ backgroundColor: '#FEF3C7', borderColor: '#D97706', color: '#92400E', marginBottom: 0 }}>
                                                <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
                                                    {selectedAppeal.compliance_issues.map((issue, idx) => (
                                                        <li key={idx} style={{ marginBottom: '0.5rem', fontWeight: '500' }}>{issue}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </div>
                                    )}

                                    <div className="form-group">
                                        <label className="form-label">Rejection Feedback (Optional)</label>
                                        <textarea
                                            value={feedback}
                                            onChange={(e) => setFeedback(e.target.value)}
                                            rows={3}
                                            className="form-textarea"
                                            placeholder="Provide feedback if requesting revision..."
                                        />
                                    </div>

                                    <div style={{ display: 'flex', gap: '1rem', borderTop: '1px solid var(--color-border)', paddingTop: '1.5rem' }}>
                                        <button
                                            onClick={() => handleApprove(selectedAppeal.id)}
                                            disabled={actionLoading}
                                            className="btn btn-success"
                                            style={{ flex: 1 }}
                                        >
                                            {actionLoading ? (
                                                <Loader size={20} style={{ animation: 'spin 1s linear infinite' }} />
                                            ) : (
                                                <>
                                                    <CheckCircle2 size={20} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'middle' }} />
                                                    Approve & Submit
                                                </>
                                            )}
                                        </button>

                                        <button
                                            onClick={() => handleReject(selectedAppeal.id)}
                                            disabled={actionLoading}
                                            className="btn btn-secondary"
                                            style={{ flex: 1 }}
                                        >
                                            <XCircle size={20} style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'middle' }} />
                                            Request Revision
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
                                <div style={{ textAlign: 'center' }}>
                                    <FileText size={48} color="var(--color-text-muted)" style={{ margin: '0 auto 1rem' }} />
                                    <p style={{ color: 'var(--color-text-secondary)' }}>
                                        Select an appeal from the list to review
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
