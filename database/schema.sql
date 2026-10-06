-- ============================================
-- SmartMed Database Schema
-- ============================================

-- 1. Users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 2. Manufacturers
CREATE TABLE manufacturers (
    manufacturer_id INTEGER PRIMARY KEY,
    manufacturer_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    generics_count INTEGER,
    brand_names_count INTEGER
);


-- 3. Drug Classes
CREATE TABLE drug_classes (
    drug_class_id INTEGER PRIMARY KEY,
    drug_class_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    generics_count INTEGER
);


-- 4. Indications
CREATE TABLE indications (
    indication_id INTEGER PRIMARY KEY,
    indication_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    generics_count INTEGER
);


-- 5. Dosage Forms
CREATE TABLE dosage_forms (
    dosage_form_id INTEGER PRIMARY KEY,
    dosage_form_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    brand_names_count INTEGER
);


-- 6. Generics
CREATE TABLE generics (
    generic_id INTEGER PRIMARY KEY,
    generic_name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    monograph_link TEXT,
    drug_class VARCHAR(255),
    indication VARCHAR(255),

    indication_description TEXT,
    therapeutic_class_description TEXT,
    pharmacology_description TEXT,
    dosage_description TEXT,
    administration_description TEXT,
    interaction_description TEXT,
    contraindications_description TEXT,
    side_effects_description TEXT,
    pregnancy_lactation_description TEXT,
    precautions_description TEXT,
    pediatric_usage_description TEXT,
    overdose_effects_description TEXT,
    duration_of_treatment_description TEXT,
    reconstitution_description TEXT,
    storage_conditions_description TEXT
);


-- 7. Medicines
CREATE TABLE medicines (
    medicine_id INTEGER PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    medicine_type VARCHAR(50) NOT NULL,
    slug VARCHAR(255),

    dosage_form_id INTEGER,
    generic_id INTEGER,
    strength VARCHAR(255),
    manufacturer_id INTEGER,

    package_container TEXT,
    package_size TEXT,

    FOREIGN KEY (dosage_form_id)
        REFERENCES dosage_forms(dosage_form_id),

    FOREIGN KEY (generic_id)
        REFERENCES generics(generic_id),

    FOREIGN KEY (manufacturer_id)
        REFERENCES manufacturers(manufacturer_id)
);


-- 8. Collection Centers
CREATE TABLE collection_centers (
    center_id SERIAL PRIMARY KEY,
    center_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    phone VARCHAR(20),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    is_active BOOLEAN DEFAULT TRUE
);


-- 9. Disposal Requests
CREATE TABLE disposal_requests (
    request_id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,

    quantity INTEGER DEFAULT 1,
    expiry_date DATE,

    disposal_guidance TEXT,

    status VARCHAR(50) DEFAULT 'REQUESTED',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (medicine_id)
        REFERENCES medicines(medicine_id)
);


-- 10. Tracking
CREATE TABLE tracking (
    tracking_id SERIAL PRIMARY KEY,

    request_id INTEGER UNIQUE NOT NULL,

    tracking_code VARCHAR(50) UNIQUE NOT NULL,

    status VARCHAR(50) DEFAULT 'REQUESTED',

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (request_id)
        REFERENCES disposal_requests(request_id)
);


-- 11. Admins
CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,

    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- Indexes for faster medicine search
-- ============================================

CREATE INDEX idx_medicine_brand
ON medicines(brand_name);

CREATE INDEX idx_medicine_generic
ON medicines(generic_id);

CREATE INDEX idx_medicine_manufacturer
ON medicines(manufacturer_id);

CREATE INDEX idx_medicine_type
ON medicines(medicine_type);

CREATE INDEX idx_disposal_user
ON disposal_requests(user_id);

CREATE INDEX idx_disposal_status
ON disposal_requests(status);

CREATE INDEX idx_tracking_code
ON tracking(tracking_code);