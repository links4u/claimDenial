import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { FileText, Activity, Shield, Home } from 'lucide-react';
import HomePage from './pages/HomePage';
import SubmitClaimPage from './pages/SubmitClaimPage';
import ReviewAppealsPage from './pages/ReviewAppealsPage';
import AuditLogPage from './pages/AuditLogPage';

function Navigation() {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'active' : '';
    };

    return (
        <nav className="nav">
            <div className="nav-container">
                <Link to="/" className="nav-brand">
                    ClaimPilot™
                </Link>

                <ul className="nav-menu">
                    <li>
                        <Link to="/" className={`nav-link ${isActive('/')}`}>
                            <Home size={18} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '0.5rem' }} />
                            Home
                        </Link>
                    </li>
                    <li>
                        <Link to="/submit" className={`nav-link ${isActive('/submit')}`}>
                            <FileText size={18} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '0.5rem' }} />
                            Submit Claim
                        </Link>
                    </li>
                    <li>
                        <Link to="/appeals" className={`nav-link ${isActive('/appeals')}`}>
                            <Activity size={18} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '0.5rem' }} />
                            Review Appeals
                        </Link>
                    </li>
                    <li>
                        <Link to="/audit" className={`nav-link ${isActive('/audit')}`}>
                            <Shield size={18} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '0.5rem' }} />
                            Audit Log
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

function App() {
    return (
        <Router>
            <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navigation />

                <main style={{ flex: 1, paddingBottom: '2rem' }}>
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/submit" element={<SubmitClaimPage />} />
                        <Route path="/appeals" element={<ReviewAppealsPage />} />
                        <Route path="/audit" element={<AuditLogPage />} />
                    </Routes>
                </main>

                <footer style={{
                    backgroundColor: 'var(--color-surface)',
                    borderTop: '1px solid var(--color-border)',
                    padding: '1.5rem 0',
                    textAlign: 'center'
                }}>
                    <div className="container">
                        <p style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                            ClaimPilot™ v1.0 • Enterprise AI Platform for Healthcare Revenue Cycle Management
                        </p>
                    </div>
                </footer>
            </div>
        </Router>
    );
}

export default App;
