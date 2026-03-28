# P28 AstroVedic -- Gemini Audit (2026-03-28)

**Model:** gemini-2.5-pro | **CLI:** v0.35.3

---

### **1. ASTROLOGY ACCURACY**

**Score: 3/10**

The core of an astrology application is its calculation engine. This project's engine (`astro_engine.py`) has a fatal flaw for a production system: it has a pure-python fallback of "low-precision" when the `swisseph` library is not available. This is unacceptable for a commercial product. Astrological calculations must be precise, and a low-accuracy fallback introduces a massive risk of providing incorrect chart data to users, which invalidates all subsequent interpretations (Dasha, Doshas, etc.).

The primary path using `swisseph` is good and is the industry standard. However, the tests in `test_astro_engine.py` are weak; they only perform basic sanity checks (e.g., "is Ketu 180 degrees from Rahu?", "are there 12 houses?"). There are no regression tests against known chart data from a reliable source like Jagannatha Hora or AstroSage for the specified test case (DOB=1985-08-23, Time=23:15, Place=Delhi). Without these, the accuracy of the `swisseph` implementation itself cannot be verified. The code also uses Placidus for houses, which is more common in Western astrology; many Vedic astrologers prefer whole sign houses. This isn't necessarily wrong, but it's a choice that should be explicit.

### **2. CODE QUALITY**

**Score: 5/10**

-   **Error Handling**: Mediocre. The `kundli.py` router has some basic error handling (e.g., 404 for not found), but many of the engine functions themselves lack robust error handling for edge cases in astrological calculations.
-   **Security**: Mixed bag.
    -   **SQL Injection**: The use of `psycopg2` with parameterized queries (e.g., `db.execute("... WHERE id = %s", (kundli_id,))`) is good and prevents SQL injection.
    -   **JWT Security**: The JWT secret in `config.py` is randomly generated if not set in the environment. This is a good development default, but the warning message is crucial. Token expiry is set, which is good. The `require_role` dependency is a clean way to handle authorization.
    -   **CORS**: It is configured, but allowing `"*"` for methods and headers is too permissive for a production environment. It should be restricted to known methods and headers.
    -   **Rate Limiting**: Basic IP-based rate limiting is implemented with `slowapi`, which is a good start.
    -   **Password Hashing**: `passlib` with bcrypt is used, which is the correct approach.
-   **Dead Code**: There are signs of code rot. The `database.py` file has several `migrate_*` functions that are empty no-ops, with comments indicating they are for PostgreSQL. This suggests a previous database system (like SQLite) was used and the migration path has left some artifacts.

### **3. FRONTEND QUALITY**

**Score: 4/10**

-   **Component Structure**: The frontend seems to have a decent structure, with `components` and `sections` directories. However, `KundliGenerator.tsx` is a monolithic 100KB+ component that manages an enormous amount of state for the entire multi-tab result view. This is a major red flag for maintainability. This component should be broken down into many smaller, manageable child components, with state management handled by a dedicated library (like Zustand or Redux) or lifted to a context provider.
-   **State Management**: The heavy use of `useState` in `KundliGenerator.tsx` for every single piece of data (`doshaData`, `iogitaData`, `dashaData`, etc.) is a symptom of poor state management strategy. Each tab's data and loading state should be self-contained or managed by a centralized store.
-   **Loading/Error States**: There are loading states (`loadingDosha`, `loadingIogita`, etc.), but the implementation is scattered and verbose. Error handling seems to be a single `setError` string, which is insufficient for a complex UI.
-   **Theme & Responsiveness**: I cannot visually inspect the theme. The code uses TailwindCSS, which is good for creating a consistent design system. However, the presence of a `MOBILE_RESPONSIVE.md` file suggests that responsiveness might be an afterthought or a documented problem area.

### **4. API DESIGN**

**Score: 6/10**

-   **RESTful Conventions**: The API mostly follows RESTful conventions (e.g., `GET /kundli/list`, `POST /kundli/generate`).
-   **Consistency**: The use of Pydantic models (`app/models.py`) ensures consistent request and response shapes, which is excellent.
-   **Input Validation**: Pydantic models also provide input validation, which is a major strength.
-   **Pagination**: There is no evidence of pagination on the `/api/kundli/list` endpoint. This is a significant omission and will cause performance issues as users create more kundlis.
-   **Endpoint Design**: The `kundli.py` router is a bit of a monolith. Endpoints like `/dosha`, `/dasha`, `/ashtakvarga` are all separate `POST` requests that take a `kundli_id`. It might be cleaner to have these as sub-resources like `GET /kundli/{id}/dosha`. The use of `POST` for read-only analysis operations is not strictly RESTful (should be `GET`).

### **5. PERFORMANCE**

**Score: 4/10**

