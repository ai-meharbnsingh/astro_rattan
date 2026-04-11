-- Lal Kitab Kundli Database Schema
-- Comprehensive database for Lal Kitab astrology predictions

-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Kundli/Birth Charts Table
CREATE TABLE kundlis (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    time_of_birth TIME NOT NULL,
    place_of_birth VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    timezone VARCHAR(50),
    gender ENUM('male', 'female', 'other') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Planetary Positions Table
CREATE TABLE planetary_positions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    planet ENUM('sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu') NOT NULL,
    house INT NOT NULL CHECK (house BETWEEN 1 AND 12),
    zodiac_sign VARCHAR(20) NOT NULL,
    degree DECIMAL(6, 2) NOT NULL,
    is_retrograde BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Nishaniyan (Signs) Master Data
CREATE TABLE nishaniyan_master (
    id INT PRIMARY KEY AUTO_INCREMENT,
    planet ENUM('sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu') NOT NULL,
    house INT NOT NULL CHECK (house BETWEEN 1 AND 12),
    nishani_text TEXT NOT NULL,
    category ENUM('general', 'health', 'wealth', 'marriage', 'career', 'family') DEFAULT 'general',
    severity ENUM('mild', 'moderate', 'strong') DEFAULT 'moderate'
);

-- Lal Kitab Debts (Rin) Master Data
CREATE TABLE lal_kitab_debts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    debt_type VARCHAR(100) NOT NULL,
    planet ENUM('sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu') NOT NULL,
    description TEXT NOT NULL,
    indication TEXT,
    remedy TEXT NOT NULL
);

-- Remedies Master Data
CREATE TABLE remedies_master (
    id INT PRIMARY KEY AUTO_INCREMENT,
    planet ENUM('sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu') NOT NULL,
    house INT CHECK (house BETWEEN 1 AND 12),
    remedy_text TEXT NOT NULL,
    remedy_type ENUM('donation', 'worship', 'gemstone', 'mantra', 'behavior', 'other') DEFAULT 'other',
    duration_days INT DEFAULT 43,
    instructions TEXT,
    caution TEXT
);

-- Varshphal (Yearly Predictions) Table
CREATE TABLE varshphal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    year INT NOT NULL,
    varsh_lord VARCHAR(50),
    muntha_sign VARCHAR(20),
    muntha_house INT,
    prediction_text TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Dasha Periods Table
CREATE TABLE dasha_periods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    dasha_type ENUM('vimshottari', 'yogini', 'char') DEFAULT 'vimshottari',
    planet VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_years DECIMAL(4, 2),
    prediction_text TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Marriage Predictions Table
CREATE TABLE marriage_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    marriage_age INT,
    spouse_details TEXT,
    compatibility_score INT,
    manglik_status ENUM('manglik', 'non-manglik', 'partial') DEFAULT 'non-manglik',
    predictions TEXT,
    remedies TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Career Predictions Table
CREATE TABLE career_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    suitable_careers TEXT,
    business_suitability BOOLEAN,
    job_suitability BOOLEAN,
    favourable_periods TEXT,
    challenges TEXT,
    remedies TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Health Predictions Table
CREATE TABLE health_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    general_health TEXT,
    vulnerable_areas TEXT,
    chronic_issues TEXT,
    favourable_periods TEXT,
    precautions TEXT,
    remedies TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Wealth Predictions Table
CREATE TABLE wealth_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    wealth_potential ENUM('excellent', 'good', 'moderate', 'challenging') DEFAULT 'moderate',
    income_sources TEXT,
    favourable_periods TEXT,
    investment_advice TEXT,
    challenges TEXT,
    remedies TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Gochar (Transit) Predictions Table
CREATE TABLE gochar_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    transit_planet VARCHAR(20) NOT NULL,
    transit_house INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    prediction_text TEXT,
    remedies TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Teva Details Table
CREATE TABLE teva_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    teva_type ENUM('ratandh', 'dharmi', 'nabalik', 'normal') DEFAULT 'normal',
    blind_planets TEXT,
    righteous_planets TEXT,
    underage_planets TEXT,
    description TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Chandra Chalana Table
CREATE TABLE chandra_chalana (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kundli_id INT NOT NULL,
    moon_sign VARCHAR(20) NOT NULL,
    chalana_method ENUM('first', 'second') DEFAULT 'first',
    predictions TEXT,
    remedies TEXT,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- User Saved Predictions
CREATE TABLE saved_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    kundli_id INT NOT NULL,
    prediction_type VARCHAR(50) NOT NULL,
    prediction_data JSON,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (kundli_id) REFERENCES kundlis(id) ON DELETE CASCADE
);

