# Lal Kitab Kundli - Complete Astrology Website

A comprehensive Lal Kitab astrology website with kundli generation, predictions, and remedies.

## Features

### Core Features
- **Complete Kundli Analysis**: Generate detailed birth charts with accurate planetary positions
- **Planetary Positions**: Display all 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) in 12 houses
- **Nishaniyan (Signs)**: 108+ different signs based on planet-house combinations
- **Lal Kitab Debts (Rin)**: Identify and clear karmic debts from past lives
- **Remedies (Upay)**: Simple and effective remedies for all life problems

### Prediction Tabs
- **Marriage Predictions**: Timing, spouse details, compatibility, Manglik dosha check
- **Career Guidance**: Suitable careers, business vs job analysis, favourable periods
- **Health Analysis**: Vulnerable areas, preventive measures, health remedies
- **Wealth Predictions**: Financial potential, income sources, investment advice
- **Varshphal (Yearly)**: Yearly predictions based on birth chart
- **Dasha Predictions**: Planetary period analysis
- **Gochar (Transit)**: Current planetary transit effects
- **Teva Details**: Blind planets, Dharmi Teva, Nabalik Teva
- **Chandra Chalana**: Moon-based predictions

### User Features
- User Registration and Login
- Create and Save Multiple Kundlis
- View Detailed Kundli Charts
- Access All Prediction Tabs
- Save Favorite Predictions

### Admin Features
- Manage Users and Kundlis
- Add/Edit Nishaniyan Data
- Add/Edit Remedies
- View Dashboard Statistics

## Tech Stack

### Frontend
- React 19
- React Router DOM
- Tailwind CSS
- Lucide React Icons
- Vite Build Tool

### Backend
- Node.js
- Express.js
- MySQL Database
- JWT Authentication
- bcrypt.js for Password Hashing

## Database Schema

### Tables
1. **users**: User accounts and profiles
2. **kundlis**: Birth chart data
3. **planetary_positions**: Planet positions in houses
4. **nishaniyan_master**: Signs data for planet-house combinations
5. **lal_kitab_debts**: Karmic debts information
6. **remedies_master**: Remedies for planets
7. **varshphal**: Yearly predictions
8. **dasha_periods**: Planetary periods
9. **marriage_predictions**: Marriage analysis
10. **career_predictions**: Career guidance
11. **health_predictions**: Health analysis
12. **wealth_predictions**: Wealth analysis
13. **gochar_predictions**: Transit predictions
14. **teva_details**: Teva classification
15. **chandra_chalana**: Moon predictions
16. **saved_predictions**: User saved predictions
17. **admin_users**: Admin accounts

## Installation

### Prerequisites
- Node.js (v16 or higher)
- MySQL Database

### Frontend Setup
```bash
cd app
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
npm install
# Configure .env file with database credentials
npm start
```

### Database Setup
1. Create MySQL database: `lal_kitab_kundli`
2. Import schema: `backend/database/schema.sql`

## Environment Variables

### Backend (.env)
```
PORT=5000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=lal_kitab_kundli
JWT_SECRET=your_secret_key
NODE_ENV=development
```

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - User login
- GET `/api/auth/me` - Get current user

### Kundli
- POST `/api/kundli/create` - Create new kundli
- GET `/api/kundli/list` - Get all kundlis
- GET `/api/kundli/:id` - Get single kundli
- DELETE `/api/kundli/:id` - Delete kundli

### Predictions
- GET `/api/predictions/nishaniyan/:kundliId` - Get nishaniyan
- GET `/api/predictions/debts/:kundliId` - Get debts
- GET `/api/predictions/marriage/:kundliId` - Get marriage predictions
- GET `/api/predictions/career/:kundliId` - Get career predictions
- GET `/api/predictions/health/:kundliId` - Get health predictions
- GET `/api/predictions/wealth/:kundliId` - Get wealth predictions

### Remedies
- GET `/api/remedies/:kundliId` - Get remedies for kundli
- GET `/api/remedies/planet/:planet` - Get planet-specific remedies

### Admin
- POST `/api/admin/login` - Admin login
- GET `/api/admin/users` - Get all users
- GET `/api/admin/kundlis` - Get all kundlis
- GET `/api/admin/stats` - Get dashboard stats
- POST `/api/admin/nishaniyan` - Add nishaniyan
- POST `/api/admin/remedy` - Add remedy

## Lal Kitab Concepts

### Nishaniyan (Signs)
Nishaniyan are specific indications that appear in a birth chart based on planetary positions. They reveal:
- Problems in various life areas
- Root causes of issues
- Severity of problems
- Solutions through remedies

### Rin (Debts)
Lal Kitab identifies 8 types of karmic debts:
1. **Pitra Rin** (Sun) - Debts to ancestors/father
2. **Matra Rin** (Moon) - Debts to mother
3. **Bhratri Rin** (Mars) - Debts to siblings
4. **Dev Rin** (Jupiter) - Debts to deities/guru
5. **Stri Rin** (Venus) - Debts to women
6. **Shatru Rin** (Saturn) - Debts to enemies/karma
7. **Pitamah Rin** (Rahu) - Debts to maternal grandfather
8. **Prapitamah Rin** (Ketu) - Debts to paternal grandfather

### Teva System
Classification of birth charts based on planetary positions:
- **Ratandh Teva** - Blind planets
- **Dharmi Teva** - Righteous planets
- **Nabalik Teva** - Underage planets
- **Normal Teva** - Regular chart

## Planets and Their Significance

| Planet | Name | Significance |
|--------|------|--------------|
| Sun | Surya | Soul, Father, Authority |
| Moon | Chandra | Mind, Mother, Emotions |
| Mars | Mangal | Courage, Siblings, Property |
| Mercury | Budh | Intelligence, Communication |
| Jupiter | Guru | Wisdom, Children, Wealth |
| Venus | Shukra | Love, Marriage, Luxury |
| Saturn | Shani | Karma, Discipline, Delays |
| Rahu | - | Illusion, Foreign, Sudden |
| Ketu | - | Spirituality, Detachment |

## Houses and Their Significance

| House | Name | Significance |
|-------|------|--------------|
| 1 | Pratham Bhav | Body, Personality, Health |
| 2 | Dvitiya Bhav | Wealth, Family, Speech |
| 3 | Tritiya Bhav | Courage, Siblings, Efforts |
| 4 | Chaturth Bhav | Mother, Vehicle, Happiness |
| 5 | Pancham Bhav | Children, Education, Speculation |
| 6 | Shashth Bhav | Diseases, Enemies, Debts |
| 7 | Saptam Bhav | Marriage, Spouse, Business |
| 8 | Ashtam Bhav | Longevity, Sudden Gains |
| 9 | Navam Bhav | Fortune, Religion, Father |
| 10 | Dasham Bhav | Career, Status, Reputation |
| 11 | Ekadash Bhav | Gains, Friends, Elder Siblings |
| 12 | Dwadash Bhav | Expenses, Liberation, Foreign |

## License

This project is licensed under the MIT License.

## Credits

Based on the ancient wisdom of Lal Kitab astrology as documented in:
- Book of Nishaniya
- Nazm E Jyotish
- Nishaniya hi Nishaniya
- Graho Ki Nishaniya