-   **Database**: The use of a `ThreadedConnectionPool` in `database.py` is good for managing database connections in a multi-threaded FastAPI environment. The schema in `database.py` shows that indexes are being created for foreign keys and commonly queried columns, which is excellent.
-   **N+1 Queries**: Without seeing more complex data retrieval logic, it's hard to spot N+1 queries. However, the simple list endpoints are likely not suffering from this.
-   **Frontend Bundle Size**: The audit prompt mentions a 1.8MB bundle size. This is very large for a modern web app. The `App.tsx` file shows lazy loading is used for `CosmicBackground` and `Kundli3D`, which is good. However, many large sections are imported directly, which will contribute to a large initial bundle. `KundliGenerator.tsx` alone is a huge red flag for performance.
-   **Client-Side Performance**: The massive state management in `KundliGenerator.tsx` will lead to many unnecessary re-renders and a sluggish UI, especially on lower-end devices.

### **6. DEPLOYMENT**

**Score: 7/10**

The project includes configuration for both Render (`render.yaml`) and Vercel (`vercel.json`), which is good. The `database.py` code correctly handles SSL modes for cloud databases. The use of environment variables for configuration and secrets (`config.py`) is standard and correct. The presence of a `Dockerfile` shows that containerization has been considered. The main risk is the Render free tier's cold start, which is acknowledged in the audit prompt and can lead to a poor user experience on the first load.

### **7. MISSING FEATURES / BUGS**

**Score: 5/10**

-   **Missing Features**:
    1.  **Whole Sign Houses**: No option to switch house systems.
    2.  **Ephemeris Management**: The reliance on an environment variable for the Swiss Ephemeris path is brittle. A production system should have a managed, verified ephemeris data source baked into its deployment.
    3.  **Timezone Abstraction**: The frontend requires the user to provide a raw timezone offset. A production app should use a library to look up the correct timezone and DST for a given place and date, as users often do not know the correct offset.
    4.  **Detailed Transit Analysis**: The current transit engine is basic. A full-featured platform would offer detailed transit reports, including aspects to natal planets.
    5.  **Remedies Integration**: The Lal Kitab and Dosha engines are present, but there is no deep, integrated system for suggesting and tracking remedies.
-   **Potential Bugs**:
    1.  **Fallback Engine**: The biggest bug is the existence of the low-accuracy fallback engine. This is a critical issue.
    2.  **State Management in Frontend**: The monolithic `KundliGenerator` component is a bug farm waiting to happen. State inconsistencies are almost guaranteed.
    3.  **No Pagination**: The `/kundli/list` endpoint will eventually become slow and unusable for active users.

---

### **Overall Score & Verdict**

| Category | Score | Weight | Weighted |
|---|---|---|---|
| Astrology Accuracy | 3/10 | 3x | 9 |
| Code Quality | 5/10 | 1x | 5 |
| Frontend Quality | 4/10 | 1x | 4 |
| API Design | 6/10 | 1x | 6 |
| Performance | 4/10 | 1x | 4 |
| Deployment | 7/10 | 1x | 7 |
| Missing Features / Bugs | 5/10 | 1x | 5 |

**Weighted Average: (9 + 5 + 4 + 6 + 4 + 7 + 5) / (3 + 1 + 1 + 1 + 1 + 1 + 1) = 40 / 9 = 4.44**

**Overall Score: 4.4 / 10**

### **Top 5 Critical Issues to Fix**

1.  **Remove Fallback Astrology Engine**: The pure-python fallback in `astro_engine.py` must be completely removed. The application should fail loudly if `swisseph` is unavailable. An inaccurate chart is worse than no chart.
2.  **Refactor `KundliGenerator.tsx`**: Break this 100KB+ monolith into smaller, manageable components. Introduce a proper state management solution (Context with reducers, Zustand, or Redux Toolkit) to handle the complex state of the results view.
3.  **Implement Strong Astrological Validation**: Add a comprehensive test suite that validates chart calculations (planets, ascendant, D9) against a trusted source like AstroSage for a dozen different birth data samples.
4.  **Implement Pagination**: Add pagination to all list endpoints, starting with `/api/kundli/list`.
5.  **Improve Timezone Handling**: Replace the manual timezone offset input with a proper timezone lookup library (like `geo-tz`) that takes latitude/longitude and a date to determine the correct timezone identifier (e.g., "Asia/Kolkata") and handles historical DST changes.

### **Top 5 Nice-to-Have Improvements**

1.  **House System Option**: Allow users to switch between Placidus and Whole Sign houses.
2.  **Code Splitting**: Be more aggressive with lazy loading in the frontend (`App.tsx`) to reduce the initial bundle size.
3.  **API Refactoring**: Refactor analysis endpoints (`/dosha`, `/dasha`) to be `GET` requests on sub-resources (e.g., `/kundli/{id}/dasha`).
4.  **Component Library**: Formalize the UI components into a storybook for better documentation and reusability.
5.  **Database Migrations**: Replace the no-op `migrate_*` functions with a proper migration tool like Alembic to manage schema changes systematically.

### **Verdict: Is this production-ready?**

**Absolutely not.** The presence of a low-accuracy fallback astrology engine is a deal-breaker. It demonstrates a fundamental misunderstanding of the domain, where precision is paramount. The frontend's monolithic `KundliGenerator` component points to severe maintainability and performance issues that will plague development and frustrate users. While the project has some good parts (use of Pydantic, basic security measures, CI/CD setup), the critical flaws in the core domain logic and frontend architecture make it unfit for a production environment where users would be making life decisions based on its output.
