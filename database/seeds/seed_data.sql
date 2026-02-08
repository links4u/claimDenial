-- ClaimPilot™ Seed Data
-- Sample claims and policy data for testing

-- =====================================================
-- SEED: Sample Claims
-- =====================================================
INSERT INTO claims (claim_id, denial_code, denial_description, payer_name, policy_text, category) VALUES
(
    'CLM-2024-001',
    'CO-197',
    'Precertification/authorization/notification absent. Service not authorized or pre-certified by the payer.',
    'Blue Cross Blue Shield',
    'Section 5.2: All specialist consultations require prior authorization 48 hours before the appointment.',
    'Authorization'
),
(
    'CLM-2024-002',
    'CO-50',
    'These are non-covered services because this is not deemed a medical necessity by the payer.',
    'Aetna',
    'Section 8.1: Cosmetic procedures are excluded unless deemed medically necessary for functional restoration.',
    'Medical Necessity'
),
(
    'CLM-2024-003',
    'CO-16',
    'Claim lacks information or has submission/billing error(s). Coding error detected.',
    'UnitedHealthcare',
    'Section 12.4: CPT codes must match the documented diagnosis codes per ICD-10 guidelines.',
    'Coding'
),
(
    'CLM-2024-004',
    'CO-96',
    'Non-covered charge(s). Service is not included in the policy coverage.',
    'Cigna',
    'Section 3.7: Alternative medicine treatments including acupuncture are not covered under standard plans.',
    'Coverage'
),
(
    'CLM-2024-005',
    'CO-18',
    'Exact duplicate claim/service. Claim previously processed and paid.',
    'Humana',
    NULL,
    'Other'
);

-- =====================================================
-- SEED: Sample Policy Excerpts
-- =====================================================

-- Note: Embeddings would normally be generated programmatically
-- For seed data, we'll insert NULL and let the application generate them

INSERT INTO policies (payer_name, section_title, section_text, metadata) VALUES
(
    'Blue Cross Blue Shield',
    'Section 5.2 - Prior Authorization Requirements',
    'All specialist consultations, including cardiology, neurology, and orthopedics, require prior authorization to be obtained at least 48 hours before the scheduled appointment. Emergency consultations are exempt from this requirement. Failure to obtain prior authorization may result in claim denial under code CO-197.',
    '{"version": "2024.1", "effective_date": "2024-01-01", "category": "Authorization"}'::jsonb
),
(
    'Blue Cross Blue Shield',
    'Section 8.3 - Imaging Services Authorization',
    'Advanced imaging services such as MRI, CT scans, and PET scans require medical necessity review and prior authorization. Standard X-rays do not require authorization. Authorization requests must include clinical justification and relevant diagnosis codes.',
    '{"version": "2024.1", "effective_date": "2024-01-01", "category": "Authorization"}'::jsonb
),
(
    'Aetna',
    'Section 8.1 - Medical Necessity for Cosmetic Procedures',
    'Cosmetic procedures are generally excluded from coverage unless they are deemed medically necessary for functional restoration following trauma, disease, or congenital abnormality. Examples include reconstructive surgery post-mastectomy or repair of facial fractures. Elective cosmetic surgeries such as rhinoplasty for aesthetic purposes are not covered.',
    '{"version": "2024.2", "effective_date": "2024-02-15", "category": "Medical Necessity"}'::jsonb
),
(
    'Aetna',
    'Section 9.4 - Experimental Treatments',
    'Treatments classified as experimental or investigational are not covered. Medical necessity review applies to all new therapeutic approaches. Coverage decisions are based on peer-reviewed clinical evidence and FDA approval status.',
    '{"version": "2024.2", "effective_date": "2024-02-15", "category": "Medical Necessity"}'::jsonb
),
(
    'UnitedHealthcare',
    'Section 12.4 - Coding Accuracy Requirements',
    'All claims must use accurate CPT and ICD-10 codes that align with documented diagnoses and procedures. Coding errors including mismatched diagnosis-procedure codes, outdated codes, or insufficient specificity will result in claim denial under CO-16. Providers must use the current year's coding manual.',
    '{"version": "2024.3", "effective_date": "2024-03-01", "category": "Coding"}'::jsonb
),
(
    'UnitedHealthcare',
    'Section 12.8 - Modifier Usage',
    'Appropriate use of modifiers is required for accurate claim processing. Common modifiers include -25 (separate E&M service), -59 (distinct procedural service), and -76 (repeat procedure by same physician). Incorrect or missing modifiers may lead to denials.',
    '{"version": "2024.3", "effective_date": "2024-03-01", "category": "Coding"}'::jsonb
),
(
    'Cigna',
    'Section 3.7 - Excluded Services - Alternative Medicine',
    'Alternative and complementary medicine treatments are generally not covered under standard benefit plans. This includes but is not limited to acupuncture, chiropractic care beyond acute treatment, naturopathy, and homeopathy. Members may purchase supplemental coverage for these services.',
    '{"version": "2024.1", "effective_date": "2024-01-10", "category": "Coverage"}'::jsonb
),
(
    'Cigna',
    'Section 3.2 - Covered Preventive Services',
    'All ACA-mandated preventive services are covered at 100% when obtained from in-network providers. This includes annual physicals, immunizations, cancer screenings, and well-child visits. No prior authorization is required for preventive services.',
    '{"version": "2024.1", "effective_date": "2024-01-10", "category": "Coverage"}'::jsonb
),
(
    'Humana',
    'Section 7.1 - Duplicate Claim Prevention',
    'Claims that are exact duplicates of previously processed claims will be denied under code CO-18. The system automatically flags claims with identical service dates, provider, patient, and procedure codes. If resubmission is necessary due to correction, use appropriate claim adjustment reason codes.',
    '{"version": "2024.4", "effective_date": "2024-04-01", "category": "Administrative"}'::jsonb
);

-- =====================================================
-- SEED: Sample Appeals (for testing UI)
-- =====================================================

INSERT INTO appeals (claim_id, draft_text, policy_citations, status, approved) VALUES
(
    (SELECT id FROM claims WHERE claim_id = 'CLM-2024-001'),
    'Dear Blue Cross Blue Shield Appeals Committee,

I am writing to appeal the denial of Claim CLM-2024-001 under denial code CO-197 for precertification absence.

While I acknowledge that Section 5.2 of your policy requires prior authorization 48 hours before specialist consultations, this case qualifies as an emergency consultation exempt from this requirement. The patient presented with acute cardiac symptoms requiring immediate cardiologist evaluation.

Clinical documentation attached demonstrates the emergent nature of this consultation. I respectfully request reconsideration of this claim under the emergency exemption clause referenced in Section 5.2.

Thank you for your prompt attention to this matter.

Sincerely,
[Provider Name]',
    '["Section 5.2 - Prior Authorization Requirements"]'::jsonb,
    'draft',
    FALSE
);

-- =====================================================
-- SEED: Sample Audit Logs
-- =====================================================

INSERT INTO audit_logs (claim_id, agent_name, input_data, output_data, metadata) VALUES
(
    (SELECT id FROM claims WHERE claim_id = 'CLM-2024-001'),
    'DenialClassifierAgent',
    '{"denial_code": "CO-197", "denial_description": "Precertification/authorization/notification absent"}'::jsonb,
    '{"category": "Authorization", "confidence": 0.98}'::jsonb,
    '{"model": "claude-3-5-sonnet-20241022", "latency_ms": 1247, "token_count": 156}'::jsonb
);

COMMIT;
