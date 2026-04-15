"""Seed the database with initial spiritual content, festivals, and products."""
import json
import logging
import uuid
import psycopg2

logger = logging.getLogger(__name__)

from app.database import init_db, DATABASE_URL, PgConnection


def _uid() -> str:
    return uuid.uuid4().hex


def seed_all(db_path: str = None):
    """Seed all initial data. Skips if content_library already has rows."""

    # Ensure schema exists
    init_db()

    raw = psycopg2.connect(DATABASE_URL)
    raw.autocommit = False
    conn = PgConnection(raw)

    try:
        row = conn.execute("SELECT COUNT(*) as c FROM content_library").fetchone()
        count = row["c"]
        if count > 0:
            logger.info("[seed] content_library already has %d rows — skipping seed.", count)
            raw.close()
            return

        logger.info("[seed] Seeding database...")

        # ------------------------------------------------------------------
        # 1. Gita Chapters (18 entries, category='gita')
        # ------------------------------------------------------------------
        gita_chapters = [
            (1, "Arjuna Vishada Yoga", "The Yoga of Arjuna's Dejection", 47,
             "Arjuna, seeing his relatives and teachers arrayed against him on the battlefield of Kurukshetra, "
             "is overcome with grief and moral dilemma. He drops his bow and refuses to fight, expressing his "
             "anguish to Lord Krishna about the futility of war and the sin of killing kinsmen."),
            (2, "Sankhya Yoga", "The Yoga of Knowledge", 72,
             "Krishna begins his teaching by explaining the immortality of the soul (Atman), the impermanence "
             "of the body, and the duty (dharma) of a warrior. He introduces the paths of knowledge (Sankhya) "
             "and selfless action (Karma Yoga), urging Arjuna to act without attachment to results."),
            (3, "Karma Yoga", "The Yoga of Action", 43,
             "Krishna explains that no one can remain inactive even for a moment. He teaches that selfless action "
             "performed as duty, without attachment to fruits, is superior to inaction. He emphasizes performing "
             "one's prescribed duties for the welfare of the world (loka-sangraha)."),
            (4, "Jnana Karma Sanyasa Yoga", "Renunciation of Action through Knowledge", 42,
             "Krishna reveals that he has taught this eternal yoga to the sun god Vivasvan. He explains how divine "
             "knowledge destroys the bondage of karma, and that a wise person sees inaction in action and action "
             "in inaction. The fire of knowledge burns all karmic reactions."),
            (5, "Karma Sanyasa Yoga", "The Yoga of Renunciation", 29,
             "Krishna reconciles the paths of renunciation of action and selfless action, declaring both lead to "
             "liberation. He explains that true renunciation is mental detachment from results while continuing to "
             "act. A self-realized person finds happiness within and sees equality in all beings."),
            (6, "Dhyana Yoga", "The Yoga of Meditation", 47,
             "Krishna describes the practice of meditation (dhyana), including the proper posture, focus, and "
             "discipline required. He teaches that the mind must be controlled through practice and detachment. "
             "He assures Arjuna that no effort on the spiritual path is ever wasted."),
            (7, "Jnana Vijnana Yoga", "The Yoga of Knowledge and Wisdom", 30,
             "Krishna reveals his divine nature, explaining that he is the source of all material and spiritual "
             "worlds. He describes how his Maya deludes beings and how rare are those who seek and know him truly. "
             "He explains both his lower (material) and higher (spiritual) natures."),
            (8, "Aksara Brahma Yoga", "The Yoga of the Imperishable Absolute", 28,
             "Krishna explains the concepts of Brahman, Adhyatma, Karma, Adhibhuta, Adhidaiva, and Adhiyajna. "
             "He teaches that those who remember him at the time of death attain his supreme abode. He describes "
             "the paths of light and darkness by which yogis depart from this world."),
            (9, "Raja Vidya Raja Guhya Yoga", "The Yoga of Royal Knowledge", 34,
             "Krishna reveals the most confidential knowledge: that he pervades the entire universe yet remains "
             "transcendent. He explains how devotion (bhakti) is the supreme path, accessible to all regardless "
             "of birth or status. Even a leaf or water offered with devotion is accepted by him."),
            (10, "Vibhuti Yoga", "The Yoga of Divine Manifestation", 42,
             "Krishna describes his divine glories (vibhutis) — the finest manifestations in every category of "
             "existence. He is the beginning, middle, and end of all beings. Among mountains he is Meru, among "
             "rivers the Ganga, among weapons the thunderbolt, and among sciences he is the science of the Self."),
            (11, "Vishvarupa Darshana Yoga", "The Yoga of the Universal Form", 55,
             "At Arjuna's request, Krishna reveals his cosmic universal form (Vishvarupa), displaying infinite "
             "faces, arms, and divine weapons. Arjuna sees the entire universe, all beings, and the gods within "
             "Krishna's body. Overwhelmed with awe and fear, he begs Krishna to return to his gentle form."),
            (12, "Bhakti Yoga", "The Yoga of Devotion", 20,
             "Arjuna asks whether it is better to worship the personal or impersonal form of God. Krishna "
             "declares that those who fix their minds on him with faith and devotion are the most perfect yogis. "
             "He describes the qualities of a dear devotee: compassionate, humble, content, and equal in joy and sorrow."),
            (13, "Kshetra Kshetrajna Vibhaga Yoga", "The Yoga of Field and Knower", 35,
             "Krishna explains the body as the field (kshetra) and the soul as the knower of the field "
             "(kshetrajna). He describes the elements that constitute the field, true knowledge, and the "
             "supreme Brahman. Understanding the distinction between Prakriti and Purusha leads to liberation."),
            (14, "Gunatraya Vibhaga Yoga", "The Yoga of the Three Gunas", 27,
             "Krishna explains the three qualities (gunas) of material nature: Sattva (goodness), Rajas (passion), "
             "and Tamas (ignorance). He describes how these gunas bind the soul and how one can transcend them. "
             "One who transcends the gunas attains immortality."),
            (15, "Purushottama Yoga", "The Yoga of the Supreme Person", 20,
             "Krishna uses the metaphor of the eternal banyan tree (ashvattha) with roots above and branches below "
             "to describe the material world. He explains that he is Purushottama — the Supreme Person beyond both "
             "the perishable (material) and imperishable (individual soul)."),
            (16, "Daivasura Sampad Vibhaga Yoga", "Divine and Demonic Natures", 24,
             "Krishna describes twenty-six divine qualities (fearlessness, purity, charity, self-control) and six "
             "demonic qualities (hypocrisy, arrogance, pride, anger, harshness, ignorance). He explains that "
             "divine qualities lead to liberation while demonic qualities lead to bondage."),
            (17, "Shraddhatraya Vibhaga Yoga", "The Yoga of Three Kinds of Faith", 28,
             "Krishna explains that faith (shraddha) is of three types corresponding to the three gunas: sattvic, "
             "rajasic, and tamasic. This threefold division applies to food, sacrifice, austerity, and charity. "
             "He teaches the significance of Om Tat Sat as the threefold designation of Brahman."),
            (18, "Moksha Sanyasa Yoga", "The Yoga of Liberation through Renunciation", 78,
             "In this concluding chapter, Krishna summarizes all teachings. He explains renunciation, the three "
             "types of knowledge, action, and doer. He reveals his most confidential instruction: surrender unto "
             "him completely (sarva-dharman parityajya). Arjuna's delusion is destroyed and he is ready to fight."),
        ]

        for ch_num, name, subtitle, verse_count, summary in gita_chapters:
            conn.execute(
                "INSERT INTO content_library (id, category, title, title_hindi, content, chapter, translation, sort_order) "
                "VALUES (%s, 'gita', %s, NULL, %s, %s, %s, %s)",
                (_uid(), f"Chapter {ch_num}: {name} ({subtitle})", summary, ch_num, f"{verse_count} verses", ch_num),
            )

        # ------------------------------------------------------------------
        # 2. Key Gita Verses (10 famous slokas, category='gita')
        # ------------------------------------------------------------------
        gita_verses = [
            (2, 47,
             "karmanye vadhikaraste ma phaleshu kadachana\nma karma-phala-hetur bhur ma te sango 'stv akarmani",
             "You have the right to perform your duty, but you are not entitled to the fruits of your actions. "
             "Never consider yourself to be the cause of the results, and never be attached to inaction.",
             "This is the foundational verse of Karma Yoga. Krishna teaches Arjuna that one should focus on "
             "action alone, without attachment to outcomes. This detachment from results is the key to inner peace."),
            (2, 14,
             "matra-sparshas tu kaunteya shitoshna-sukha-duhkha-dah\nagamapayino 'nityas tams titikshasva bharata",
             "O son of Kunti, the contact of the senses with their objects gives rise to cold and heat, "
             "pleasure and pain. They are transient, arising and disappearing. Bear them patiently, O Bharata.",
             "Krishna teaches equanimity — the ability to remain balanced amidst pleasure and pain. Both are "
             "temporary and arise from sense contact with the material world."),
            (4, 7,
             "yada yada hi dharmasya glanir bhavati bharata\nabhyutthanam adharmasya tadatmanam srjamy aham",
             "Whenever there is a decline in righteousness and an increase in unrighteousness, O Arjuna, "
             "at that time I manifest myself on earth.",
             "Krishna declares the purpose of divine incarnation (avatara). Whenever dharma declines and "
             "adharma rises, the Lord appears to restore cosmic order."),
            (9, 22,
             "ananyash chintayanto mam ye janah paryupasate\ntesham nityabhiyuktanam yoga-kshemam vahamy aham",
             "To those who worship me with exclusive devotion, meditating on my transcendental form, "
             "I carry what they lack and preserve what they have.",
             "Krishna's promise to devotees: those who worship him with undivided devotion receive his "
             "personal care. He ensures their material and spiritual welfare."),
            (11, 32,
             "kalo 'smi loka-kshaya-krit pravrddho lokan samahartum iha pravrttah\nrte 'pi tvam na bhavishyanti sarve ye 'vasthitah pratyanikesu yodhah",
             "I am mighty Time, the destroyer of worlds, engaged in destroying all beings. Even without "
             "your participation, all the warriors arrayed in the opposing armies shall cease to exist.",
             "Krishna reveals his terrifying cosmic form as Time (Kala), the ultimate destroyer. "
             "This verse was famously quoted by J. Robert Oppenheimer after the first nuclear test."),
            (18, 66,
             "sarva-dharman parityajya mam ekam sharanam vraja\naham tvam sarva-papebhyo mokshayishyami ma shuchah",
             "Abandon all varieties of dharma and simply surrender unto me. "
             "I shall deliver you from all sinful reactions. Do not fear.",
             "The charama-shloka — Krishna's ultimate instruction. Complete surrender (sharanagati) to God "
             "is the highest teaching. This is considered the essence of the entire Gita."),
            (2, 20,
             "na jayate mriyate va kadachin nayam bhutva bhavita va na bhuyah\najo nityah shashvato 'yam purano na hanyate hanyamane sharire",
             "The soul is neither born, nor does it ever die; nor having once existed, does it ever cease to be. "
             "The soul is unborn, eternal, ever-existing, and primeval. It is not slain when the body is slain.",
             "Krishna's teaching on the immortality of the Atman. The soul transcends birth and death, "
             "existing beyond the temporary material body."),
            (6, 5,
             "uddhared atmanatmanam natmanam avasadayet\natmaiva hy atmano bandhur atmaiva ripur atmanah",
             "Let a person lift themselves by their own self; let them not degrade themselves. "
             "For the self alone is the friend of the self, and the self alone is the enemy of the self.",
             "A powerful teaching on self-reliance. One's own mind can be either the greatest friend or "
             "the worst enemy. Through discipline and effort, one must elevate oneself."),
            (3, 35,
             "shreyaan sva-dharmo vigunah para-dharmaat sv-anushthitaat\nsva-dharme nidhanam shreyah para-dharmo bhayavahah",
             "It is far better to discharge one's prescribed duties, even though imperfectly, "
             "than another's duties perfectly. Destruction in the course of one's own duty is better; "
             "the duty of another is full of danger.",
             "Krishna emphasizes following one's own nature and calling (sva-dharma) rather than "
             "imitating another's path. Authenticity in one's own duty, even imperfectly performed, is safer."),
            (15, 15,
             "sarvasya chaham hrdi sannivishto mattah smritir jnanam apohanam cha\nvedaish cha sarvair aham eva vedyo vedanta-krd veda-vid eva caham",
             "I am seated in the hearts of all living beings. From me come memory, knowledge, and forgetfulness. "
             "I alone am to be known by all the Vedas. I am the author of Vedanta and the knower of the Vedas.",
             "Krishna reveals his presence as the Supersoul (Paramatma) within every heart. He is the source "
             "of all knowledge and the ultimate subject of all Vedic literature."),
        ]

        for ch, verse, sanskrit, translation, commentary in gita_verses:
            conn.execute(
                "INSERT INTO content_library (id, category, title, content, chapter, verse, "
                "sanskrit_text, translation, commentary, sort_order) "
                "VALUES (%s, 'gita', %s, %s, %s, %s, %s, %s, %s, %s)",
                (_uid(), f"BG {ch}.{verse}", f"Bhagavad Gita Chapter {ch}, Verse {verse}",
                 ch, verse, sanskrit, translation, commentary, 100 + ch * 100 + verse),
            )

        # ------------------------------------------------------------------
        # 3. Mantras (8 entries, category='mantra')
        # ------------------------------------------------------------------
        mantras = [
            ("Gayatri Mantra",
             "Om Bhur Bhuvah Svah\nTat Savitur Varenyam\nBhargo Devasya Dhimahi\nDhiyo Yo Nah Prachodayat",
             "We meditate upon the divine light of the adorable Sun of spiritual consciousness. "
             "May it stimulate our power of spiritual perception.",
             "The Gayatri Mantra is considered the most sacred mantra in Hinduism, from the Rig Veda (3.62.10). "
             "It is a prayer to Savitri, the sun deity, for enlightenment and spiritual awakening."),
            ("Maha Mrityunjaya Mantra",
             "Om Tryambakam Yajamahe\nSugandhim Pushtivardhanam\nUrvarukamiva Bandhanan\nMrityor Mukshiya Maamritat",
             "We worship the three-eyed Lord Shiva who nourishes and spreads fragrance in our lives. "
             "May he liberate us from the bondage of death, as a ripe cucumber is severed from its vine.",
             "Also known as the Moksha Mantra, this powerful chant from the Rig Veda (7.59.12) is dedicated "
             "to Lord Shiva. It is recited for healing, protection from danger, and conquering the fear of death."),
            ("Om Namah Shivaya",
             "Om Namah Shivaya",
             "I bow to Lord Shiva, the auspicious one, the supreme consciousness.",
             "The Panchakshari (five-syllable) mantra is the most fundamental mantra dedicated to Lord Shiva. "
             "It appears in the Shri Rudram of the Yajur Veda and is considered a path to liberation."),
            ("Om Namo Bhagavate Vasudevaya",
             "Om Namo Bhagavate Vasudevaya",
             "I bow to Lord Vasudeva (Krishna), the Supreme Personality of Godhead.",
             "The Dvadasakshari (twelve-syllable) mantra is a liberation (mukti) mantra dedicated to Lord Vishnu/Krishna. "
             "It is prominently mentioned in the Bhagavata Purana."),
            ("Hanuman Mantra",
             "Om Hanumate Namah\n\nManojavam Maruta-tulya-vegam\nJitendriyam Buddhi-mataam Varishtham\n"
             "Vaataatmajam Vaanara-yootha-mukhyam\nShri Rama-dootam Sharanam Prapadye",
             "I surrender to Hanuman, the messenger of Lord Rama, who is swift as the mind and fast as the wind, "
             "master of the senses, foremost among the learned, son of the Wind God, and chief of the monkey army.",
             "Hanuman mantras invoke strength, courage, devotion, and protection. Lord Hanuman is the supreme "
             "devotee of Lord Rama and the embodiment of selfless service and unwavering faith."),
            ("Ganesh Mantra",
             "Om Gam Ganapataye Namah\n\nVakratunda Mahakaya\nSuryakoti Samaprabha\nNirvighnam Kuru Me Deva\nSarva-Kaaryeshu Sarvada",
             "O Lord Ganesha with the curved trunk and mighty body, whose radiance equals a billion suns, "
             "please make all my endeavors free of obstacles, always.",
             "Lord Ganesha is the remover of obstacles (Vighnaharta) and is worshipped at the beginning "
             "of all auspicious undertakings. His mantras bring wisdom, success, and new beginnings."),
            ("Lakshmi Mantra",
             "Om Shreem Mahalakshmiyei Namah\n\nSarva-mangala-maangalye Shive Sarvaartha-saadhike\n"
             "Sharanye Tryambake Gauri Naaraayani Namo-stute",
             "I bow to Goddess Mahalakshmi. O auspicious of all that is auspicious, O consort of Lord Shiva, "
             "O fulfiller of all objectives, O giver of refuge, O three-eyed Gauri, O Narayani, I bow to you.",
             "Goddess Lakshmi is the deity of wealth, fortune, prosperity, and beauty. Her mantras are chanted "
             "for abundance, material well-being, and spiritual richness."),
            ("Saraswati Mantra",
             "Om Aim Saraswatyai Namah\n\nSaraswati Namastubhyam\nVarade Kaama-roopini\nVidyaarambham Karishyaami\nSiddhir Bhavatu Me Sadaa",
             "I bow to Goddess Saraswati, the bestower of boons and fulfiller of desires. "
             "I am beginning my studies — may success be mine always.",
             "Goddess Saraswati presides over knowledge, music, arts, and learning. Her mantras are chanted "
             "by students, artists, and seekers of wisdom for intellectual clarity and creative inspiration."),
        ]

        for sort_idx, (title, content, translation, commentary) in enumerate(mantras, start=1):
            conn.execute(
                "INSERT INTO content_library (id, category, title, content, translation, commentary, sort_order) "
                "VALUES (%s, 'mantra', %s, %s, %s, %s, %s)",
                (_uid(), title, content, translation, commentary, sort_idx),
            )

        # ------------------------------------------------------------------
        # 4. Aarti (5 entries, category='aarti')
        # ------------------------------------------------------------------
        aartis = [
            ("Om Jai Jagdish Hare",
             "Om Jai Jagdish Hare, Swami Jai Jagdish Hare\n"
             "Bhakt Janon Ke Sankat, Daas Janon Ke Sankat\nKshan Mein Door Kare\nOm Jai Jagdish Hare",
             "O Lord of the Universe, Glory to you! You remove the troubles of your devotees in an instant.",
             "One of the most popular Hindu aartis, sung during evening prayers (sandhya aarti). "
             "Composed by Pandit Shardha Ram Phillauri in 1870, it is a universal prayer to the Supreme Lord."),
            ("Om Jai Shiv Omkara",
             "Om Jai Shiv Omkara, Swami Jai Shiv Omkara\n"
             "Brahma Vishnu Sadashiv, Ardhangi Dhara\nOm Jai Shiv Omkara",
             "Glory to Lord Shiva, the one represented by Om. Brahma, Vishnu, and Sadashiva reside in him, "
             "and his consort Parvati adorns half his body.",
             "The Shiv Aarti is sung during the worship of Lord Shiva. It describes his divine attributes, "
             "his cosmic role, and the blessings he bestows on his devotees."),
            ("Aarti Kunj Bihari Ki",
             "Aarti Kunj Bihari Ki, Shri Girdhar Krishna Murari Ki\n"
             "Gale Mein Baijanti Mala, Bajave Murali Madhur Bala\nShravan Mein Kunj Bihari Ki",
             "Aarti to Lord Krishna, the one who roams the gardens of Vrindavan, lifter of Govardhan hill. "
             "He wears the Vaijanti garland and plays the sweet flute.",
             "This beloved aarti is dedicated to Lord Krishna in his Vrindavan form. It paints a vivid "
             "picture of Krishna's divine beauty, his playful nature, and his enchanting flute."),
            ("Jai Ganesh Deva",
             "Jai Ganesh Jai Ganesh Jai Ganesh Deva\n"
             "Mata Jaki Parvati, Pita Mahadeva\nOm Jai Ganesh Deva",
             "Victory to Lord Ganesha! Whose mother is Parvati and whose father is Lord Shiva (Mahadeva).",
             "The Ganesh Aarti is traditionally sung at the beginning of any puja or auspicious occasion. "
             "Lord Ganesha, the elephant-headed god, is the remover of obstacles and the lord of beginnings."),
            ("Jai Ambe Gauri",
             "Jai Ambe Gauri, Maiya Jai Shyama Gauri\nTumko Nishdin Dhyavat, Hari Brahma Shivri\nJai Ambe Gauri",
             "Victory to Mother Ambika (Durga), the fair one. Lord Vishnu, Brahma, and Shiva meditate upon you day and night.",
             "This aarti is dedicated to Goddess Durga (Ambika/Gauri) and is prominently sung during Navratri. "
             "It celebrates the divine mother's power, grace, and her role as protector of the universe."),
        ]

        for sort_idx, (title, content, translation, commentary) in enumerate(aartis, start=1):
            conn.execute(
                "INSERT INTO content_library (id, category, title, content, translation, commentary, sort_order) "
                "VALUES (%s, 'aarti', %s, %s, %s, %s, %s)",
                (_uid(), title, content, translation, commentary, sort_idx),
            )

        # ------------------------------------------------------------------
        # 5. Chalisa (3 entries, category='chalisa')
        # ------------------------------------------------------------------
        chalisas = [
            ("Hanuman Chalisa",
             "Shri Guru Charan Saroj Raj, Nij Manu Mukuru Sudhari\n"
             "Barnau Raghubar Bimal Jasu, Jo Dayaku Phal Chari\n\n"
             "Budhiheen Tanu Jaanike, Sumirau Pavan Kumar\n"
             "Bal Budhi Vidya Dehu Mohi, Harahu Kalesh Vikaar\n\n"
             "Jai Hanuman Gyan Gun Sagar\nJai Kapis Tihun Lok Ujagar\n\n"
             "Ram Doot Atulit Bal Dhama\nAnjani Putra Pavan Sut Nama\n\n"
             "... [full 40 chaupais]",
             "With the dust of Guru's lotus feet, I clean the mirror of my mind. "
             "I narrate the pure glory of Rama, the bestower of the four fruits of life. "
             "Knowing my body to be devoid of intelligence, I remember Hanuman, son of the Wind God. "
             "Grant me strength, wisdom, and knowledge; remove my afflictions and blemishes.",
             "The Hanuman Chalisa is a 40-verse devotional hymn composed by Tulsidas in Awadhi. "
             "It is the most recited Hindu prayer globally, dedicated to Lord Hanuman. "
             "Reciting it is believed to invoke Hanuman's protection, courage, and blessings."),
            ("Shiv Chalisa",
             "Jai Ganesh Girija Suvan, Mangal Mul Sujan\n"
             "Kahat Ayodhya Das Tum, Deu Abhay Vardan\n\n"
             "Jai Girijapati Deen Dayala\nSada Karat Santan Pratipala\n\n"
             "Bhal Chandrama Sohat Nike\nKanan Kundal Nagaphani Ke\n\n"
             "Ang Gaur Shira Ganga Bahaye\nMundmala Tan Chhaar Lagaye\n\n"
             "... [full 40 chaupais]",
             "Victory to Ganesha, son of Girija (Parvati), the auspicious one. "
             "Victory to the lord of Parvati, compassionate to the humble. "
             "The crescent moon adorns his forehead beautifully, serpent-shaped earrings in his ears.",
             "The Shiv Chalisa is a 40-verse hymn dedicated to Lord Shiva, describing his divine attributes, "
             "his cosmic role as destroyer and regenerator, and his benevolence toward devotees."),
            ("Durga Chalisa",
             "Namo Namo Durge Sukh Karani\nNamo Namo Ambe Dukh Harani\n\n"
             "Nirankar Hai Jyoti Tumhari\nTihu Lok Pheli Ujiyari\n\n"
             "Shashi Lalaat Mukh Mahavishala\nNetra Laal Bhrikuti Vikarala\n\n"
             "Roop Matu Ko Adhik Suhave\nDaras Karat Jan Ati Sukh Pave\n\n"
             "... [full 40 chaupais]",
             "I bow to Durga, the bestower of happiness. I bow to Amba, the remover of sorrows. "
             "Your divine light is formless and illuminates all three worlds. "
             "The moon adorns your forehead, your face is vast and majestic.",
             "The Durga Chalisa is a 40-verse hymn praising Goddess Durga (Shakti). "
             "Recited especially during Navratri, it celebrates the divine mother's power to destroy evil "
             "and protect her devotees from all calamities."),
        ]

        for sort_idx, (title, content, translation, commentary) in enumerate(chalisas, start=1):
            conn.execute(
                "INSERT INTO content_library (id, category, title, content, translation, commentary, sort_order) "
                "VALUES (%s, 'chalisa', %s, %s, %s, %s, %s)",
                (_uid(), title, content, translation, commentary, sort_idx),
            )

        # ------------------------------------------------------------------
        # 6. Festivals (15 entries in festivals table, year=2026)
        # ------------------------------------------------------------------
        festivals = [
            ("Diwali", "दीवाली", "2026-10-20",
             "The Festival of Lights celebrates the victory of light over darkness, good over evil, "
             "and knowledge over ignorance. It marks Lord Rama's return to Ayodhya after 14 years of exile.",
             json.dumps(["Light diyas and candles", "Perform Lakshmi Puja", "Exchange sweets and gifts",
                         "Burst firecrackers", "Rangoli decoration", "Wear new clothes"]),
             "major"),
            ("Holi", "होली", "2026-03-03",
             "The Festival of Colors celebrates the arrival of spring, the end of winter, and the victory "
             "of good over evil. It commemorates the divine love of Radha and Krishna.",
             json.dumps(["Holika Dahan bonfire on eve", "Play with colors and water",
                         "Drink thandai and bhang", "Sing and dance", "Share gujiya and sweets"]),
             "major"),
            ("Navratri", "नवरात्रि", "2026-10-01",
             "Nine nights dedicated to the worship of Goddess Durga and her nine forms (Navadurga). "
             "Devotees observe fasting, perform garba and dandiya, and celebrate feminine divine energy.",
             json.dumps(["Nine days of fasting", "Worship Navadurga forms", "Garba and Dandiya Raas",
                         "Kanya Puja on Ashtami/Navami", "Recite Durga Saptashati"]),
             "major"),
            ("Dussehra", "दशहरा", "2026-10-10",
             "Also known as Vijayadashami, it celebrates Lord Rama's victory over the demon king Ravana. "
             "Effigies of Ravana, Kumbhakarna, and Meghanada are burned, symbolizing the triumph of good over evil.",
             json.dumps(["Ramlila performances", "Burning of Ravana effigy", "Worship of weapons (Shastra Puja)",
                         "Exchange of Apta leaves", "Victory processions"]),
             "major"),
            ("Janmashtami", "जन्माष्टमी", "2026-08-15",
             "Celebrates the birth of Lord Krishna, the eighth avatar of Lord Vishnu. "
             "Observed on the eighth day (Ashtami) of the dark fortnight in the month of Bhadrapada.",
             json.dumps(["Midnight celebration of Krishna's birth", "Fasting until midnight",
                         "Dahi Handi (breaking curd pot)", "Devotional songs and dances",
                         "Jhankis depicting Krishna's life"]),
             "major"),
            ("Ganesh Chaturthi", "गणेश चतुर्थी", "2026-09-07",
             "The grand festival celebrating the birth of Lord Ganesha, the elephant-headed god of wisdom "
             "and new beginnings. Clay idols of Ganesha are installed and worshipped for 1 to 11 days.",
             json.dumps(["Install Ganesh idol", "Daily puja with modak offerings", "Aarti and bhajan",
                         "Visarjan (immersion) procession", "Community pandal celebrations"]),
             "major"),
            ("Maha Shivaratri", "महा शिवरात्रि", "2026-02-15",
             "The Great Night of Shiva — devotees observe fasting and all-night vigil to honor Lord Shiva. "
             "It is believed that on this night, Shiva performs the cosmic dance of creation and destruction.",
             json.dumps(["All-night vigil (jagaran)", "Fasting", "Abhishekam of Shiva Lingam with milk, honey, water",
                         "Chanting Om Namah Shivaya", "Visiting Shiva temples"]),
             "major"),
            ("Ram Navami", "राम नवमी", "2026-04-05",
             "Celebrates the birth of Lord Rama, the seventh avatar of Lord Vishnu and the ideal man (Maryada Purushottam). "
             "Observed on the ninth day of Chaitra Shukla Paksha.",
             json.dumps(["Recite Ramayana", "Fast and perform puja", "Visit Ram temples",
                         "Charitable acts", "Rath Yatra processions"]),
             "major"),
            ("Hanuman Jayanti", "हनुमान जयंती", "2026-04-14",
             "Celebrates the birth of Lord Hanuman, the supreme devotee of Lord Rama and the embodiment of "
             "strength, devotion, and selfless service.",
             json.dumps(["Recite Hanuman Chalisa", "Visit Hanuman temples", "Offer sindoor and oil",
                         "Community feasts", "Strength-related activities and wrestling"]),
             "major"),
            ("Makar Sankranti", "मकर संक्रांति", "2026-01-14",
             "Marks the sun's transition into Makara rashi (Capricorn), signaling the end of winter solstice "
             "and beginning of longer days. Known by different names across India.",
             json.dumps(["Fly kites", "Take holy dip in rivers", "Prepare til-gur (sesame-jaggery) sweets",
                         "Bonfires (Lohri in Punjab)", "Pongal celebrations in Tamil Nadu"]),
             "major"),
            ("Guru Purnima", "गुरु पूर्णिमा", "2026-07-11",
             "A day to honor and express gratitude to spiritual and academic teachers (gurus). "
             "It is celebrated on the full moon day (Purnima) of the Hindu month Ashadha.",
             json.dumps(["Honor your guru with offerings", "Perform Vyasa Puja", "Seek blessings",
                         "Donate to educational causes", "Recite guru stotrams"]),
             "major"),
            ("Raksha Bandhan", "रक्षा बंधन", "2026-08-11",
             "The festival celebrating the sacred bond between brothers and sisters. Sisters tie a protective "
             "thread (rakhi) on their brother's wrist, and brothers vow to protect their sisters.",
             json.dumps(["Sister ties rakhi on brother's wrist", "Brother gives gift/money",
                         "Family feast with sweets", "Prayers for sibling well-being"]),
             "major"),
            ("Karva Chauth", "करवा चौथ", "2026-10-17",
             "A fasting festival observed by married Hindu women for the longevity and well-being of their husbands. "
             "The fast is broken after sighting the moon through a sieve.",
             json.dumps(["Full-day fast from sunrise to moonrise", "Apply mehndi (henna)",
                         "Dress in bridal attire", "Listen to Karva Chauth katha",
                         "Break fast after sighting moon through sieve"]),
             "fasting"),
            ("Chhath Puja", "छठ पूजा", "2026-11-08",
             "An ancient Vedic festival dedicated to the Sun God (Surya) and Chhathi Maiya. "
             "Devotees observe rigorous fasting and offer prayers standing in water at sunrise and sunset.",
             json.dumps(["36-hour waterless fast (nirjala)", "Offer arghya to setting and rising sun",
                         "Prepare thekua and other prasad", "Stand in water bodies for prayers",
                         "Community celebration at river ghats"]),
             "major"),
            ("Vasant Panchami", "वसंत पंचमी", "2026-02-01",
             "Celebrates the arrival of spring and is dedicated to Goddess Saraswati, the deity of knowledge, "
             "music, and arts. People wear yellow, symbolizing the vibrancy of spring.",
             json.dumps(["Worship Goddess Saraswati", "Wear yellow clothes", "Fly yellow kites",
                         "Place books and instruments near Saraswati idol", "Prepare yellow sweets"]),
             "major"),
        ]

        for name, name_hindi, date, description, rituals, category in festivals:
            conn.execute(
                "INSERT INTO festivals (id, name, name_hindi, date, description, rituals, category, year) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 2026)",
                (_uid(), name, name_hindi, date, description, rituals, category),
            )

        # ------------------------------------------------------------------
        # 7. Products (12 entries in products table)
        # ------------------------------------------------------------------
        products = [
            # Gemstones
            ("Ruby (Manikya)", "Natural certified Ruby gemstone for Sun (Surya). Enhances leadership, vitality, "
             "and fame. Recommended for weak Sun in horoscope. Set in gold ring for best results.",
             "gemstone", 15000, "Sun", json.dumps({"origin": "Burma", "weight": "3-5 carats",
              "certification": "GIA certified", "benefits": ["Leadership", "Vitality", "Fame", "Government favor"]})),
            ("Blue Sapphire (Neelam)", "Natural certified Blue Sapphire for Saturn (Shani). Brings discipline, "
             "wealth, and karmic rewards. Must be worn after proper consultation. Set in silver or panchdhatu.",
             "gemstone", 25000, "Saturn", json.dumps({"origin": "Sri Lanka", "weight": "3-7 carats",
              "certification": "GIA certified", "benefits": ["Wealth", "Discipline", "Karmic reward", "Protection from Shani Dasha"]})),
            ("Emerald (Panna)", "Natural certified Emerald for Mercury (Budh). Enhances intellect, communication, "
             "and business acumen. Ideal for writers, speakers, and businesspeople. Set in gold.",
             "gemstone", 18000, "Mercury", json.dumps({"origin": "Colombia", "weight": "3-5 carats",
              "certification": "GIA certified", "benefits": ["Intellect", "Communication", "Business success", "Creativity"]})),
            # Rudraksha
            ("1-Mukhi Rudraksha", "Rare one-faced Rudraksha bead representing Lord Shiva himself. The most powerful "
             "Rudraksha for spiritual awakening, meditation, and moksha. Ruled by the Sun.",
             "rudraksha", 5000, "Sun", json.dumps({"faces": 1, "ruling_deity": "Shiva",
              "benefits": ["Spiritual enlightenment", "Concentration", "Leadership", "Inner peace"]})),
            ("5-Mukhi Rudraksha", "The most common and versatile five-faced Rudraksha representing Lord Kalagni Rudra. "
             "Beneficial for health, peace of mind, and spiritual growth. Ruled by Jupiter.",
             "rudraksha", 500, "Jupiter", json.dumps({"faces": 5, "ruling_deity": "Kalagni Rudra",
              "benefits": ["Health", "Peace of mind", "Academic success", "Blood pressure regulation"]})),
            ("Gauri Shankar Rudraksha", "A naturally joined twin Rudraksha symbolizing the union of Shiva and Parvati. "
             "Ideal for harmonious relationships, marital bliss, and balancing masculine-feminine energy.",
             "rudraksha", 3000, "Moon", json.dumps({"faces": "Twin-joined", "ruling_deity": "Shiva-Parvati",
              "benefits": ["Marital harmony", "Relationship healing", "Emotional balance", "Fertility blessings"]})),
            # Bracelets
            ("7 Chakra Healing Bracelet", "Natural stone bracelet with seven gemstones aligned to the seven chakras: "
             "Red Jasper, Carnelian, Tiger Eye, Green Aventurine, Lapis Lazuli, Amethyst, and Clear Quartz.",
             "bracelet", 1200, None, json.dumps({"stones": ["Red Jasper", "Carnelian", "Tiger Eye",
              "Green Aventurine", "Lapis Lazuli", "Amethyst", "Clear Quartz"],
              "benefits": ["Chakra balancing", "Energy alignment", "Stress relief", "Holistic healing"]})),
            ("Tiger Eye Bracelet", "Natural Tiger Eye stone bracelet for courage, confidence, and protection. "
             "Associated with the solar plexus chakra. Brings clarity of intention and willpower.",
             "bracelet", 800, "Sun", json.dumps({"stone": "Tiger Eye",
              "benefits": ["Courage", "Confidence", "Protection from evil eye", "Willpower", "Focus"]})),
            ("Black Tourmaline Bracelet", "Natural Black Tourmaline bracelet for powerful protection against "
             "negative energies, psychic attacks, and electromagnetic radiation. Grounding and purifying.",
             "bracelet", 1000, "Saturn", json.dumps({"stone": "Black Tourmaline",
              "benefits": ["Protection", "Grounding", "EMF shielding", "Negativity removal", "Stress relief"]})),
            # Yantras
            ("Sri Yantra", "Sacred geometric diagram representing the cosmos and the union of Shiva-Shakti. "
             "Energized Sri Yantra on copper plate for wealth, prosperity, and spiritual advancement.",
             "yantra", 2500, None, json.dumps({"material": "Copper", "size": "6x6 inches",
              "benefits": ["Wealth attraction", "Prosperity", "Spiritual growth", "Vastu correction",
                           "Business success"]})),
            ("Navgraha Yantra", "Yantra representing all nine planets (Navagrahas) for overall planetary harmony. "
             "Energized on copper plate. Mitigates malefic effects of all planets simultaneously.",
             "yantra", 3500, None, json.dumps({"material": "Copper", "size": "8x8 inches",
              "planets": ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
              "benefits": ["Planetary harmony", "Dosha removal", "Overall protection", "Success in endeavors"]})),
            # Vastu
            ("Vastu Pyramid Set", "Set of 9 copper pyramids for Vastu correction. Place in the center of your "
             "home or office to harmonize energy flow. Includes placement guide and activation mantra.",
             "vastu", 1500, None, json.dumps({"material": "Copper", "quantity": 9,
              "includes": ["9 pyramids", "Placement guide", "Activation mantra card"],
              "benefits": ["Vastu dosha correction", "Energy harmonization", "Positive vibrations",
                           "Peace and prosperity"]})),
        ]

        for name, description, category, price, planet, properties in products:
            conn.execute(
                "INSERT INTO products (id, name, description, category, price, planet, properties, stock, is_active) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, 50, 1)",
                (_uid(), name, description, category, price, planet, properties),
            )

        conn.commit()

        # Print summary counts
        content_count = conn.execute("SELECT COUNT(*) as c FROM content_library").fetchone()["c"]
        festival_count = conn.execute("SELECT COUNT(*) as c FROM festivals").fetchone()["c"]
        product_count = conn.execute("SELECT COUNT(*) as c FROM products").fetchone()["c"]

        logger.info("[seed] Done! content_library=%d, festivals=%d, products=%d", content_count, festival_count, product_count)

    except Exception as e:
        raw.rollback()
        logger.error("[seed] ERROR: %s", e)
        raise
    finally:
        raw.close()


if __name__ == "__main__":
    seed_all()