-- Admin Users Table
CREATE TABLE admin_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role ENUM('super_admin', 'admin', 'editor') DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Sample Nishaniyan Data (Sun in different houses)
INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
('sun', 1, 'क्रोधी स्वभाव का होगा। सिर के बाल कम होंगे। बहुत ज़्यादा हिम्मती होगा। पत्नी हमेशा बीमार रहेगी या दब कर रहेगी।', 'general', 'moderate'),
('sun', 2, 'जातक के परिवार में 2 शादियाँ होंगी। भाई का तलाक़ हो जाता है। परिवार में औरतों की कमी रहेगी।', 'family', 'strong'),
('sun', 3, 'पड़ोस का घर उजड़ा होगा या पड़ोसी परेशान होगा। भाइयों और दोस्तों से अनबन रहती है।', 'general', 'moderate'),
('sun', 4, 'जातक मीठे का शौकीन होगा। घर में गच्चक, गुड़, chocolate आएगा।', 'general', 'mild'),
('sun', 5, 'पेट हमेशा ख़राब ही रहता है। परिवार में दो शादियाँ ज़रूर होंगी।', 'health', 'moderate'),
('sun', 6, 'जातक का जन्म नानके में होता है या नानके निसर्ग होम के पैसे भरते हैं। गुप्त शत्रु ज़्यादा बनते हैं।', 'general', 'moderate'),
('sun', 7, 'घर में गुड़, गच्चक, chocolate गिफ़्ट आती है। प्रेम विवाह करने के योग।', 'marriage', 'moderate'),
('sun', 8, 'जातक की पत्नी घर के भेद बाहर बताएगी। मुकदमे में बार बार हार होती है।', 'marriage', 'strong'),
('sun', 9, 'घर में पीतल के बड़े बर्तन खाली पड़े होंगे। जब भी मकान बदलेगा खुद पे या पिता पे कष्ट आएगा।', 'general', 'moderate'),
('sun', 10, 'घर में खोटे सिक्के पड़े होंगे। जहाँ काम कम पैसों में हो सकता है यह ज़्यादा पैसे दे के आएगा।', 'wealth', 'moderate'),
('sun', 11, 'जातक का ससुर जीवित नही रहेगा। नेकी करेगा तो बदनामी मिलेगी।', 'family', 'strong'),
('sun', 12, 'जातक को मोबाइल गिफ़्ट मिलता है। उच्च रक्तचाप रहेगा।', 'health', 'moderate');

-- Insert Sample Remedies Data
INSERT INTO remedies_master (planet, house, remedy_text, remedy_type, duration_days, instructions) VALUES
('sun', 1, 'रूबी धारण करें। बंदरों को गुड़ खिलाएं। तांबे के सांप जल में प्रवाहित करें।', 'gemstone', 43, 'सूर्योदय के समय जल अर्पित करें'),
('sun', 2, 'गेहूं, गुड़ और लोहे की कड़ाही का दान करें। नारियल, बादाम और तेल का दान करें।', 'donation', 43, 'रविवार को दान करें'),
('sun', 3, 'सूर्य को गुड़ मिलाकर जल चढ़ाएं। कुएं में चांदी का टुकड़ा डालें।', 'worship', 43, 'प्रतिदिन सुबह करें'),
('jupiter', 1, 'पीला पुखराज धारण करें। मिट्टी की कुज्जी में शक्कर भरकर कच्ची जमीन में दबाएं।', 'gemstone', 43, 'गुरुवार से शुरू करें'),
('jupiter', 2, 'सांप को दूध पिलाना। सोने में ब्राजील का पुखराज धारण करना।', 'worship', 43, 'गुरुवार को दूध पिलाएं'),
('rahu', 1, '400 ग्राम सीसा बहते पानी में डालें। गले में चांदी पहनें।', 'donation', 43, 'शनिवार को करें'),
('ketu', 1, 'बंदरों को गुड़ खिलाएं। केसर का तिलक लगाएं।', 'worship', 43, 'प्रतिदिन करें');

-- Insert Lal Kitab Debts Data
INSERT INTO lal_kitab_debts (debt_type, planet, description, indication, remedy) VALUES
('पितृ ऋण', 'sun', 'पिता या पूर्वजों से संबंधित ऋण', 'सूर्य खराब हो, पिता से अनबन, आंखों की समस्या', 'तांबे के बर्तन में गंगाजल रखें, पिता का आशीर्वाद लें'),
('मातृ ऋण', 'moon', 'माता से संबंधित ऋण', 'चंद्रमा खराब हो, माता से अनबन, मानसिक तनाव', 'चांदी का चौकोर टुकड़ा रखें, माता की सेवा करें'),
('भ्रातृ ऋण', 'mars', 'भाई बहनों से संबंधित ऋण', 'मंगल खराब हो, भाइयों से झगड़े, रक्त संबंधी रोग', 'लाल मसूर की दाल दान करें, भाई का सम्मान करें'),
('देव ऋण', 'jupiter', 'देवताओं या गुरु से संबंधित ऋण', 'गुरु खराब हो, संतान संबंधी समस्याएं', 'पीपल के पेड़ की पूजा करें, ब्राह्मण को भोजन कराएं'),
('स्त्री ऋण', 'venus', 'स्त्रियों से संबंधित ऋण', 'शुक्र खराब हो, वैवाहिक समस्याएं', 'गाय की सेवा करें, पत्नी का सम्मान करें'),
('शत्रु ऋण', 'saturn', 'शत्रुओं या कर्म से संबंधित ऋण', 'शनि खराब हो, देरी से सफलता, शारीरिक पीड़ा', 'शनिवार को तेल दान करें, काले कुत्ते को रोटी खिलाएं'),
('पितामह ऋण', 'rahu', 'पूर्वजों या नाना से संबंधित ऋण', 'राहु खराब हो, गुप्त शत्रु, नशे की लत', '400 ग्राम सीसा बहते पानी में डालें, नाना का सम्मान करें'),
('प्रपितामह ऋण', 'ketu', 'पूर्वजों या दादा से संबंधित ऋण', 'केतु खराब हो, आध्यात्मिक भ्रम, अकाल मृत्यु का भय', 'बंदरों को गुड़ खिलाएं, केसर का तिलक लगाएं');
