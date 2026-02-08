import { useState } from 'react';
import { claimsAPI } from '../services/api';
import { Loader, AlertCircle, CheckCircle2, Send } from 'lucide-react';

export default function SubmitClaimPage() {
    const [formData, setFormData] = useState({
        claim_id: '',
        denial_code: '',
        denial_description: '',
        payer_name: '',
        policy_text: '',
    });

    const [loading, setLoading] = useState(false);
    const [processing, setProcessing] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const claimResponse = await claimsAPI.create(formData);
            console.log('Claim created:', claimResponse.data);

            setProcessing(true);
            const workflowResponse = await claimsAPI.process(formData.claim_id);

            setResult(workflowResponse.data);
            setProcessing(false);

            setFormData({
                claim_id: '',
                denial_code: '',
                denial_description: '',
                payer_name: '',
                policy_text: '',
            });
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'An error occurred');
            setProcessing(false);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="page-header">
                <div className="container">
                    <h1 className="page-title">Submit Claim for Appeal</h1>
                    <p className="page-subtitle">
                        Enter claim denial details. The 6-agent AI workflow will classify the denial,
                        retrieve relevant policies, and generate a compliant appeal draft.
                    </p>
                </div>
            </div>

            <div className="container">
                <form onSubmit={handleSubmit} className="card" style={{ maxWidth: '900px', margin: '0 auto' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem' }}>
                        <div className="form-group">
                            <label className="form-label">Claim ID *</label>
                            <input
                                type="text"
                                name="claim_id"
                                value={formData.claim_id}
                                onChange={handleChange}
                                required
                                className="form-input"
                                placeholder="CLM-2024-001"
                            />
                            <div className="form-help">Unique identifier for this claim</div>
                        </div>

                        <div className="form-group">
                            <label className="form-label">Denial Code *</label>
                            <input
                                type="text"
                                name="denial_code"
                                value={formData.denial_code}
                                onChange={handleChange}
                                required
                                className="form-input"
                                placeholder="CO-197"
                            />
                            <div className="form-help">CARC/RARC denial code</div>
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Payer Name *</label>
                        <input
                            type="text"
                            name="payer_name"
                            value={formData.payer_name}
                            onChange={handleChange}
                            required
                            className="form-input"
                            placeholder="Blue Cross Blue Shield"
                        />
                        <div className="form-help">Insurance payer organization</div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Denial Description *</label>
                        <textarea
                            name="denial_description"
                            value={formData.denial_description}
                            onChange={handleChange}
                            required
                            className="form-textarea"
                            rows={5}
                            placeholder="Precertification/authorization/notification absent. Service not authorized or pre-certified by the payer..."
                        />
                        <div className="form-help">Detailed explanation of the denial reason</div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Policy Text (Optional)</label>
                        <textarea
                            name="policy_text"
                            value={formData.policy_text}
                            onChange={handleChange}
                            className="form-textarea"
                            rows={4}
                            placeholder="Section 5.2: All specialist consultations require prior authorization within 48 hours..."
                        />
                        <div className="form-help">Relevant policy excerpts (if available)</div>
                    </div>

                    <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: '1.5rem', marginTop: '1rem' }}>
                        <button
                            type="submit"
                            disabled={loading}
                            className="btn btn-primary"
                            style={{ width: '100%', padding: '1rem', fontSize: '1rem' }}
                        >
                            {loading ? (
                                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                                    <Loader size={20} style={{ animation: 'spin 1s linear infinite' }} />
                                    {processing ? 'Processing through AI workflow...' : 'Submitting claim...'}
                                </span>
                            ) : (
                                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                                    <Send size={20} />
                                    Submit & Process Claim
                                </span>
                            )}
                        </button>
                        {!loading && (
                            <div style={{ textAlign: 'center', marginTop: '0.75rem', fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                                Processing typically takes 8-15 seconds
                            </div>
                        )}
                    </div>
                </form>

                {error && (
                    <div className="alert alert-error" style={{ maxWidth: '900px', margin: '1.5rem auto 0' }}>
                        <div style={{ display: 'flex', alignItems: 'start', gap: '0.75rem' }}>
                            <AlertCircle size={20} style={{ flexShrink: 0 }} />
                            <div>
                                <h4 style={{ fontWeight: '600', marginBottom: '0.25rem' }}>Submission Error</h4>
                                <p>{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                {result && (
                    <div style={{ maxWidth: '900px', margin: '1.5rem auto 0' }}>
                        <div className="alert alert-success">
                            <div style={{ display: 'flex', alignItems: 'start', gap: '0.75rem' }}>
                                <CheckCircle2 size={24} style={{ flexShrink: 0 }} />
                                <div>
                                    <h4 style={{ fontWeight: '600', marginBottom: '0.25rem', fontSize: '1.125rem' }}>
                                        Appeal Generated Successfully
                                    </h4>
                                    <p>Your claim has been processed through the AI workflow. Review the draft in the Appeals dashboard.</p>
                                </div>
                            </div>
                        </div>

                        <div className="card mt-4">
                            <h3 className="card-header">Appeal Draft Preview</h3>

                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '0.5rem' }}>
                                    Appeal ID
                                </label>
                                <div style={{ fontFamily: 'monospace', fontSize: '1rem', fontWeight: '600', color: 'var(--color-primary)' }}>
                                    {result.appeal_id}
                                </div>
                            </div>

                            <div style={{
                                backgroundColor: 'var(--color-background)',
                                border: '1px solid var(--color-border)',
                                borderRadius: '6px',
                                padding: '1.5rem',
                                marginBottom: '1.5rem'
                            }}>
                                <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
                                    Draft Text
                                </label>
                                <div style={{ fontFamily: 'Georgia, serif', fontSize: '0.9375rem', lineHeight: '1.7', color: 'var(--color-text-primary)', whiteSpace: 'pre-wrap' }}>
                                    {result.draft_text || "Appeal draft will appear here..."}
                                </div>
                            </div>

                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <a href="/appeals" className="btn btn-primary" style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}>
                                    Review in Appeals Dashboard
                                </a>
                                <button
                                    onClick={() => setResult(null)}
                                    className="btn btn-secondary"
                                    style={{ flex: 1 }}
                                >
                                    Submit Another Claim
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
