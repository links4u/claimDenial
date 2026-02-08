import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:1500';

const api = axios.create({
    baseURL: `${API_BASE_URL}/api/v1`,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Claims API
export const claimsAPI = {
    create: (claimData) => api.post('/claims/', claimData),
    list: (params) => api.get('/claims/', { params }),
    get: (claimId) => api.get(`/claims/${claimId}`),
    process: (claimId) => api.post('/claims/process', { claim_id: claimId }),
};

// Appeals API
export const appealsAPI = {
    list: (params) => api.get('/appeals/', { params }),
    get: (appealId) => api.get(`/appeals/${appealId}`),
    approve: (appealId, approved, feedback) =>
        api.post(`/appeals/${appealId}/approve`, { approved, feedback }),
    getForClaim: (claimId) => api.get(`/appeals/claim/${claimId}`),
};

// Policies API
export const policiesAPI = {
    list: (params) => api.get('/policies/', { params }),
    generateEmbeddings: () => api.post('/policies/generate-embeddings'),
    listPayers: () => api.get('/policies/payers'),
};

// Audit API
export const auditAPI = {
    list: (params) => api.get('/audit/', { params }),
    getForClaim: (claimId) => api.get(`/audit/claim/${claimId}`),
    listAgents: () => api.get('/audit/agents'),
};

export default api;
