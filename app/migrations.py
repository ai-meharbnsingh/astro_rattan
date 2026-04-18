"""H-02: Database Migration System — tracks and applies schema migrations in order."""
import logging
import psycopg2
import psycopg2.extras
from typing import List, Tuple

logger = logging.getLogger(__name__)

from app.database import DATABASE_URL

# Each migration: (version, description, sql)
MIGRATIONS: List[Tuple[int, str, str]] = [
    (
        1,
        "Add audit_log table",
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
            user_id TEXT,
            action TEXT NOT NULL,
            resource TEXT,
            resource_id TEXT,
            details TEXT,
            ip_address TEXT,
            created_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
        );
        CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
        CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);
        """,
    ),
    (
        2,
        "Add date_of_birth, gender, city, is_active columns to users",
        """
        SELECT 1;
        """,
    ),
    (
        3,
        "Add blog_posts table and seed starter editorial content",
        """
        CREATE TABLE IF NOT EXISTS blog_posts (
            id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
            slug TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            cover_image_url TEXT,
            tags TEXT NOT NULL DEFAULT '[]',
            author_name TEXT NOT NULL DEFAULT 'Astro Rattan Editorial',
            seo_title TEXT,
            seo_description TEXT,
            is_published INTEGER NOT NULL DEFAULT 1,
            published_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS'),
            created_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS'),
            updated_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
        );
        CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
        CREATE INDEX IF NOT EXISTS idx_blog_posts_published ON blog_posts(is_published, published_at DESC);
        """,
    ),
    (
        4,
        "Add email_verifications table for OTP-based registration",
        """
        CREATE TABLE IF NOT EXISTS email_verifications (
            id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT to_char(NOW(), 'YYYY-MM-DDTHH24:MI:SS')
        );
        CREATE INDEX IF NOT EXISTS idx_email_verifications_email ON email_verifications(email);
        """,
    ),
    (
        5,
        "Add ON DELETE CASCADE to all foreign key constraints",
        # SQL is not used — handled via special Python logic in run_migrations
        "SELECT 1;",
    ),
    (
        6,
        "Convert date/time columns from TEXT to TIMESTAMPTZ",
        # SQL is not used — handled via special Python logic in run_migrations
        "SELECT 1;",
    ),
    (
        7,
        "Enhance panchang_cache with extended data support via ON CONFLICT",
        "SELECT 1;",
    ),
    (
        8,
        "Add Lal Kitab tracker, chandra protocol, and journal tables",
        """
    CREATE TABLE IF NOT EXISTS lk_tracker_logs (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        user_id TEXT NOT NULL,
        kundli_id TEXT NOT NULL,
        date TEXT NOT NULL,
        completed_ids TEXT NOT NULL DEFAULT '[]',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        UNIQUE(user_id, kundli_id, date)
    );
    CREATE INDEX IF NOT EXISTS idx_lk_tracker_user_kundli ON lk_tracker_logs(user_id, kundli_id);

    CREATE TABLE IF NOT EXISTS lk_chandra_protocol (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        user_id TEXT NOT NULL UNIQUE,
        start_date TEXT,
        completed_days TEXT NOT NULL DEFAULT '[]',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_lk_chandra_user ON lk_chandra_protocol(user_id);

    CREATE TABLE IF NOT EXISTS lk_journal_entries (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        user_id TEXT NOT NULL,
        source TEXT NOT NULL,
        kundli_id TEXT,
        date TEXT NOT NULL,
        note TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_lk_journal_user ON lk_journal_entries(user_id, source);
    """,
    ),
    (
        10,
        "Add page_views table for frontend SPA traffic analytics",
        """
    CREATE TABLE IF NOT EXISTS page_views (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        path TEXT NOT NULL,
        session_id TEXT NOT NULL,
        user_id TEXT,
        referrer TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_pv_path ON page_views(path);
    CREATE INDEX IF NOT EXISTS idx_pv_session ON page_views(session_id);
    CREATE INDEX IF NOT EXISTS idx_pv_created ON page_views(created_at DESC);
    """,
    ),
    (
        9,
        "Add FK constraints with ON DELETE CASCADE for LK tables",
        # SQL not used — handled via _apply_lk_fk_constraints called in run_migrations
        "SELECT 1;",
    ),
    (
        12,
        "Add nishaniyan_master, lal_kitab_debts, remedies_master with full seed data",
        """
    CREATE TABLE IF NOT EXISTS nishaniyan_master (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        planet TEXT NOT NULL,
        house INTEGER NOT NULL CHECK (house BETWEEN 1 AND 12),
        nishani_text TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'general',
        severity TEXT NOT NULL DEFAULT 'moderate'
    );
    CREATE INDEX IF NOT EXISTS idx_nishaniyan_planet_house ON nishaniyan_master(planet, house);

    CREATE TABLE IF NOT EXISTS lal_kitab_debts (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        debt_type TEXT NOT NULL,
        planet TEXT NOT NULL,
        description TEXT NOT NULL,
        indication TEXT,
        remedy TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS remedies_master (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        planet TEXT NOT NULL,
        house INTEGER CHECK (house BETWEEN 1 AND 12),
        remedy_text TEXT NOT NULL,
        remedy_type TEXT NOT NULL DEFAULT 'other',
        duration_days INTEGER DEFAULT 43,
        instructions TEXT,
        caution TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_remedies_planet_house ON remedies_master(planet, house);

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('sun', 1, 'क्रोधी स्वभाव का होगा। सिर के बाल कम होंगे। बहुत ज़्यादा हिम्मती होगा। पत्नी हमेशा बीमार रहेगी या दब कर रहेगी।', 'general', 'moderate'),
    ('sun', 2, 'जातक के परिवार में 2 शादियाँ होंगी। भाई का तलाक़ हो जाता है। परिवार में औरतों की कमी रहेगी।', 'family', 'strong'),
    ('sun', 3, 'पड़ोस का घर उजड़ा होगा या पड़ोसी परेशान होगा। भाइयों और दोस्तों से अनबन रहती है।', 'general', 'moderate'),
    ('sun', 4, 'जातक मीठे का शौकीन होगा। घर में गच्चक, गुड़, चॉकलेट आएगा।', 'general', 'mild'),
    ('sun', 5, 'पेट हमेशा ख़राब ही रहता है। परिवार में दो शादियाँ ज़रूर होंगी।', 'health', 'moderate'),
    ('sun', 6, 'जातक का जन्म नानके में होता है या नानके निसर्ग होम के पैसे भरते हैं। गुप्त शत्रु ज़्यादा बनते हैं।', 'general', 'moderate'),
    ('sun', 7, 'घर में गुड़, गच्चक, चॉकलेट गिफ़्ट आती है। प्रेम विवाह करने के योग।', 'marriage', 'moderate'),
    ('sun', 8, 'जातक की पत्नी घर के भेद बाहर बताएगी। मुकदमे में बार बार हार होती है।', 'marriage', 'strong'),
    ('sun', 9, 'घर में पीतल के बड़े बर्तन खाली पड़े होंगे। जब भी मकान बदलेगा खुद पे या पिता पे कष्ट आएगा।', 'general', 'moderate'),
    ('sun', 10, 'घर में खोटे सिक्के पड़े होंगे। जहाँ काम कम पैसों में हो सकता है यह ज़्यादा पैसे दे के आएगा।', 'wealth', 'moderate'),
    ('sun', 11, 'जातक का ससुर जीवित नहीं रहेगा। नेकी करेगा तो बदनामी मिलेगी।', 'family', 'strong'),
    ('sun', 12, 'जातक को मोबाइल गिफ़्ट मिलता है। उच्च रक्तचाप रहेगा।', 'health', 'moderate');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('jupiter', 1, 'जातक अमीर बनाता है। शिक्षा भले ही कम हो फिर भी पड़े लिखों का बाप होगा। जातक स्वस्थ रहेगा और दुश्मनों से कभी नहीं डरेगा।', 'general', 'mild'),
    ('jupiter', 2, 'घर के बाहर सड़क टूटी होगी या गटर का ढक्कन होगा। घर की दीवारें रंग बिरंगी या पपड़ियाँ उतरी हुई होंगी। गुरु गंटाल योग के बाद भोग या भोग के बाद योग करने वाला।', 'general', 'moderate'),
    ('jupiter', 3, 'गद्दे-बिस्तरे को आग लगी हुई या कार की सीट जली हुई। एक ही दिशा में तीन दरवाज़े या तीन खिड़कियाँ। घर में तीन कुकर या पतीले।', 'general', 'moderate'),
    ('jupiter', 4, 'घर में किश्ती की फ़ोटो या स्टैचू होगा। घर का कोई बुजुर्ग सन्यासी होगा। माता का चेहरा गोल और तेजवान होगा।', 'family', 'mild'),
    ('jupiter', 5, 'दाँत पीले होंगे। घर में कोई टीचर या टीचिंग क्लास देने वाला होगा। कोई ज्योतिषी या धार्मिक इंसान मित्र होगा।', 'general', 'mild'),
    ('jupiter', 6, 'घर के पास कोई धार्मिक स्थान होगा। जातक शत्रुओं पर भारी रहेगा। गुरु अशुभ हो तो पेट की बीमारियाँ होंगी।', 'health', 'moderate'),
    ('jupiter', 7, 'शादी के बाद किस्मत खुलेगी। पत्नी धार्मिक और संस्कारी होगी। ससुराल में बड़ा मकान या जमीन होगी।', 'marriage', 'mild'),
    ('jupiter', 8, 'पारिवारिक संपत्ति विरासत में मिलेगी। 42 साल के बाद उन्नति होगी। गुप्त विद्याओं में रुचि होगी।', 'wealth', 'moderate'),
    ('jupiter', 9, 'भाग्य उज्ज्वल होगा। धार्मिक यात्राओं से लाभ। बड़े लोगों का आशीर्वाद मिलता रहेगा।', 'general', 'mild'),
    ('jupiter', 10, 'सरकारी या बड़े पद पर होगा। यश और कीर्ति मिलेगी। पिता का व्यवसाय आगे बढ़ाएगा।', 'career', 'mild'),
    ('jupiter', 11, 'बड़े भाई या बहन की मदद से उन्नति होगी। मित्रों का दायरा बड़ा होगा। लाभ के अनेक स्रोत होंगे।', 'wealth', 'mild'),
    ('jupiter', 12, 'विदेश यात्रा का योग। आध्यात्मिक जीवन की ओर झुकाव। खर्च अधिक होगा लेकिन धर्म के काम में।', 'general', 'mild');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('moon', 1, 'नज़ला जुकाम बहुत जल्दी होता है। घर में एंटीबायऑटिक दवाई होती है। हरी सब्जियाँ खाने का शौकीन।', 'health', 'mild'),
    ('moon', 2, 'भगवान शंकर की मूर्तियाँ और शंख, सर्प, शिवलिंग होंगे। नशे या नींद की दवाई खाता होगा। जली हुई प्रेस या खराब मिक्सी होगी।', 'general', 'moderate'),
    ('moon', 3, 'कमज़ोर दिल का होगा। रिश्तेदारों और भाइयों से अनबन रहती है। माता को नसों की परेशानी होगी।', 'health', 'moderate'),
    ('moon', 4, 'बनियान फटी हुई होगी। माता का अपमान करता है। कंजूस होता है।', 'family', 'strong'),
    ('moon', 5, 'संतान प्रिय होगा। बच्चे धार्मिक और आज्ञाकारी होंगे। पेट में गड़बड़ी होने के योग।', 'health', 'mild'),
    ('moon', 6, 'माता की सेहत कमज़ोर रहेगी। शत्रु गुप्त होंगे। मानसिक अशांति रहेगी।', 'health', 'moderate'),
    ('moon', 7, 'पत्नी सुंदर और भावुक होगी। वैवाहिक जीवन में उतार चढ़ाव। पत्नी की सेहत ध्यान देने योग्य।', 'marriage', 'moderate'),
    ('moon', 8, 'माता को कष्ट होने के योग। अचानक धन लाभ या हानि। गुप्त बातें दूसरों को पता चलेंगी।', 'wealth', 'strong'),
    ('moon', 9, 'भाग्य माता के आशीर्वाद पर निर्भर। धार्मिक यात्राओं से लाभ। विदेश से धन आने के योग।', 'general', 'mild'),
    ('moon', 10, 'माता की तरह दयालु और नर्म दिल। व्यापार में उतार चढ़ाव। जनता में लोकप्रियता।', 'career', 'mild'),
    ('moon', 11, 'मित्रों से सहायता मिलती रहेगी। बड़ी बहन का योग। पानी और दूध से व्यापार शुभ।', 'wealth', 'mild'),
    ('moon', 12, 'विदेश यात्रा के योग। अकेलापन महसूस होगा। खर्च पर नियंत्रण ज़रूरी।', 'general', 'moderate');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('venus', 1, 'पत्नी बीमार रहती है। जिसपे दिल आ गया उसके लिए जान कुर्बान कर देगा। दिन में भी प्रेम के सपने देखने वाला।', 'marriage', 'moderate'),
    ('venus', 2, 'घर शेरमुखी होगा। पत्नी घर की बॉस होगी। नीली जींस और सफेद शर्ट पहनने की आदत या शौकीन।', 'family', 'moderate'),
    ('venus', 3, 'कला का पुजारी होगा। शत्रुओं से डरने वाला। घर की नौकरानी या पड़ोसन से अत्यधिक नजदीकी।', 'general', 'strong'),
    ('venus', 4, 'दो पत्नियों के योग। सुख सुविधाओं का शौकीन। शादी के 4 वर्ष बाद भाग्य उदय होता है।', 'marriage', 'strong'),
    ('venus', 5, 'रोमांटिक स्वभाव। संतान सुंदर और गुणी होगी। कला और संगीत में रुचि।', 'marriage', 'mild'),
    ('venus', 6, 'स्वास्थ्य में परेशानी। ऋण लेने के योग। विरोधियों से सतर्क रहना होगा।', 'health', 'moderate'),
    ('venus', 7, 'सुंदर और संस्कारी पत्नी। वैवाहिक जीवन सुखद। व्यापारिक साझेदारी से लाभ।', 'marriage', 'mild'),
    ('venus', 8, 'ससुराल से धन लाभ। गुप्त संबंध बनने के योग। दुर्घटना का भय।', 'wealth', 'moderate'),
    ('venus', 9, 'भाग्यशाली। धार्मिक कार्यों में रुचि। विदेश यात्रा से लाभ।', 'general', 'mild'),
    ('venus', 10, 'कला, फिल्म, फैशन के क्षेत्र में सफलता। सरकार से लाभ। व्यापार में उन्नति।', 'career', 'mild'),
    ('venus', 11, 'मित्रों से सहायता। बड़ी बहन होगी। धन संचय के योग।', 'wealth', 'mild'),
    ('venus', 12, 'विदेश में स्थायी निवास का योग। गुप्त प्रेम संबंध। खर्च अधिक होगा।', 'general', 'moderate');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('mars', 1, 'परिवार में कोई यूनीफॉर्म पहन कर काम करने वाला होता है। शरीर को चुस्त दरुस्त रखने वाला। जातक के सिर या माथे पे चोट का निशान होता है।', 'health', 'moderate'),
    ('mars', 2, 'मसालेदार, फास्ट फूड तंदूरी खाने का शौकीन। मीठा बनकर दूसरों को ठगने वाला। सच का साथ देने वाला और सच बोलने वाला।', 'general', 'moderate'),
    ('mars', 3, 'भाइयों के साथ झगड़े होंगे। साहसी और निडर होगा। दुर्घटनाओं का खतरा रहेगा।', 'health', 'strong'),
    ('mars', 4, 'माता के साथ झगड़े। घर में आग लगने का खतरा। संपत्ति विवाद के योग।', 'family', 'strong'),
    ('mars', 5, 'पहला बच्चा लड़का होने के योग। संतान सुख में कमी। जुआ सट्टे में नुकसान।', 'family', 'moderate'),
    ('mars', 6, 'शत्रुओं पर विजय। शरीर में रक्त संबंधी रोग। सेना, पुलिस में सेवा योग।', 'health', 'moderate'),
    ('mars', 7, 'मंगली योग। पति-पत्नी में झगड़े। विवाह में देरी या परेशानी।', 'marriage', 'strong'),
    ('mars', 8, 'अचानक आघात का भय। पैतृक संपत्ति को लेकर विवाद। 28 वर्ष के बाद उन्नति।', 'wealth', 'strong'),
    ('mars', 9, 'पिता के साथ विचार नहीं मिलते। धर्म के प्रति संशय। विदेश यात्रा में बाधाएं।', 'family', 'moderate'),
    ('mars', 10, 'कार्यक्षेत्र में प्रतिस्पर्धा। सरकारी काम में सफलता। इंजीनियरिंग, सेना में करियर।', 'career', 'mild'),
    ('mars', 11, 'बड़े भाई से विरोध। मित्र विश्वासघात करेंगे। धन लाभ संघर्ष के बाद।', 'wealth', 'moderate'),
    ('mars', 12, 'गुप्त शत्रु अधिक। खर्च अनियंत्रित। विदेश में संघर्ष।', 'general', 'strong');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('mercury', 1, 'परिवार में कोई गायक होगा या खुद बाथरूम सिंगर होगा। जुबान का कच्चा होगा। चापलूस और शरारती होगा।', 'general', 'moderate'),
    ('mercury', 2, 'घर में बंद घड़ियाँ, पुराने चश्मे, हरी बोतलें होंगी। दाँत टेढ़े-मेढ़े या एक दूसरे के ऊपर चढ़े हुए होंगे। टूटे हेडफोन या चार्जिंग केबल बेड बॉक्स में होंगी।', 'general', 'moderate'),
    ('mercury', 3, 'पढ़ने-लिखने में कुशल। व्यापारिक बुद्धि तीव्र। भाई-बहनों के साथ मधुर संबंध।', 'career', 'mild'),
    ('mercury', 4, 'माता पढ़ी-लिखी और बुद्धिमान होगी। घर में किताबें और पढ़ाई का माहौल। संपत्ति को लेकर तर्क-वितर्क।', 'family', 'mild'),
    ('mercury', 5, 'संतान बुद्धिमान और पढ़ी-लिखी होगी। लेखन, शिक्षा, गणित में रुचि। अटकलों से नुकसान।', 'family', 'mild'),
    ('mercury', 6, 'बुद्धि से शत्रुओं को हराएगा। चालाकी से काम लेगा। स्वास्थ्य में पेट और त्वचा की परेशानी।', 'health', 'moderate'),
    ('mercury', 7, 'पत्नी बुद्धिमान और व्यापारिक। साझेदारी में धोखे का भय। विवाह में चालाकी से काम।', 'marriage', 'moderate'),
    ('mercury', 8, 'गुप्त ज्ञान में रुचि। पैतृक संपत्ति में विवाद। जीवनकाल में अचानक परिवर्तन।', 'wealth', 'moderate'),
    ('mercury', 9, 'लेखन, अध्यापन, ज्योतिष में सफलता। धार्मिक बुद्धि तीव्र। विदेश से ज्ञान प्राप्ति।', 'career', 'mild'),
    ('mercury', 10, 'व्यापार में सफलता। लेखक, पत्रकार, वकील बनने के योग। बुद्धि से उच्च पद।', 'career', 'mild'),
    ('mercury', 11, 'व्यापारिक मित्र फायदेमंद। बहन का विशेष सहयोग। आय के अनेक स्रोत।', 'wealth', 'mild'),
    ('mercury', 12, 'विदेश में बसने के योग। गुप्त अध्ययन में रुचि। खर्च पर नियंत्रण ज़रूरी।', 'general', 'mild');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('saturn', 1, 'घर में शराब रखी होगी। नज़र कमज़ोर और क्रोधी स्वभाव का होगा। अपने राज़ किसी को आसानी से न बतायेगा।', 'general', 'strong'),
    ('saturn', 2, 'अधूरी पढ़ाई। पत्नी चालाक होगी। छत से गिरने या सिर पे चोट लगने के योग।', 'health', 'strong'),
    ('saturn', 3, 'भाइयों से विरोध। कड़ी मेहनत के बाद सफलता। यात्राओं में बाधाएं।', 'family', 'moderate'),
    ('saturn', 4, 'माता को कष्ट। मकान में देरी। पुराना मकान या जमीन होगी।', 'family', 'strong'),
    ('saturn', 5, 'संतान सुख में विलंब। पहली संतान कष्ट में। शिक्षा में रुकावट।', 'family', 'strong'),
    ('saturn', 6, 'शत्रुओं पर विजय देर से मिलेगी। दीर्घकालीन रोग। नौकरों से परेशानी।', 'health', 'moderate'),
    ('saturn', 7, 'विवाह में देरी। पत्नी बड़ी उम्र की। वैवाहिक जीवन में संघर्ष।', 'marriage', 'strong'),
    ('saturn', 8, 'दीर्घायु। पैतृक संपत्ति में विवाद। 36 वर्ष के बाद उन्नति।', 'wealth', 'moderate'),
    ('saturn', 9, 'पिता को कष्ट। धर्म के प्रति उदासीनता। किस्मत देर से जागेगी।', 'family', 'strong'),
    ('saturn', 10, 'उच्च पद देर से मिलेगा। कड़ी मेहनत से सफलता। पदावनति का भय।', 'career', 'moderate'),
    ('saturn', 11, 'बड़े भाई को कष्ट। मित्रों से धोखे का भय। धन संचय धीरे-धीरे।', 'wealth', 'moderate'),
    ('saturn', 12, 'जेल, अस्पताल, विदेश का योग। एकांतवास की इच्छा। गुप्त शत्रु अधिक।', 'general', 'strong');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('rahu', 1, 'कभी एक जगह टिक के काम नहीं करेगा। दो शादियों के योग। बहुत ज़्यादा और खामखां बोलने वाला।', 'general', 'strong'),
    ('rahu', 2, 'घर से एक बार ज़रूर भागेगा। घर में दिन में चोरी हो सकती है। नेत्र रोगी और माता या बीवी का अपमान करने वाला।', 'health', 'strong'),
    ('rahu', 3, 'भाइयों से अनबन। झूठ बोलने की आदत। यात्राओं से धन हानि।', 'family', 'strong'),
    ('rahu', 4, 'माता का अचानक स्वास्थ्य बिगड़ना। घर में बार-बार परिवर्तन। संपत्ति विवाद।', 'family', 'strong'),
    ('rahu', 5, 'संतान को कष्ट। जुआ-सट्टे में नुकसान। प्रेम संबंधों में धोखा।', 'family', 'strong'),
    ('rahu', 6, 'गुप्त शत्रु। चर्म रोग या नशे की लत। कर्ज से परेशानी।', 'health', 'strong'),
    ('rahu', 7, 'विवाह में देरी या परेशानी। साझेदार से धोखा। पत्नी का स्वास्थ्य ठीक नहीं।', 'marriage', 'strong'),
    ('rahu', 8, 'अचानक धन हानि। दुर्घटना का भय। गुप्त शत्रु जानलेवा।', 'wealth', 'strong'),
    ('rahu', 9, 'पिता को कष्ट। धर्म के प्रति भ्रम। विदेश यात्रा में बाधाएं।', 'family', 'moderate'),
    ('rahu', 10, 'करियर में अचानक उठान या पतन। सरकारी कामों में बाधाएं। झूठ से काम चलाएगा।', 'career', 'strong'),
    ('rahu', 11, 'मित्र विश्वासघाती। धन अचानक मिलेगा और जाएगा। बड़े भाई को कष्ट।', 'wealth', 'moderate'),
    ('rahu', 12, 'विदेश में बसने के योग लेकिन परेशानी। गुप्त शत्रु। खर्च बेहद अधिक।', 'general', 'strong');

    INSERT INTO nishaniyan_master (planet, house, nishani_text, category, severity) VALUES
    ('ketu', 1, 'वात रोग सर दर्द और विधवा स्त्री से झगड़ा करने वाला। परिवार में किसी को शुगर हो सकती है। रिश्तेदारों से अनबन रहेगी।', 'health', 'moderate'),
    ('ketu', 2, 'परिवार में कोई बहुत सड़े मिज़ाज का होगा। जातक खुद या परिवार में किसी को किसी और ने पाला होगा। पतंग की डोर, केबल के गुच्छे, ऊन के गोले घर में होंगे।', 'family', 'strong'),
    ('ketu', 3, 'भाई-बहनों के साथ तनाव। साहस की कमी। धार्मिक यात्राओं में बाधाएं।', 'family', 'moderate'),
    ('ketu', 4, 'माता को कष्ट। पुराने घर में रहने के योग। माता की सेहत चिंताजनक।', 'family', 'strong'),
    ('ketu', 5, 'संतान कम। पहला बच्चा कष्ट में। आध्यात्मिक संतान होगी।', 'family', 'strong'),
    ('ketu', 6, 'रोग जल्दी ठीक होंगे। गुप्त शत्रु नष्ट होंगे। पेट के रोगों से सावधानी।', 'health', 'moderate'),
    ('ketu', 7, 'विवाह में परेशानी। पति-पत्नी में दूरी। साझेदार से झगड़ा।', 'marriage', 'strong'),
    ('ketu', 8, 'दीर्घायु। पैतृक संपत्ति में हानि। रहस्यमयी जीवन।', 'wealth', 'moderate'),
    ('ketu', 9, 'पिता का साथ नहीं मिलेगा। धर्म में संशय। भाग्य साथ नहीं देगा।', 'family', 'strong'),
    ('ketu', 10, 'करियर में रुकावटें। ध्यान भटकेगा। आध्यात्मिक कार्यों से सफलता।', 'career', 'moderate'),
    ('ketu', 11, 'मित्रों से लाभ कम। बड़े भाई की परेशानी। धन संचय कठिन।', 'wealth', 'moderate'),
    ('ketu', 12, 'मोक्ष की साधना करेगा। विदेश में सुख। एकांतवास में रुचि।', 'general', 'mild');

    INSERT INTO lal_kitab_debts (debt_type, planet, description, indication, remedy) VALUES
    ('पितृ ऋण', 'sun', 'पिता या पूर्वजों से संबंधित ऋण', 'सूर्य खराब हो, पिता से अनबन, आंखों की समस्या', 'तांबे के बर्तन में गंगाजल रखें, पिता का आशीर्वाद लें'),
    ('मातृ ऋण', 'moon', 'माता से संबंधित ऋण', 'चंद्रमा खराब हो, माता से अनबन, मानसिक तनाव', 'चांदी का चौकोर टुकड़ा रखें, माता की सेवा करें'),
    ('भ्रातृ ऋण', 'mars', 'भाई-बहनों से संबंधित ऋण', 'मंगल खराब हो, भाइयों से झगड़े, रक्त संबंधी रोग', 'लाल मसूर की दाल दान करें, भाई का सम्मान करें'),
    ('देव ऋण', 'jupiter', 'देवताओं या गुरु से संबंधित ऋण', 'गुरु खराब हो, संतान संबंधी समस्याएं', 'पीपल के पेड़ की पूजा करें, ब्राह्मण को भोजन कराएं'),
    ('स्त्री ऋण', 'venus', 'स्त्रियों से संबंधित ऋण', 'शुक्र खराब हो, वैवाहिक समस्याएं', 'गाय की सेवा करें, पत्नी का सम्मान करें'),
    ('शत्रु ऋण', 'saturn', 'शत्रुओं या कर्म से संबंधित ऋण', 'शनि खराब हो, देरी से सफलता, शारीरिक पीड़ा', 'शनिवार को तेल दान करें, काले कुत्ते को रोटी खिलाएं'),
    ('पितामह ऋण', 'rahu', 'पूर्वजों या नाना से संबंधित ऋण', 'राहु खराब हो, गुप्त शत्रु, नशे की लत', '400 ग्राम सीसा बहते पानी में डालें, नाना का सम्मान करें'),
    ('प्रपितामह ऋण', 'ketu', 'पूर्वजों या दादा से संबंधित ऋण', 'केतु खराब हो, आध्यात्मिक भ्रम, अकाल मृत्यु का भय', 'बंदरों को गुड़ खिलाएं, केसर का तिलक लगाएं');

    INSERT INTO remedies_master (planet, house, remedy_text, remedy_type, duration_days, instructions) VALUES
    ('sun', 1, 'रूबी धारण करें। बंदरों को गुड़ खिलाएं। तांबे के सांप जल में प्रवाहित करें।', 'gemstone', 43, 'सूर्योदय के समय जल अर्पित करें'),
    ('sun', 2, 'गेहूं, गुड़ और लोहे की कड़ाही का दान करें। नारियल, बादाम और तेल का दान करें।', 'donation', 43, 'रविवार को दान करें'),
    ('sun', 3, 'सूर्य को गुड़ मिलाकर जल चढ़ाएं। कुएं में चांदी का टुकड़ा डालें।', 'worship', 43, 'प्रतिदिन सुबह करें'),
    ('moon', 1, 'माता का आशीर्वाद लें। चांदी के बर्तन में दूध पिएं। चाँदी धारण करें।', 'worship', 43, 'हर सोमवार करें'),
    ('moon', 2, 'घर में शंख, घड़ियाल न रखें। ससुराल से चाँदी की ईंट लें। कन्या पूजन करें।', 'donation', 43, 'सोमवार को करें'),
    ('mars', 1, 'मूंगा धारण करें। हनुमान जी को सिंदूर चढ़ाएं। एक घड़े में गुड़ भरकर ज़मीन में दबाएं।', 'gemstone', 43, 'मंगलवार से शुरू करें'),
    ('mars', 7, 'मंगलवार को हनुमान चालीसा पढ़ें। मसूर दाल दान करें। मूंगा धारण करें।', 'worship', 43, 'मंगलवार को करें'),
    ('jupiter', 1, 'पीला पुखराज धारण करें। मिट्टी की कुज्जी में शक्कर भरकर कच्ची जमीन में दबाएं।', 'gemstone', 43, 'गुरुवार से शुरू करें'),
    ('jupiter', 2, 'सांप को दूध पिलाना। सोने में ब्राजील का पुखराज धारण करना।', 'worship', 43, 'गुरुवार को दूध पिलाएं'),
    ('venus', 1, 'हीरा या ओपल धारण करें। गाय की सेवा करें। शुक्रवार को उपवास रखें।', 'gemstone', 43, 'शुक्रवार से शुरू करें'),
    ('venus', 2, 'बेल्जियम का हीरा धारण करें। गाय को हल्दी पीले आलू खिलाएं।', 'gemstone', 43, 'शुक्रवार को करें'),
    ('mercury', 1, 'पन्ना धारण करें। फिटकरी से दाँत साफ करें। दुर्गा सप्तशती का पाठ करें।', 'gemstone', 43, 'बुधवार से शुरू करें'),
    ('saturn', 1, 'नीलम या काले घोड़े की नाल की अंगूठी। सुरमा कच्ची ज़मीन में दबाएं। बंदर पालें।', 'gemstone', 43, 'शनिवार से शुरू करें'),
    ('saturn', 2, 'नंगे पैर मंदिर जाएं। गुरु की सेवा करें। भूरी भैंस की सेवा करें।', 'worship', 43, 'हर शनिवार करें'),
    ('rahu', 1, '400 ग्राम सीसा बहते पानी में डालें। गले में चाँदी पहनें।', 'donation', 43, 'शनिवार को करें'),
    ('rahu', 2, 'चाँदी की ठोस गोली गले में पहनें। हाथी के पैरों की मिट्टी कुएं में डालें।', 'gemstone', 43, 'शनिवार को करें'),
    ('ketu', 1, 'बंदरों को गुड़ खिलाएं। केसर का तिलक लगाएं। गणेश पूजन करें।', 'worship', 43, 'प्रतिदिन करें'),
    ('ketu', 2, 'काले-सफेद कुतिया रखें। इमली-तिल मंदिर में दान करें। केसर का तिलक लगाएं।', 'worship', 43, 'बुधवार को करें');
        """,
    ),
    (
        13,
        "Add saved_predictions table for user-bookmarked LK predictions",
        """
    CREATE TABLE IF NOT EXISTS saved_predictions (
        id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        user_id TEXT NOT NULL,
        kundli_id TEXT NOT NULL,
        prediction_type TEXT NOT NULL,
        prediction_data TEXT NOT NULL DEFAULT '{}',
        note TEXT NOT NULL DEFAULT '',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_saved_predictions_user_kundli ON saved_predictions(user_id, kundli_id);
    CREATE INDEX IF NOT EXISTS idx_saved_predictions_created ON saved_predictions(created_at DESC);
    """,
    ),
    (
        11,
        "Add feedback table — user ratings, text, action_taken, admin_remarks",
        """
    CREATE TABLE IF NOT EXISTS feedback (
        id           TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
        user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        rating_interface    INTEGER CHECK(rating_interface    BETWEEN 1 AND 5),
        rating_reports      INTEGER CHECK(rating_reports      BETWEEN 1 AND 5),
        rating_calculations INTEGER CHECK(rating_calculations BETWEEN 1 AND 5),
        feedback_text TEXT,
        status       TEXT NOT NULL DEFAULT 'open'
                     CHECK(status IN ('open','closed')),
        action_taken TEXT NOT NULL DEFAULT 'NR'
                     CHECK(action_taken IN ('yes','no','NR')),
        admin_remarks TEXT,
        created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_feedback_user    ON feedback(user_id);
    CREATE INDEX IF NOT EXISTS idx_feedback_status  ON feedback(status);
    CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback(created_at DESC);
    """,
    ),
    (
        15,
        "Add kundli_id columns to ai_chat_logs and reports",
        """
        ALTER TABLE ai_chat_logs ADD COLUMN IF NOT EXISTS kundli_id TEXT REFERENCES kundlis(id) ON DELETE CASCADE;
        ALTER TABLE reports ADD COLUMN IF NOT EXISTS kundli_id TEXT REFERENCES kundlis(id) ON DELETE CASCADE;
        """,
    ),
    (
        14,
        "Add nishani_text_en column to nishaniyan_master and populate English translations",
        """
    ALTER TABLE nishaniyan_master ADD COLUMN IF NOT EXISTS nishani_text_en TEXT NOT NULL DEFAULT '';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Short-tempered by nature. Hair tends to be sparse. Very courageous. Wife will often be unwell or subdued.'
        WHEN 2  THEN 'Two marriages will occur in the family. Brother''s marriage may end in divorce. Women will be fewer in the family.'
        WHEN 3  THEN 'Neighbor''s house will be empty or neighbor will be in trouble. Disagreements with brothers and friends persist.'
        WHEN 4  THEN 'Native is fond of sweets. Jaggery, gachak, and chocolates frequently come to the home.'
        WHEN 5  THEN 'Stomach is frequently disturbed. Two marriages will certainly occur in the family.'
        WHEN 6  THEN 'Native is born at maternal grandparents'' home or they bear the delivery expenses. Many hidden enemies.'
        WHEN 7  THEN 'Jaggery, gachak, chocolates come as gifts at home. Chances of a love marriage.'
        WHEN 8  THEN 'Wife will reveal family secrets to others. Repeated defeats in court cases.'
        WHEN 9  THEN 'Large brass utensils will lie empty at home. Whenever the house changes, hardship comes to self or father.'
        WHEN 10 THEN 'Counterfeit coins will be found at home. Will pay more for work that could be done cheaply.'
        WHEN 11 THEN 'Father-in-law will not survive long. Acts of kindness will bring disrepute.'
        WHEN 12 THEN 'Native receives a mobile phone as a gift. High blood pressure is likely.'
        ELSE '' END
    WHERE planet = 'sun';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Native becomes wealthy. Even with less education will be wiser than the educated. Healthy and fearless of enemies.'
        WHEN 2  THEN 'Road outside home will be broken or have a drain cover. Walls will be multicolored or with peeling paint. Alternates between worldly pleasures and spiritual practice.'
        WHEN 3  THEN 'Mattress or car seat will be burnt or scorched. Three doors or windows in one direction. Three pressure cookers or pots in the home.'
        WHEN 4  THEN 'A boat photo or statuette will be in the home. An elderly family member will be a renunciant. Mother''s face will be round and radiant.'
        WHEN 5  THEN 'Teeth will be yellowish. A teacher or coaching instructor will be in the family. A friend will be an astrologer or religious person.'
        WHEN 6  THEN 'A religious place will be near the home. Will overcome enemies. If Jupiter is malefic, digestive ailments will arise.'
        WHEN 7  THEN 'Fortune opens after marriage. Wife will be religious and cultured. In-laws will have a large house or land.'
        WHEN 8  THEN 'Ancestral property will be inherited. Progress after age 42. Interest in occult sciences.'
        WHEN 9  THEN 'Fortune will be bright. Gain from religious travel. Blessings of elders will continue.'
        WHEN 10 THEN 'Will hold government or senior position. Fame and renown. Will carry forward father''s business.'
        WHEN 11 THEN 'Progress with help of elder sibling. Wide circle of friends. Multiple sources of income.'
        WHEN 12 THEN 'Chance of foreign travel. Inclination toward spiritual life. High expenses but in religious work.'
        ELSE '' END
    WHERE planet = 'jupiter';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Prone to colds and sinus issues. Antibiotics often found at home. Fond of eating green vegetables.'
        WHEN 2  THEN 'Shiva idols, conch shells, and Shivalingas will be in the home. May use intoxicants or sleep medication. A burnt iron or broken mixer in the house.'
        WHEN 3  THEN 'Emotionally sensitive. Disagreements with relatives and brothers persist. Mother will have nerve-related issues.'
        WHEN 4  THEN 'Undershirt will often be torn. Disrespects mother. Tends to be miserly.'
        WHEN 5  THEN 'Affectionate toward children. Children will be religious and obedient. Chances of digestive disturbances.'
        WHEN 6  THEN 'Mother''s health will be weak. Enemies will be hidden. Mental restlessness will persist.'
        WHEN 7  THEN 'Wife will be beautiful and emotional. Ups and downs in married life. Wife''s health needs attention.'
        WHEN 8  THEN 'Mother may face hardship. Sudden financial gain or loss. Secret matters will become known to others.'
        WHEN 9  THEN 'Fortune depends on mother''s blessings. Gains from religious travel. Chances of money coming from abroad.'
        WHEN 10 THEN 'Compassionate and soft-hearted like mother. Fluctuations in business. Popular among the masses.'
        WHEN 11 THEN 'Friends will continue to help. Likely to have an elder sister. Business in water and milk is auspicious.'
        WHEN 12 THEN 'Chances of foreign travel. Will feel loneliness. Expenditure control is necessary.'
        ELSE '' END
    WHERE planet = 'moon';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Wife remains unwell. Will sacrifice everything for someone they fall in love with. Daydreams about romance constantly.'
        WHEN 2  THEN 'House will be triangular or sher-mukhi shaped. Wife will be the boss at home. Fond of wearing blue jeans and white shirt.'
        WHEN 3  THEN 'A devotee of the arts. Tends to fear enemies. Excessive closeness with household help or neighbor.'
        WHEN 4  THEN 'Chances of two marriages. Very fond of comforts and luxuries. Fortune rises 4 years after marriage.'
        WHEN 5  THEN 'Romantic by nature. Children will be beautiful and virtuous. Interest in arts and music.'
        WHEN 6  THEN 'Health troubles. Prone to taking on debt. Must be cautious of opponents.'
        WHEN 7  THEN 'Beautiful and cultured wife. Happy married life. Gains from business partnerships.'
        WHEN 8  THEN 'Financial gain from in-laws. Chances of secret relationships. Fear of accidents.'
        WHEN 9  THEN 'Lucky. Interest in religious activities. Gains from foreign travel.'
        WHEN 10 THEN 'Success in arts, film, or fashion. Benefits from government. Growth in business.'
        WHEN 11 THEN 'Support from friends. Will have an elder sister. Chances of wealth accumulation.'
        WHEN 12 THEN 'Chances of permanent settlement abroad. Secret love affairs. Expenditure will be high.'
        ELSE '' END
    WHERE planet = 'venus';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Someone in the family works in uniform. Physically fit and active. Scar on head or forehead.'
        WHEN 2  THEN 'Fond of spicy, fast food, and tandoori food. Pretends to be sweet-natured while deceiving others. Stands by truth and speaks honestly.'
        WHEN 3  THEN 'Disputes with brothers. Courageous and fearless. Risk of accidents.'
        WHEN 4  THEN 'Disputes with mother. Fire hazard at home. Property dispute chances.'
        WHEN 5  THEN 'First child likely to be a boy. Less happiness from children. Losses from gambling or speculation.'
        WHEN 6  THEN 'Victory over enemies. Blood-related disorders in the body. Good prospects for army or police service.'
        WHEN 7  THEN 'Manglik yoga. Disputes between husband and wife. Delay or trouble in marriage.'
        WHEN 8  THEN 'Fear of sudden trauma. Dispute over ancestral property. Progress after age 28.'
        WHEN 9  THEN 'Does not agree with father. Skeptical about religion. Obstacles in foreign travel.'
        WHEN 10 THEN 'Competition in the workplace. Success in government work. Career in engineering or armed forces.'
        WHEN 11 THEN 'Opposition from elder brother. Friends will betray. Financial gain after struggle.'
        WHEN 12 THEN 'Many hidden enemies. Uncontrolled expenses. Struggles abroad.'
        ELSE '' END
    WHERE planet = 'mars';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Someone in the family is a singer or is a bathroom singer. Loose-tongued. Flattering and mischievous.'
        WHEN 2  THEN 'Stopped clocks, old spectacles, green bottles found at home. Crooked or overlapping teeth. Broken headphones or charging cables in the bedside drawer.'
        WHEN 3  THEN 'Skilled in reading and writing. Sharp business mind. Harmonious relations with siblings.'
        WHEN 4  THEN 'Mother is educated and intelligent. Books and study atmosphere at home. Arguments over property.'
        WHEN 5  THEN 'Children will be intelligent and well-educated. Interest in writing, education, mathematics. Losses from speculation.'
        WHEN 6  THEN 'Will defeat enemies with intelligence. Uses cleverness at work. Health issues related to stomach and skin.'
        WHEN 7  THEN 'Wife is intelligent and business-minded. Risk of betrayal in partnerships. Uses cleverness in marriage matters.'
        WHEN 8  THEN 'Interest in occult knowledge. Dispute over ancestral property. Sudden changes during lifetime.'
        WHEN 9  THEN 'Success in writing, teaching, and astrology. Sharp religious intellect. Acquiring knowledge from abroad.'
        WHEN 10 THEN 'Success in business. Chances of becoming writer, journalist, or lawyer. High position through intellect.'
        WHEN 11 THEN 'Business-minded friends are beneficial. Special support from sister. Multiple sources of income.'
        WHEN 12 THEN 'Chances of settling abroad. Interest in secret studies. Expenditure control is necessary.'
        ELSE '' END
    WHERE planet = 'mercury';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Alcohol will be kept at home. Weak eyesight and irritable temperament. Will not easily reveal personal secrets.'
        WHEN 2  THEN 'Incomplete education. Wife will be cunning. Chances of falling from roof or head injury.'
        WHEN 3  THEN 'Opposition from brothers. Success only after hard work. Obstacles in journeys.'
        WHEN 4  THEN 'Hardship to mother. Delay in owning a home. Old house or land will be there.'
        WHEN 5  THEN 'Late child happiness. First child in distress. Obstacles in education.'
        WHEN 6  THEN 'Victory over enemies will come late. Chronic illness. Troubles from servants.'
        WHEN 7  THEN 'Late marriage. Wife will be older. Struggle in married life.'
        WHEN 8  THEN 'Long life. Dispute over ancestral property. Progress after age 36.'
        WHEN 9  THEN 'Hardship to father. Indifferent toward religion. Fortune will awaken late.'
        WHEN 10 THEN 'Senior position will come late. Success through hard work. Fear of demotion.'
        WHEN 11 THEN 'Elder brother in difficulty. Risk of betrayal by friends. Wealth accumulation is slow.'
        WHEN 12 THEN 'Chances of prison, hospital, or foreign country. Desire for seclusion. Many hidden enemies.'
        ELSE '' END
    WHERE planet = 'saturn';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Will never settle in one place for long. Chances of two marriages. Talks excessively and unnecessarily.'
        WHEN 2  THEN 'Will run away from home at least once. Day-time theft can happen at home. Suffers from eye disease; disrespects mother or wife.'
        WHEN 3  THEN 'Disputes with brothers. Habit of lying. Financial losses from travel.'
        WHEN 4  THEN 'Mother''s health may deteriorate suddenly. Frequent changes in home. Property disputes.'
        WHEN 5  THEN 'Children face hardship. Losses in gambling and speculation. Betrayal in love relationships.'
        WHEN 6  THEN 'Hidden enemies. Skin disease or addiction. Troubles from debt.'
        WHEN 7  THEN 'Delay or trouble in marriage. Betrayal by partner. Wife''s health not good.'
        WHEN 8  THEN 'Sudden financial loss. Fear of accidents. Hidden enemies are dangerous.'
        WHEN 9  THEN 'Hardship to father. Confusion about religion. Obstacles in foreign travel.'
        WHEN 10 THEN 'Sudden rise or fall in career. Obstacles in government work. Will use deception to manage.'
        WHEN 11 THEN 'Treacherous friends. Money will come and go suddenly. Elder brother in hardship.'
        WHEN 12 THEN 'Chances of settling abroad but with hardship. Hidden enemies. Very high expenditure.'
        ELSE '' END
    WHERE planet = 'rahu';

    UPDATE nishaniyan_master SET nishani_text_en = CASE house
        WHEN 1  THEN 'Vata disorders and headaches; quarrelsome with widows. Someone in family may have diabetes. Disputes with relatives.'
        WHEN 2  THEN 'Someone in family will be very ill-tempered. Native or family member was raised by someone else. Kite strings, cable bundles, or wool balls found in the house.'
        WHEN 3  THEN 'Tension with siblings. Lack of courage. Obstacles in religious journeys.'
        WHEN 4  THEN 'Hardship to mother. Likely to live in an old house. Mother''s health is concerning.'
        WHEN 5  THEN 'Few children. First child faces hardship. Children will be spiritually inclined.'
        WHEN 6  THEN 'Diseases will heal quickly. Hidden enemies will be destroyed. Caution regarding stomach ailments.'
        WHEN 7  THEN 'Trouble in marriage. Distance between husband and wife. Disputes with partner.'
        WHEN 8  THEN 'Long life. Loss in ancestral property. Mysterious life.'
        WHEN 9  THEN 'Will not receive father''s support. Doubt about religion. Fortune will not be supportive.'
        WHEN 10 THEN 'Obstacles in career. Mind will wander. Success through spiritual work.'
        WHEN 11 THEN 'Less benefit from friends. Elder brother''s hardship. Wealth accumulation is difficult.'
        WHEN 12 THEN 'Will seek spiritual liberation. Happiness abroad. Interest in solitude.'
        ELSE '' END
    WHERE planet = 'ketu';
    """,
    ),
    (16, "download_tokens table + pending_astrologer role", """
    CREATE TABLE IF NOT EXISTS download_tokens (
        token TEXT PRIMARY KEY,
        kundli_id TEXT NOT NULL REFERENCES kundlis(id) ON DELETE CASCADE,
        user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        expires_at TIMESTAMPTZ NOT NULL
    );
    ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check;
    ALTER TABLE users ADD CONSTRAINT users_role_check CHECK(role IN ('user','astrologer','pending_astrologer','admin'));
    """),
    (17, "guest_kundlis table", """
CREATE TABLE IF NOT EXISTS guest_kundlis (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    birth_time TEXT NOT NULL,
    birth_place TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timezone_offset DOUBLE PRECISION DEFAULT 5.5,
    gender TEXT DEFAULT 'male',
    marketing_consent BOOLEAN DEFAULT false,
    visit_count INTEGER DEFAULT 1,
    chart_data TEXT,
    preview_data TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_visited_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_guest_email ON guest_kundlis(email);
CREATE INDEX IF NOT EXISTS idx_guest_phone ON guest_kundlis(phone);
    """),
    (18, "lk_prediction_feedback table — per-kundli prediction ratings", """
CREATE TABLE IF NOT EXISTS lk_prediction_feedback (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kundli_id TEXT NOT NULL REFERENCES kundlis(id) ON DELETE CASCADE,
    feedback JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, kundli_id)
);
CREATE INDEX IF NOT EXISTS idx_lk_pred_feedback_user_kundli ON lk_prediction_feedback(user_id, kundli_id);
    """),
    (19, "P2.1/P2.7/P2.8 — Farmaan DB + Source library + Rights provenance", """
CREATE TABLE IF NOT EXISTS lk_source_library (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    edition_year INTEGER NOT NULL,
    edition_label TEXT NOT NULL,
    volume TEXT,
    chapter TEXT,
    section_ref TEXT,
    page_number INTEGER,
    language TEXT NOT NULL,
    script TEXT NOT NULL,
    source_type TEXT NOT NULL,
    body TEXT NOT NULL,
    body_normalised TEXT,
    scan_url TEXT,
    contributor TEXT,
    verification_status TEXT NOT NULL DEFAULT 'unverified',
    rights_status TEXT NOT NULL DEFAULT 'commercial_unclear',
    rights_note TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_source_lib_edition ON lk_source_library(edition_year);
CREATE INDEX IF NOT EXISTS idx_source_lib_section ON lk_source_library(section_ref);
CREATE INDEX IF NOT EXISTS idx_source_lib_lang_script ON lk_source_library(language, script);
CREATE INDEX IF NOT EXISTS idx_source_lib_rights ON lk_source_library(rights_status);

CREATE TABLE IF NOT EXISTS lk_farmaan (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    farmaan_number INTEGER UNIQUE,
    urdu_script TEXT NOT NULL,
    urdu_latin TEXT,
    hindi TEXT,
    english TEXT,
    traditional_commentary_en TEXT,
    traditional_commentary_hi TEXT,
    modern_commentary_en TEXT,
    modern_commentary_hi TEXT,
    confidence_level TEXT NOT NULL DEFAULT 'undeciphered',
    planet_tags TEXT[],
    house_tags INTEGER[],
    debt_tags TEXT[],
    remedy_category TEXT,
    rights_status TEXT NOT NULL DEFAULT 'commercial_unclear',
    source_library_id TEXT REFERENCES lk_source_library(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_farmaan_number ON lk_farmaan(farmaan_number);
CREATE INDEX IF NOT EXISTS idx_farmaan_planets ON lk_farmaan USING GIN(planet_tags);
CREATE INDEX IF NOT EXISTS idx_farmaan_houses ON lk_farmaan USING GIN(house_tags);
CREATE INDEX IF NOT EXISTS idx_farmaan_debts ON lk_farmaan USING GIN(debt_tags);
CREATE INDEX IF NOT EXISTS idx_farmaan_confidence ON lk_farmaan(confidence_level);

CREATE TABLE IF NOT EXISTS lk_farmaan_annotations (
    id TEXT PRIMARY KEY DEFAULT encode(gen_random_bytes(16), 'hex'),
    farmaan_id TEXT NOT NULL REFERENCES lk_farmaan(id) ON DELETE CASCADE,
    contributor_user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    annotation_type TEXT NOT NULL,
    language TEXT NOT NULL,
    body TEXT NOT NULL,
    upvotes INTEGER NOT NULL DEFAULT 0,
    is_accepted BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_farmaan_ann_farmaan ON lk_farmaan_annotations(farmaan_id);
CREATE INDEX IF NOT EXISTS idx_farmaan_ann_accepted ON lk_farmaan_annotations(is_accepted);
    """),
    (20, "P3.5 — Astrologer Dashboard: extend consultations table", """
-- P3.5 — Professional client management dashboard needs a richer
-- consultations shape: link to the astrologer's own `clients` record,
-- track duration, and carry an updated_at for activity-feed ordering.
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS client_id TEXT;
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS duration_minutes INTEGER DEFAULT 30;
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- Point `astrologer_id` at the users table directly (simpler routing — the
-- previous FK pointed at astrologers(id) which required a join to resolve
-- the logged-in user). We keep old rows working by dropping + re-adding
-- the FK to users(id) with ON DELETE SET NULL.
DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE table_name = 'consultations' AND constraint_name = 'consultations_astrologer_id_fkey'
  ) THEN
    EXECUTE 'ALTER TABLE consultations DROP CONSTRAINT consultations_astrologer_id_fkey';
  END IF;
END $$;
ALTER TABLE consultations ADD CONSTRAINT consultations_astrologer_id_fkey
  FOREIGN KEY (astrologer_id) REFERENCES users(id) ON DELETE SET NULL;

-- FK for the new client_id column.
DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE table_name = 'consultations' AND constraint_name = 'consultations_client_id_fkey'
  ) THEN
    EXECUTE 'ALTER TABLE consultations ADD CONSTRAINT consultations_client_id_fkey
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL';
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_consultations_astrologer ON consultations(astrologer_id);
CREATE INDEX IF NOT EXISTS idx_consultations_client ON consultations(client_id);
CREATE INDEX IF NOT EXISTS idx_consultations_scheduled ON consultations(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status);
    """),
    (21, "Sprint I — Client profile photo + palmistry hand photos", """
-- Client photo slots.
-- NOTE: astrologer/user profile photo already uses users.avatar_url
-- (added at table creation time) so no change is needed there.
-- Stored as base64 data URLs OR as relative paths under /uploads/ —
-- callers choose; the column is a free-form TEXT so the frontend can
-- pass whichever URL scheme it prefers.
ALTER TABLE clients ADD COLUMN IF NOT EXISTS profile_photo_url TEXT;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS left_hand_photo_url TEXT;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS right_hand_photo_url TEXT;
    """),
    (22, "Sprint I fixup — ensure consultations.client_id exists (prod)", """
-- Migration 20 attempted to add client_id + duration_minutes + updated_at
-- to consultations, but its DO $$ BEGIN...END $$ blocks contained inline
-- semicolons that the simple `sql.split(';')` runner splits on, leaving
-- the migration partially executed or silently skipped on production.
-- This migration re-applies the 3 column adds as plain idempotent ALTERs.

ALTER TABLE consultations ADD COLUMN IF NOT EXISTS client_id TEXT;
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS duration_minutes INTEGER DEFAULT 30;
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
CREATE INDEX IF NOT EXISTS idx_consultations_astrologer ON consultations(astrologer_id);
CREATE INDEX IF NOT EXISTS idx_consultations_client ON consultations(client_id);
CREATE INDEX IF NOT EXISTS idx_consultations_scheduled ON consultations(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status);
    """),
    (23, "Sprint I re-fixup — retry consultations columns (v22 had bad comment)", """
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS client_id TEXT;
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS duration_minutes INTEGER DEFAULT 30;
ALTER TABLE consultations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
CREATE INDEX IF NOT EXISTS idx_consultations_astrologer ON consultations(astrologer_id);
CREATE INDEX IF NOT EXISTS idx_consultations_client ON consultations(client_id);
CREATE INDEX IF NOT EXISTS idx_consultations_scheduled ON consultations(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status);
    """),
    (24, "Deduplicate kundlis per client+chart_type and enforce uniqueness", """
UPDATE kundlis SET chart_type = 'vedic' WHERE chart_type IS NULL OR chart_type = '';
DELETE FROM kundlis WHERE client_id IS NOT NULL AND id NOT IN (SELECT DISTINCT ON (client_id, chart_type) id FROM kundlis WHERE client_id IS NOT NULL ORDER BY client_id, chart_type, created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_kundlis_client_chart_unique ON kundlis (client_id, chart_type) WHERE client_id IS NOT NULL;
    """),
]


# ---- Migration 5 helper: re-create all FK constraints with ON DELETE CASCADE ----

# (child_table, fk_column(s), parent_table, parent_column(s))
_FK_CASCADE_SPEC = [
    ("kundlis", ["user_id"], "users", ["id"]),
    ("prashnavali_logs", ["user_id"], "users", ["id"]),
    ("ai_chat_logs", ["user_id"], "users", ["id"]),
    ("ai_chat_logs", ["kundli_id"], "kundlis", ["id"]),
    ("cart_items", ["user_id"], "users", ["id"]),
    ("cart_items", ["product_id"], "products", ["id"]),
    ("orders", ["user_id"], "users", ["id"]),
    ("order_items", ["order_id"], "orders", ["id"]),
    ("order_items", ["product_id"], "products", ["id"]),
    ("payments", ["order_id"], "orders", ["id"]),
    ("astrologers", ["user_id"], "users", ["id"]),
    ("consultations", ["user_id"], "users", ["id"]),
    ("consultations", ["astrologer_id"], "astrologers", ["id"]),
    ("messages", ["consultation_id"], "consultations", ["id"]),
    ("messages", ["sender_id"], "users", ["id"]),
    ("reports", ["user_id"], "users", ["id"]),
    ("reports", ["kundli_id"], "kundlis", ["id"]),
    ("bundle_items", ["bundle_id"], "product_bundles", ["id"]),
    ("bundle_items", ["product_id"], "products", ["id"]),
    ("referral_codes", ["user_id"], "users", ["id"]),
    ("referral_earnings", ["referrer_id"], "users", ["id"]),
    ("referral_earnings", ["referred_id"], "users", ["id"]),
    ("referral_earnings", ["order_id"], "orders", ["id"]),
    ("user_karma", ["user_id"], "users", ["id"]),
    ("karma_transactions", ["user_id"], "users", ["id"]),
    ("user_badges", ["user_id"], "users", ["id"]),
    ("learning_progress", ["user_id"], "users", ["id"]),
    ("learning_progress", ["module_id"], "learning_modules", ["id"]),
    ("user_notifications", ["user_id"], "users", ["id"]),
    ("notification_preferences", ["user_id"], "users", ["id"]),
    ("forum_threads", ["category_id"], "forum_categories", ["id"]),
    ("forum_threads", ["user_id"], "users", ["id"]),
    ("forum_replies", ["thread_id"], "forum_threads", ["id"]),
    ("forum_replies", ["user_id"], "users", ["id"]),
    ("forum_likes", ["user_id"], "users", ["id"]),
    ("forum_likes", ["reply_id"], "forum_replies", ["id"]),
    ("astrologer_clients", ["astrologer_user_id"], "users", ["id"]),
    ("astrologer_clients", ["kundli_id"], "kundlis", ["id"]),
]


def _apply_cascade_migration(conn):
    """Drop and recreate every FK constraint with ON DELETE CASCADE.

    Looks up the auto-generated constraint name from pg_constraint,
    drops it, and adds a new one with CASCADE.  Idempotent — skips
    any FK that already has CASCADE or whose constraint is missing
    (e.g. table not yet created).
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for child_table, fk_cols, parent_table, parent_cols in _FK_CASCADE_SPEC:
            # Find the constraint name for this FK
            cur.execute("""
                SELECT con.conname, con.confdeltype
                FROM pg_constraint con
                JOIN pg_class rel ON rel.oid = con.conrelid
                JOIN pg_namespace nsp ON nsp.oid = rel.relnamespace
                WHERE rel.relname = %s
                  AND nsp.nspname = 'public'
                  AND con.contype = 'f'
                  AND EXISTS (
                      SELECT 1
                      FROM unnest(con.conkey) WITH ORDINALITY AS ck(attnum, ord)
                      JOIN pg_attribute a ON a.attrelid = con.conrelid AND a.attnum = ck.attnum
                      WHERE a.attname = %s
                  )
            """, (child_table, fk_cols[0]))
            rows = cur.fetchall()
            if not rows:
                # Table or FK doesn't exist yet — skip
                continue
            for row in rows:
                if row["confdeltype"] == "c":
                    # Already CASCADE — nothing to do
                    continue
                constraint_name = row["conname"]
                fk_col_list = ", ".join(fk_cols)
                parent_col_list = ", ".join(parent_cols)
                new_constraint = f"fk_{child_table}_{'_'.join(fk_cols)}_cascade"
                try:
                    cur.execute(
                        f"ALTER TABLE {child_table} DROP CONSTRAINT {constraint_name}"
                    )
                    cur.execute(
                        f"ALTER TABLE {child_table} ADD CONSTRAINT {new_constraint} "
                        f"FOREIGN KEY ({fk_col_list}) REFERENCES {parent_table}({parent_col_list}) "
                        f"ON DELETE CASCADE"
                    )
                except Exception as e:
                    logger.warning("[migration] cascade for %s.%s: %s", child_table, fk_col_list, e)
                    conn.rollback()
    conn.commit()


_TIMESTAMPTZ_COLUMNS = [
    # (table, column, has_default)
    ("users", "created_at", True),
    ("users", "updated_at", True),
    ("kundlis", "created_at", True),
    ("horoscopes", "created_at", True),
    ("panchang_cache", "created_at", True),
    ("content_library", "created_at", True),
    ("blog_posts", "published_at", True),
    ("blog_posts", "created_at", True),
    ("blog_posts", "updated_at", True),
    ("prashnavali_logs", "created_at", True),
    ("ai_chat_logs", "created_at", True),
    ("products", "created_at", True),
    ("products", "updated_at", True),
    ("cart_items", "created_at", True),
    ("orders", "created_at", True),
    ("orders", "updated_at", True),
    ("payments", "created_at", True),
    ("astrologers", "created_at", True),
    ("consultations", "scheduled_at", False),
    ("consultations", "started_at", False),
    ("consultations", "ended_at", False),
    ("consultations", "created_at", True),
    ("messages", "created_at", True),
    ("reports", "created_at", True),
    ("muhurat_cache", "created_at", True),
    ("product_bundles", "created_at", True),
    ("audit_log", "created_at", True),
    ("referral_codes", "created_at", True),
    ("referral_codes", "updated_at", True),
    ("referral_earnings", "created_at", True),
    ("user_karma", "last_activity_date", False),
    ("user_karma", "created_at", True),
    ("karma_transactions", "created_at", True),
    ("user_badges", "earned_at", True),
    ("learning_progress", "completed_at", True),
    ("user_notifications", "created_at", True),
    ("forum_threads", "created_at", True),
    ("forum_threads", "updated_at", True),
    ("forum_replies", "created_at", True),
    ("forum_replies", "updated_at", True),
    ("forum_likes", "created_at", True),
    ("astrologer_clients", "created_at", True),
    ("astrologer_clients", "updated_at", True),
    ("email_verifications", "expires_at", False),
    ("email_verifications", "created_at", True),
    ("applied_migrations", "applied_at", True),
]


def _apply_timestamptz_migration(conn):
    """Convert TEXT date/time columns to TIMESTAMPTZ.

    Uses USING column::timestamptz to cast existing ISO-8601 text values.
    Skips columns that are already TIMESTAMPTZ (idempotent).
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for table, column, has_default in _TIMESTAMPTZ_COLUMNS:
            # Check if table and column exist and what the current type is
            cur.execute("""
                SELECT data_type FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                  AND column_name = %s
            """, (table, column))
            row = cur.fetchone()
            if not row:
                # Table or column doesn't exist yet — skip
                continue
            if row["data_type"] in (
                "timestamp with time zone",
                "timestamp without time zone",
            ):
                # Already a timestamp type — skip
                continue
            try:
                cur.execute(
                    f"ALTER TABLE {table} ALTER COLUMN {column} "
                    f"TYPE TIMESTAMPTZ USING {column}::timestamptz"
                )
                if has_default:
                    cur.execute(
                        f"ALTER TABLE {table} ALTER COLUMN {column} "
                        f"SET DEFAULT NOW()"
                    )
                logger.info("[migration] Converted %s.%s to TIMESTAMPTZ", table, column)
            except Exception as e:
                logger.warning("[migration] %s.%s: %s", table, column, e)
                conn.rollback()
    conn.commit()


def _apply_lk_fk_constraints(conn):
    """Add FK ON DELETE CASCADE constraints to LK tables if not already present."""
    specs = [
        ("lk_tracker_logs", "user_id", "fk_lk_tracker_logs_user_id"),
        ("lk_chandra_protocol", "user_id", "fk_lk_chandra_protocol_user_id"),
        ("lk_journal_entries", "user_id", "fk_lk_journal_entries_user_id"),
    ]
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        for table, col, constraint_name in specs:
            # Skip if table doesn't exist
            cur.execute("""
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = %s
            """, (table,))
            if not cur.fetchone():
                logger.info("[migration] Table %s not found — skip FK", table)
                continue
            # Skip if constraint already exists
            cur.execute("""
                SELECT 1 FROM information_schema.table_constraints
                WHERE constraint_name = %s AND table_name = %s
            """, (constraint_name, table))
            if cur.fetchone():
                logger.info("[migration] FK %s already exists — skip", constraint_name)
                continue
            try:
                cur.execute(
                    f"ALTER TABLE {table} ADD CONSTRAINT {constraint_name} "
                    f"FOREIGN KEY ({col}) REFERENCES users(id) ON DELETE CASCADE"
                )
                logger.info("[migration] Added FK %s", constraint_name)
            except Exception as e:
                logger.warning("[migration] %s: %s", constraint_name, e)
                conn.rollback()
    conn.commit()


def _ensure_migration_table(conn):
    """Create the applied_migrations table if it does not exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applied_migrations (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
    conn.commit()


def _safe_alter(conn, table: str, column: str, col_def: str):
    """Add a column only if it doesn't already exist."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s
            """,
            (table, column),
        )
        exists = cur.fetchone()
    if not exists:
        with conn.cursor() as cur:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
        conn.commit()


def run_migrations(db_path: str = None):
    """Check applied_migrations table and run any pending migrations in order.
    db_path parameter is kept for API compatibility but ignored (uses DATABASE_URL)."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False

    _ensure_migration_table(conn)

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT version FROM applied_migrations")
        applied = {row["version"] for row in cur.fetchall()}

    for version, description, sql in MIGRATIONS:
        if version in applied:
            continue

        # Special handling for specific migrations
        if version == 9:
            _apply_lk_fk_constraints(conn)
        elif version == 6:
            _apply_timestamptz_migration(conn)
        elif version == 5:
            _apply_cascade_migration(conn)
        elif version == 2:
            _safe_alter(conn, "users", "date_of_birth", "TEXT")
            _safe_alter(conn, "users", "gender", "TEXT")
            _safe_alter(conn, "users", "city", "TEXT")
            _safe_alter(conn, "users", "is_active", "INTEGER DEFAULT 1")
        elif version == 3:
            try:
                from app.blog_seed import seed_blog_posts
            except ImportError:
                seed_blog_posts = None  # blog_seed removed — skip blog seeding
            # Execute each statement in the SQL block
            stmts = [s.strip() for s in sql.split(';') if s.strip()]
            with conn.cursor() as cur:
                for stmt in stmts:
                    try:
                        cur.execute(stmt)
                    except Exception as e:
                        logger.warning("[migration] v%d statement: %s", version, e, exc_info=True)
                        conn.rollback()
            conn.commit()
            if seed_blog_posts is not None:
                from app.database import PgConnection
                import psycopg2 as pg2
                raw = pg2.connect(DATABASE_URL)
                pg = PgConnection(raw)
                seed_blog_posts(pg)
                raw.commit()
                raw.close()
        else:
            stmts = [s.strip() for s in sql.split(';') if s.strip()]
            with conn.cursor() as cur:
                for stmt in stmts:
                    try:
                        cur.execute(stmt)
                    except Exception as e:
                        logger.warning("[migration] v%d statement: %s", version, e, exc_info=True)
                        conn.rollback()
            conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO applied_migrations (version, description) VALUES (%s, %s)",
                (version, description),
            )
        conn.commit()
        logger.info("[migration] Applied v%d: %s", version, description)

    conn.close()
