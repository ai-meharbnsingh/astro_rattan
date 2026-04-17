/**
 * ═══════════════════════════════════════════════════════════════════
 * LALKITAB-DATA.TS — FRONTEND FALLBACK LAYER
 * ═══════════════════════════════════════════════════════════════════
 *
 * ARCHITECTURE NOTE (per Gemini audit):
 *
 * This file provides CLIENT-SIDE chart generation and analysis
 * as a FALLBACK when backend endpoints are unavailable. The
 * AUTHORITATIVE source of truth for all Lal Kitab calculations is:
 *
 *   Backend:  app/lalkitab_engine.py      (remedies, strength)
 *             app/lalkitab_advanced.py     (teva, masnui, bunyaad)
 *             app/lalkitab_technical.py    (chalti gaadi, dhur dhur aage)
 *             app/routes/kp_lalkitab.py    (47 endpoints serving computed results)
 *
 * Frontend tabs should PREFER backend data (via /api/lalkitab/full/{id}
 * or individual endpoints) over local computations. Local functions here
 * exist for:
 *   1. Immediate UI rendering before API response arrives
 *   2. Offline/error fallback when backend is unreachable
 *   3. Dosha detection (local-only, not yet in backend)
 *
 * DO NOT add new calculation logic here. Add it to the backend instead
 * and consume via API.
 * ═══════════════════════════════════════════════════════════════════
 */

// Lal Kitab data types and constants

export interface LalKitabHouse {
  house: number;
  planets: string[];
  strength: 'strong' | 'weak' | 'empty';
}

export interface LalKitabChartData {
  houses: LalKitabHouse[];
  planetPositions: Record<string, number>;
  planetLongitudes: Record<string, number>;
  doshas: DoshaResult[];
  activePlanet: { planet: string; ageStart: number; ageEnd: number } | null;
  isIncomplete: boolean;
  missingPlanets: string[];
}

export const PLANETS = [
  { key: 'Sun', en: 'Sun', hi: 'सूर्य' },
  { key: 'Moon', en: 'Moon', hi: 'चंद्र' },
  { key: 'Mars', en: 'Mars', hi: 'मंगल' },
  { key: 'Mercury', en: 'Mercury', hi: 'बुध' },
  { key: 'Jupiter', en: 'Jupiter', hi: 'गुरु' },
  { key: 'Venus', en: 'Venus', hi: 'शुक्र' },
  { key: 'Saturn', en: 'Saturn', hi: 'शनि' },
  { key: 'Rahu', en: 'Rahu', hi: 'राहु' },
  { key: 'Ketu', en: 'Ketu', hi: 'केतु' },
] as const;

// Pakka Ghar — the permanent house of each planet in Lal Kitab
export const PAKKA_GHAR: Record<string, number> = {
  Sun: 1,
  Moon: 4,
  Mars: 3,
  Mercury: 7,
  Jupiter: 2,
  Venus: 7,
  Saturn: 8,
  Rahu: 12,
  Ketu: 6,
};

// Age-wise planet activation periods (Lal Kitab Varshphal)
export const AGE_PLANET_ACTIVATION: Array<{ planet: string; ageStart: number; ageEnd: number }> = [
  { planet: 'Sun', ageStart: 1, ageEnd: 6 },
  { planet: 'Moon', ageStart: 7, ageEnd: 12 },
  { planet: 'Mars', ageStart: 13, ageEnd: 18 },
  { planet: 'Mercury', ageStart: 19, ageEnd: 24 },
  { planet: 'Jupiter', ageStart: 25, ageEnd: 36 },
  { planet: 'Venus', ageStart: 37, ageEnd: 48 },
  { planet: 'Saturn', ageStart: 49, ageEnd: 60 },
  { planet: 'Rahu', ageStart: 61, ageEnd: 72 },
  { planet: 'Ketu', ageStart: 73, ageEnd: 84 },
];

// Planet effects when placed in specific houses
export const PLANET_EFFECTS_IN_HOUSES: Record<string, Record<number, { en: string; hi: string }>> = {
  Sun: {
    1: { en: 'Strong leadership and vitality. Government favour likely.', hi: 'मजबूत नेतृत्व और जीवनशक्ति। सरकारी लाभ की संभावना।' },
    2: { en: 'Wealth through authority. Family pride increases.', hi: 'अधिकार से धन लाभ। परिवार का गौरव बढ़ता है।' },
    3: { en: 'Courage and valor in actions. Siblings benefit.', hi: 'कार्यों में साहस और शौर्य। भाई-बहनों को लाभ।' },
    4: { en: 'Domestic unrest possible. Mother health needs care.', hi: 'घरेलू अशांति संभव। माता के स्वास्थ्य पर ध्यान दें।' },
    5: { en: 'Brilliant children. Good fortune through education.', hi: 'प्रतिभाशाली संतान। शिक्षा से शुभ भाग्य।' },
    6: { en: 'Victory over enemies. Health remains strong.', hi: 'शत्रुओं पर विजय। स्वास्थ्य मजबूत रहता है।' },
    7: { en: 'Spouse brings honour. Partnerships flourish.', hi: 'जीवनसाथी से सम्मान। साझेदारी फलती है।' },
    8: { en: 'Hidden obstacles. Avoid risky ventures.', hi: 'छिपी बाधाएं। जोखिम भरे कार्यों से बचें।' },
    9: { en: 'Father figure influential. Spiritual growth.', hi: 'पितृ तुल्य प्रभावशाली। आध्यात्मिक उन्नति।' },
    10: { en: 'Career reaches peak. High status in society.', hi: 'करियर शिखर पर। समाज में उच्च स्थान।' },
    11: { en: 'Gains from authority. Wishes fulfilled.', hi: 'अधिकार से लाभ। मनोकामना पूर्ति।' },
    12: { en: 'Expenditure on travel. Spiritual journeys.', hi: 'यात्रा पर खर्च। आध्यात्मिक यात्राएं।' },
  },
  Moon: {
    1: { en: 'Emotional strength. Public popularity.', hi: 'भावनात्मक शक्ति। जनप्रियता।' },
    2: { en: 'Family wealth grows. Good food and comfort.', hi: 'पारिवारिक धन बढ़ता है। अच्छा भोजन और आराम।' },
    3: { en: 'Creative communication. Artistic talents.', hi: 'रचनात्मक संवाद। कलात्मक प्रतिभा।' },
    4: { en: 'Excellent domestic happiness. Property gains.', hi: 'उत्तम गृह सुख। संपत्ति लाभ।' },
    5: { en: 'Intelligent children. Romantic inclinations.', hi: 'बुद्धिमान संतान। रोमांटिक प्रवृत्ति।' },
    6: { en: 'Mood fluctuations. Digestive care needed.', hi: 'मनोदशा में उतार-चढ़ाव। पाचन का ध्यान रखें।' },
    7: { en: 'Attractive spouse. Harmonious marriage.', hi: 'आकर्षक जीवनसाथी। सामंजस्यपूर्ण विवाह।' },
    8: { en: 'Emotional turbulence. Inheritance possible.', hi: 'भावनात्मक उथल-पुथल। विरासत संभव।' },
    9: { en: 'Pilgrimage brings peace. Mother is fortunate.', hi: 'तीर्थयात्रा से शांति। माता भाग्यशाली।' },
    10: { en: 'Public sector career success. Fame.', hi: 'सार्वजनिक क्षेत्र में सफलता। यश।' },
    11: { en: 'Gains through women. Social network grows.', hi: 'महिलाओं से लाभ। सामाजिक नेटवर्क बढ़ता है।' },
    12: { en: 'Restless sleep. Expenses on comfort.', hi: 'अशांत नींद। आराम पर खर्च।' },
  },
  Mars: {
    1: { en: 'Bold personality. Physical strength.', hi: 'निडर व्यक्तित्व। शारीरिक शक्ति।' },
    2: { en: 'Harsh speech may cause issues. Property gains.', hi: 'कठोर वाणी से समस्या। संपत्ति लाभ।' },
    3: { en: 'Extremely courageous. Sibling rivalry possible.', hi: 'अत्यंत साहसी। भाई-बहनों से प्रतिस्पर्धा।' },
    4: { en: 'Land and vehicle acquisitions. Mother needs care.', hi: 'भूमि और वाहन प्राप्ति। माता का ध्यान रखें।' },
    5: { en: 'Children may be headstrong. Sports talent.', hi: 'संतान जिद्दी हो सकती है। खेल प्रतिभा।' },
    6: { en: 'Destroyer of enemies. Legal victories.', hi: 'शत्रुनाशक। कानूनी विजय।' },
    7: { en: 'Manglik effects on marriage. Passionate partner.', hi: 'विवाह पर मांगलिक प्रभाव। जोशीला साथी।' },
    8: { en: 'Accident prone period. Avoid confrontation.', hi: 'दुर्घटना संभव। टकराव से बचें।' },
    9: { en: 'Father relationship complex. Dharmic warrior.', hi: 'पिता से जटिल संबंध। धार्मिक योद्धा।' },
    10: { en: 'Police, military, surgery career success.', hi: 'पुलिस, सेना, सर्जरी में सफलता।' },
    11: { en: 'High income. Gains from property.', hi: 'उच्च आय। संपत्ति से लाभ।' },
    12: { en: 'Hidden anger. Expenditure on litigation.', hi: 'छिपा क्रोध। मुकदमेबाजी पर खर्च।' },
  },
  Mercury: {
    1: { en: 'Quick-witted and youthful. Business acumen.', hi: 'तेज बुद्धि और युवा। व्यापार कौशल।' },
    2: { en: 'Excellent speech. Wealth through intellect.', hi: 'उत्तम वाणी। बुद्धि से धन।' },
    3: { en: 'Writing and communication skills. Media success.', hi: 'लेखन और संवाद कौशल। मीडिया में सफलता।' },
    4: { en: 'Educational property. Learned household.', hi: 'शैक्षिक संपत्ति। विद्वान परिवार।' },
    5: { en: 'Brilliant academic children. Speculative gains.', hi: 'प्रतिभाशाली शैक्षिक संतान। सट्टा लाभ।' },
    6: { en: 'Analytical mind defeats enemies. Skin care needed.', hi: 'विश्लेषणात्मक बुद्धि से शत्रु पराजय। त्वचा का ध्यान रखें।' },
    7: { en: 'Intelligent spouse. Trade partnerships.', hi: 'बुद्धिमान जीवनसाथी। व्यापार साझेदारी।' },
    8: { en: 'Research abilities. Nervous disorders possible.', hi: 'शोध क्षमता। तंत्रिका विकार संभव।' },
    9: { en: 'Scholar of scriptures. Long travels for knowledge.', hi: 'शास्त्रों के विद्वान। ज्ञान के लिए लंबी यात्रा।' },
    10: { en: 'Accounting, IT, trade career success.', hi: 'लेखा, आईटी, व्यापार में सफलता।' },
    11: { en: 'Multiple income sources. Friend circle grows.', hi: 'आय के अनेक स्रोत। मित्र मंडली बढ़ती है।' },
    12: { en: 'Overthinking causes loss. Expenditure on education.', hi: 'अति-चिंतन से हानि। शिक्षा पर खर्च।' },
  },
  Jupiter: {
    1: { en: 'Blessed personality. Wisdom and fortune.', hi: 'आशीर्वादित व्यक्तित्व। बुद्धि और भाग्य।' },
    2: { en: 'Great family wealth. Sweet and wise speech.', hi: 'महान पारिवारिक धन। मधुर और बुद्धिमान वाणी।' },
    3: { en: 'Spiritual courage. Guru-like influence on siblings.', hi: 'आध्यात्मिक साहस। भाई-बहनों पर गुरु जैसा प्रभाव।' },
    4: { en: 'Large home. Vehicles and comforts aplenty.', hi: 'बड़ा घर। वाहन और सुविधाएं भरपूर।' },
    5: { en: 'Exceptional children. Education brings fame.', hi: 'असाधारण संतान। शिक्षा से यश।' },
    6: { en: 'Protection from enemies. Health recovers fast.', hi: 'शत्रुओं से सुरक्षा। स्वास्थ्य जल्दी ठीक होता है।' },
    7: { en: 'Noble and wise spouse. Prosperous partnership.', hi: 'कुलीन और बुद्धिमान जीवनसाथी। समृद्ध साझेदारी।' },
    8: { en: 'Long life. Spiritual transformation.', hi: 'दीर्घ आयु। आध्यात्मिक परिवर्तन।' },
    9: { en: 'Extremely fortunate. Pilgrimage and higher learning.', hi: 'अत्यंत भाग्यशाली। तीर्थयात्रा और उच्च शिक्षा।' },
    10: { en: 'Prestigious career. Judge, professor, priest.', hi: 'प्रतिष्ठित करियर। न्यायाधीश, प्रोफेसर, पुजारी।' },
    11: { en: 'Massive gains. Influential friends.', hi: 'भारी लाभ। प्रभावशाली मित्र।' },
    12: { en: 'Charitable nature. Expenses on donations.', hi: 'दानशील स्वभाव। दान पर खर्च।' },
  },
  Venus: {
    1: { en: 'Attractive personality. Artistic talents bloom.', hi: 'आकर्षक व्यक्तित्व। कलात्मक प्रतिभा खिलती है।' },
    2: { en: 'Luxury and wealth. Beautiful speech.', hi: 'विलासिता और धन। सुंदर वाणी।' },
    3: { en: 'Creative communication. Artistic siblings.', hi: 'रचनात्मक संवाद। कलात्मक भाई-बहन।' },
    4: { en: 'Luxurious home. Beautiful vehicles.', hi: 'शानदार घर। सुंदर वाहन।' },
    5: { en: 'Romantic nature. Beautiful children.', hi: 'रोमांटिक स्वभाव। सुंदर संतान।' },
    6: { en: 'Enemies through romance. Health of spouse.', hi: 'रोमांस से शत्रुता। जीवनसाथी का स्वास्थ्य।' },
    7: { en: 'Beautiful and loving spouse. Happy marriage.', hi: 'सुंदर और प्यारा जीवनसाथी। सुखी विवाह।' },
    8: { en: 'Hidden pleasures. Inheritance from in-laws.', hi: 'छिपे सुख। ससुराल से विरासत।' },
    9: { en: 'Fortune through arts. Luxurious pilgrimages.', hi: 'कला से भाग्य। शानदार तीर्थयात्रा।' },
    10: { en: 'Entertainment industry success. Glamorous career.', hi: 'मनोरंजन उद्योग में सफलता। आकर्षक करियर।' },
    11: { en: 'Gains through women and arts. Social charm.', hi: 'महिलाओं और कला से लाभ। सामाजिक आकर्षण।' },
    12: { en: 'Bedroom pleasures. Foreign luxury.', hi: 'शयनकक्ष सुख। विदेशी विलासिता।' },
  },
  Saturn: {
    1: { en: 'Disciplined but hard life. Late success.', hi: 'अनुशासित लेकिन कठिन जीवन। देर से सफलता।' },
    2: { en: 'Slow wealth accumulation. Frugal habits.', hi: 'धीमा धन संचय। मितव्ययी आदतें।' },
    3: { en: 'Persistent efforts. Younger siblings face hardship.', hi: 'लगातार प्रयास। छोटे भाई-बहनों को कठिनाई।' },
    4: { en: 'Old property gains. Mother health concerns.', hi: 'पुरानी संपत्ति लाभ। माता के स्वास्थ्य की चिंता।' },
    5: { en: 'Delayed children. Disciplined education.', hi: 'विलंबित संतान। अनुशासित शिक्षा।' },
    6: { en: 'Chronic health issues. But enemies are defeated.', hi: 'दीर्घकालिक स्वास्थ्य समस्याएं। लेकिन शत्रु पराजित।' },
    7: { en: 'Older or mature spouse. Serious marriage.', hi: 'बड़ा या परिपक्व जीवनसाथी। गंभीर विवाह।' },
    8: { en: 'Long life but chronic ailments. Transformation through hardship.', hi: 'दीर्घ आयु लेकिन पुरानी बीमारियां। कठिनाई से परिवर्तन।' },
    9: { en: 'Delayed fortune. Hard-earned spiritual growth.', hi: 'विलंबित भाग्य। कठिन अर्जित आध्यात्मिक विकास।' },
    10: { en: 'Steady career. Success in mining, iron, oil.', hi: 'स्थिर करियर। खनन, लोहा, तेल में सफलता।' },
    11: { en: 'Steady gains after 36. Old friends helpful.', hi: '36 के बाद स्थिर लाभ। पुराने मित्र सहायक।' },
    12: { en: 'Isolation. Foreign settlement possible.', hi: 'एकांत। विदेश बसने की संभावना।' },
  },
  Rahu: {
    1: { en: 'Unusual personality. Worldly success through unconventional means.', hi: 'असामान्य व्यक्तित्व। अपरंपरागत तरीकों से सांसारिक सफलता।' },
    2: { en: 'Foreign wealth. Deceptive speech patterns.', hi: 'विदेशी धन। भ्रामक वाणी पैटर्न।' },
    3: { en: 'Technological communication. Unusual courage.', hi: 'तकनीकी संवाद। असामान्य साहस।' },
    4: { en: 'Foreign property. Mother from different culture.', hi: 'विदेशी संपत्ति। भिन्न संस्कृति की माता।' },
    5: { en: 'Unusual children. Speculative risks.', hi: 'असामान्य संतान। सट्टा जोखिम।' },
    6: { en: 'Victory over hidden enemies. Technology in health.', hi: 'छिपे शत्रुओं पर विजय। स्वास्थ्य में तकनीक।' },
    7: { en: 'Foreign spouse. Unconventional marriage.', hi: 'विदेशी जीवनसाथी। अपरंपरागत विवाह।' },
    8: { en: 'Sudden transformations. Occult interests.', hi: 'अचानक परिवर्तन। तांत्रिक रुचि।' },
    9: { en: 'Foreign travels for fortune. Unorthodox beliefs.', hi: 'भाग्य के लिए विदेश यात्रा। अपरंपरागत विश्वास।' },
    10: { en: 'Sudden career rise. Technology sector success.', hi: 'अचानक करियर उन्नति। तकनीक क्षेत्र में सफलता।' },
    11: { en: 'Massive unexpected gains. Influential foreign friends.', hi: 'भारी अप्रत्याशित लाभ। प्रभावशाली विदेशी मित्र।' },
    12: { en: 'Foreign settlement. Spiritual awakening through loss.', hi: 'विदेश बसना। हानि से आध्यात्मिक जागृति।' },
  },
  Ketu: {
    1: { en: 'Spiritual personality. Detached nature.', hi: 'आध्यात्मिक व्यक्तित्व। विरक्त स्वभाव।' },
    2: { en: 'Speech issues. Mystical knowledge of wealth.', hi: 'वाणी समस्या। धन का रहस्यमय ज्ञान।' },
    3: { en: 'Spiritual courage. Communication through silence.', hi: 'आध्यात्मिक साहस। मौन के माध्यम से संवाद।' },
    4: { en: 'Detachment from home. Spiritual mother.', hi: 'घर से वैराग्य। आध्यात्मिक माता।' },
    5: { en: 'Past-life children karma. Intuitive education.', hi: 'पूर्वजन्म संतान कर्म। सहज शिक्षा।' },
    6: { en: 'Mysterious illnesses. Spiritual healing.', hi: 'रहस्यमय बीमारियां। आध्यात्मिक उपचार।' },
    7: { en: 'Past-life spouse connection. Unusual marriage.', hi: 'पूर्वजन्म जीवनसाथी संबंध। असामान्य विवाह।' },
    8: { en: 'Deep occult knowledge. Sudden spiritual awakening.', hi: 'गहरा तांत्रिक ज्ञान। अचानक आध्यात्मिक जागृति।' },
    9: { en: 'Moksha path. Guru appears in mysterious ways.', hi: 'मोक्ष मार्ग। गुरु रहस्यमय तरीकों से प्रकट।' },
    10: { en: 'Unconventional career. Spiritual vocation.', hi: 'अपरंपरागत करियर। आध्यात्मिक व्यवसाय।' },
    11: { en: 'Gains through spirituality. Unusual friendships.', hi: 'आध्यात्मिकता से लाभ। असामान्य मित्रता।' },
    12: { en: 'Final liberation. Complete spiritual transformation.', hi: 'अंतिम मुक्ति। पूर्ण आध्यात्मिक परिवर्तन।' },
  },
};

// Planetary friendships (Lal Kitab system)
export const PLANET_FRIENDS: Record<string, string[]> = {
  Sun: ['Moon', 'Mars', 'Jupiter'],
  Moon: ['Sun', 'Mercury'],
  Mars: ['Sun', 'Moon', 'Jupiter'],
  Mercury: ['Sun', 'Venus', 'Rahu'],
  Jupiter: ['Sun', 'Moon', 'Mars'],
  Venus: ['Mercury', 'Saturn', 'Rahu'],
  Saturn: ['Mercury', 'Venus', 'Rahu'],
  Rahu: ['Mercury', 'Venus', 'Saturn', 'Ketu'],
  Ketu: ['Mars', 'Venus', 'Rahu'],
};

// Planetary enmities (Lal Kitab system)
export const PLANET_ENEMIES: Record<string, string[]> = {
  Sun: ['Saturn', 'Venus', 'Rahu', 'Ketu'],
  Moon: ['Rahu', 'Ketu'],
  Mars: ['Mercury', 'Rahu', 'Ketu'],
  Mercury: ['Moon', 'Ketu'],
  Jupiter: ['Mercury', 'Venus', 'Rahu'],
  Venus: ['Sun', 'Moon'],
  Saturn: ['Sun', 'Moon', 'Mars'],
  Rahu: ['Sun', 'Moon', 'Mars'],
  Ketu: ['Sun', 'Moon'],
};

/**
 * Determines whether a planet is "active" or "sleeping" in Lal Kitab.
 * A planet is active if it is in its Pakka Ghar, or supported by a friendly planet in the same house.
 * A planet is sleeping if an enemy planet occupies the same house or it is weakly placed.
 */
export function getPlanetStatus(
  planetKey: string,
  chartData: LalKitabChartData
): 'active' | 'sleeping' {
  const house = chartData.planetPositions[planetKey];
  if (!house) return 'sleeping';

  // Planet in its Pakka Ghar is always active
  if (house === PAKKA_GHAR[planetKey]) {
    return 'active';
  }

  // Check if any enemy planet shares the same house — sleeping
  const enemies = PLANET_ENEMIES[planetKey] || [];
  for (const enemy of enemies) {
    if (chartData.planetPositions[enemy] === house) {
      return 'sleeping';
    }
  }

  // Check if any friendly planet shares the same house — active
  const friends = PLANET_FRIENDS[planetKey] || [];
  for (const friend of friends) {
    if (chartData.planetPositions[friend] === house) {
      return 'active';
    }
  }

  return 'active';
}

// Mirror house axes — each pair mirrors the other in Lal Kitab
export const MIRROR_HOUSES: Array<[number, number]> = [
  [1, 7],
  [2, 8],
  [3, 9],
  [4, 10],
  [5, 11],
  [6, 12],
];

// House meanings for all 12 houses
export const HOUSE_MEANINGS: Array<{ en: string; hi: string; lifeAreas: { en: string; hi: string }[] }> = [
  { en: 'Self, personality, physical body, temperament', hi: 'आत्मा, व्यक्तित्व, शारीरिक शरीर, स्वभाव', lifeAreas: [{ en: 'Health', hi: 'स्वास्थ्य' }, { en: 'Identity', hi: 'पहचान' }] },
  { en: 'Wealth, family, speech, food habits', hi: 'धन, परिवार, वाणी, खान-पान', lifeAreas: [{ en: 'Wealth', hi: 'धन' }, { en: 'Family', hi: 'परिवार' }] },
  { en: 'Courage, siblings, short travel, communication', hi: 'साहस, भाई-बहन, छोटी यात्रा, संवाद', lifeAreas: [{ en: 'Courage', hi: 'साहस' }, { en: 'Siblings', hi: 'भाई-बहन' }] },
  { en: 'Mother, property, happiness, vehicles', hi: 'माता, संपत्ति, सुख, वाहन', lifeAreas: [{ en: 'Property', hi: 'संपत्ति' }, { en: 'Mother', hi: 'माता' }] },
  { en: 'Children, education, intelligence, romance', hi: 'संतान, शिक्षा, बुद्धि, प्रेम', lifeAreas: [{ en: 'Children', hi: 'संतान' }, { en: 'Education', hi: 'शिक्षा' }] },
  { en: 'Enemies, disease, debt, service', hi: 'शत्रु, रोग, ऋण, सेवा', lifeAreas: [{ en: 'Health', hi: 'स्वास्थ्य' }, { en: 'Enemies', hi: 'शत्रु' }] },
  { en: 'Marriage, partnership, business, public dealings', hi: 'विवाह, साझेदारी, व्यापार, जन-संपर्क', lifeAreas: [{ en: 'Marriage', hi: 'विवाह' }, { en: 'Business', hi: 'व्यापार' }] },
  { en: 'Longevity, obstacles, sudden events, inheritance', hi: 'आयु, बाधाएं, अचानक घटनाएं, विरासत', lifeAreas: [{ en: 'Longevity', hi: 'आयु' }, { en: 'Obstacles', hi: 'बाधाएं' }] },
  { en: 'Fortune, dharma, father, long travel', hi: 'भाग्य, धर्म, पिता, लंबी यात्रा', lifeAreas: [{ en: 'Fortune', hi: 'भाग्य' }, { en: 'Dharma', hi: 'धर्म' }] },
  { en: 'Career, karma, status, authority', hi: 'करियर, कर्म, प्रतिष्ठा, अधिकार', lifeAreas: [{ en: 'Career', hi: 'करियर' }, { en: 'Status', hi: 'प्रतिष्ठा' }] },
  { en: 'Income, gains, elder siblings, desires', hi: 'आय, लाभ, बड़े भाई-बहन, इच्छाएं', lifeAreas: [{ en: 'Income', hi: 'आय' }, { en: 'Gains', hi: 'लाभ' }] },
  { en: 'Expenses, losses, foreign travel, moksha', hi: 'व्यय, हानि, विदेश यात्रा, मोक्ष', lifeAreas: [{ en: 'Expenses', hi: 'व्यय' }, { en: 'Moksha', hi: 'मोक्ष' }] },
];

// Remedies — keyed by planet, then house
export const REMEDIES: Record<string, Record<number, Array<{ type: 'feeding' | 'donation' | 'household' | 'action'; category: 'daily' | 'weekly' | 'urgent' | 'general'; en: string; hi: string }>>> = {
  Sun: {
    1: [{ type: 'action', category: 'daily', en: 'Offer water to the Sun every morning', hi: 'प्रतिदिन सुबह सूर्य को जल अर्पित करें' }],
    4: [{ type: 'donation', category: 'weekly', en: 'Donate wheat and jaggery on Sundays', hi: 'रविवार को गेहूं और गुड़ दान करें' }, { type: 'household', category: 'general', en: 'Keep a solid square piece of copper at home', hi: 'घर में तांबे का ठोस चौकोर टुकड़ा रखें' }],
    8: [{ type: 'feeding', category: 'daily', en: 'Feed jaggery to monkeys', hi: 'बंदरों को गुड़ खिलाएं' }, { type: 'action', category: 'urgent', en: 'Do not accept any free item from anyone', hi: 'किसी से मुफ्त वस्तु न लें' }],
    10: [{ type: 'donation', category: 'weekly', en: 'Donate red cloth on Sundays', hi: 'रविवार को लाल कपड़ा दान करें' }],
    12: [{ type: 'action', category: 'urgent', en: 'Throw copper coins in flowing water', hi: 'बहते पानी में तांबे के सिक्के फेंकें' }],
  },
  Moon: {
    1: [{ type: 'action', category: 'daily', en: 'Keep a silver square piece in your pocket', hi: 'जेब में चांदी का चौकोर टुकड़ा रखें' }],
    4: [{ type: 'household', category: 'general', en: 'Keep silver items and water vessels at home', hi: 'घर में चांदी की वस्तुएं और जल पात्र रखें' }],
    6: [{ type: 'donation', category: 'weekly', en: 'Donate milk and rice on Mondays', hi: 'सोमवार को दूध और चावल दान करें' }, { type: 'feeding', category: 'daily', en: 'Feed birds with rice', hi: 'पक्षियों को चावल खिलाएं' }],
    8: [{ type: 'action', category: 'urgent', en: 'Keep rain water in a silver container', hi: 'बारिश का पानी चांदी के बर्तन में रखें' }, { type: 'feeding', category: 'daily', en: 'Offer milk to Shivling', hi: 'शिवलिंग पर दूध चढ़ाएं' }],
    12: [{ type: 'donation', category: 'weekly', en: 'Donate white cloth on Mondays', hi: 'सोमवार को सफेद कपड़ा दान करें' }],
  },
  Mars: {
    1: [{ type: 'feeding', category: 'daily', en: 'Feed sweet chapati to dogs', hi: 'कुत्तों को मीठी रोटी खिलाएं' }],
    4: [{ type: 'household', category: 'general', en: 'Keep deer skin at home', hi: 'घर में हिरण की खाल रखें' }, { type: 'action', category: 'weekly', en: 'Distribute sweets on Tuesdays', hi: 'मंगलवार को मिठाई बांटें' }],
    7: [{ type: 'donation', category: 'urgent', en: 'Donate red lentils (masoor dal)', hi: 'मसूर दाल दान करें' }, { type: 'feeding', category: 'daily', en: 'Feed sweet bread to dogs daily', hi: 'प्रतिदिन कुत्तों को मीठी रोटी खिलाएं' }],
    8: [{ type: 'action', category: 'urgent', en: 'Float red items in flowing water', hi: 'बहते पानी में लाल वस्तुएं बहाएं' }],
    12: [{ type: 'donation', category: 'weekly', en: 'Donate honey and jaggery on Tuesdays', hi: 'मंगलवार को शहद और गुड़ दान करें' }],
  },
  Mercury: {
    1: [{ type: 'household', category: 'general', en: 'Wear a copper coin with a hole in green thread', hi: 'तांबे के सिक्के को हरे धागे में पहनें' }],
    6: [{ type: 'feeding', category: 'daily', en: 'Feed green vegetables to cows', hi: 'गायों को हरी सब्जियां खिलाएं' }],
    8: [{ type: 'action', category: 'urgent', en: 'Float green items in flowing water', hi: 'बहते पानी में हरी वस्तुएं बहाएं' }, { type: 'donation', category: 'weekly', en: 'Donate green moong dal on Wednesdays', hi: 'बुधवार को हरी मूंग दाल दान करें' }],
    10: [{ type: 'household', category: 'general', en: 'Keep a parrot or its picture at workplace', hi: 'कार्यस्थल पर तोता या उसकी तस्वीर रखें' }],
    12: [{ type: 'donation', category: 'weekly', en: 'Donate green cloth on Wednesdays', hi: 'बुधवार को हरा कपड़ा दान करें' }],
  },
  Jupiter: {
    2: [{ type: 'household', category: 'general', en: 'Apply saffron tilak on forehead', hi: 'माथे पर केसर का तिलक लगाएं' }],
    5: [{ type: 'action', category: 'daily', en: 'Apply turmeric tilak daily', hi: 'प्रतिदिन हल्दी का तिलक लगाएं' }],
    8: [{ type: 'action', category: 'urgent', en: 'Keep gold in your house always', hi: 'घर में हमेशा सोना रखें' }, { type: 'donation', category: 'weekly', en: 'Donate turmeric and yellow sweets on Thursdays', hi: 'गुरुवार को हल्दी और पीली मिठाई दान करें' }],
    10: [{ type: 'feeding', category: 'daily', en: 'Feed bananas to cows', hi: 'गायों को केले खिलाएं' }],
    12: [{ type: 'donation', category: 'weekly', en: 'Donate yellow cloth and turmeric on Thursdays', hi: 'गुरुवार को पीला कपड़ा और हल्दी दान करें' }],
  },
  Venus: {
    1: [{ type: 'donation', category: 'weekly', en: 'Donate white items (curd, rice) on Fridays', hi: 'शुक्रवार को सफेद वस्तुएं (दही, चावल) दान करें' }],
    6: [{ type: 'feeding', category: 'daily', en: 'Feed green fodder to cows', hi: 'गायों को हरा चारा खिलाएं' }],
    7: [{ type: 'household', category: 'general', en: 'Use perfume and keep home fragrant', hi: 'इत्र का उपयोग करें और घर को सुगंधित रखें' }],
    8: [{ type: 'action', category: 'urgent', en: 'Float rice in flowing water', hi: 'बहते पानी में चावल बहाएं' }, { type: 'donation', category: 'weekly', en: 'Donate white sweets on Fridays', hi: 'शुक्रवार को सफेद मिठाई दान करें' }],
    12: [{ type: 'donation', category: 'weekly', en: 'Donate silk cloth on Fridays', hi: 'शुक्रवार को रेशमी कपड़ा दान करें' }],
  },
  Saturn: {
    1: [{ type: 'action', category: 'daily', en: 'Apply mustard oil on body before bath', hi: 'नहाने से पहले शरीर पर सरसों का तेल लगाएं' }, { type: 'feeding', category: 'daily', en: 'Feed chapati with mustard oil to crows', hi: 'कौओं को सरसों के तेल की रोटी खिलाएं' }],
    4: [{ type: 'donation', category: 'weekly', en: 'Donate black items on Saturdays', hi: 'शनिवार को काली वस्तुएं दान करें' }],
    7: [{ type: 'action', category: 'urgent', en: 'Keep a dark room in the house for privacy', hi: 'घर में एक अंधेरा कमरा एकांत के लिए रखें' }],
    8: [{ type: 'feeding', category: 'daily', en: 'Feed black dogs with sweet chapati', hi: 'काले कुत्तों को मीठी रोटी खिलाएं' }, { type: 'household', category: 'general', en: 'Keep an iron ball under your bed', hi: 'अपने बिस्तर के नीचे लोहे की गोली रखें' }],
    10: [{ type: 'donation', category: 'weekly', en: 'Donate iron items and mustard oil on Saturdays', hi: 'शनिवार को लोहे की वस्तुएं और सरसों का तेल दान करें' }],
  },
  Rahu: {
    1: [{ type: 'action', category: 'daily', en: 'Keep a solid silver ball in your pocket', hi: 'जेब में चांदी की ठोस गोली रखें' }],
    4: [{ type: 'household', category: 'general', en: 'Store rain water at home', hi: 'घर में बारिश का पानी इकट्ठा करें' }],
    7: [{ type: 'action', category: 'urgent', en: 'Keep barley under your pillow at night', hi: 'रात को तकिए के नीचे जौ रखें' }],
    8: [{ type: 'donation', category: 'weekly', en: 'Donate coconut in a temple', hi: 'मंदिर में नारियल दान करें' }, { type: 'feeding', category: 'daily', en: 'Feed birds daily', hi: 'प्रतिदिन पक्षियों को दाना खिलाएं' }],
    12: [{ type: 'action', category: 'urgent', en: 'Float coconut in flowing water', hi: 'बहते पानी में नारियल बहाएं' }],
  },
  Ketu: {
    1: [{ type: 'feeding', category: 'daily', en: 'Feed stray dogs regularly', hi: 'नियमित रूप से आवारा कुत्तों को खिलाएं' }],
    6: [{ type: 'donation', category: 'weekly', en: 'Donate blanket to a needy person', hi: 'जरूरतमंद को कंबल दान करें' }],
    7: [{ type: 'action', category: 'urgent', en: 'Keep a silver dog figurine at home', hi: 'घर में चांदी का कुत्ते का चित्र रखें' }],
    8: [{ type: 'household', category: 'general', en: 'Keep saffron colored items in prayer room', hi: 'पूजा कक्ष में केसरिया वस्तुएं रखें' }],
    12: [{ type: 'donation', category: 'weekly', en: 'Donate black and white blanket', hi: 'काला-सफेद कंबल दान करें' }, { type: 'feeding', category: 'daily', en: 'Feed fish in a river or pond', hi: 'नदी या तालाब में मछलियों को खिलाएं' }],
  },
};

// ═══ SCORING CONSTANTS ═══
// All numeric thresholds used in scoring/strength functions. Named for auditability.

/** Neutral starting score for any planet evaluation (midpoint of 0-100 scale). */
const SCORE_NEUTRAL_BASE = 50;
/** Bonus when a planet sits in its Pakka Ghar (permanent Lal Kitab house). */
const SCORE_PAKKA_GHAR_BONUS = 30;
/** Bonus when a planet sits in one of the life area's primary houses. */
const SCORE_PRIMARY_HOUSE_BONUS = 20;
/** Bonus when the house the planet occupies is classified as 'strong'. */
const SCORE_STRONG_HOUSE_BONUS = 12;
/** Penalty when the house the planet occupies is classified as 'weak'. */
const SCORE_WEAK_HOUSE_PENALTY = 25;
/** Extra bonus for a naturally benefic planet placed in a primary house. */
const SCORE_BENEFIC_PRIMARY_BONUS = 12;
/** Penalty for a naturally benefic planet placed in a dusthana (6/8/12). */
const SCORE_BENEFIC_DUSTHANA_PENALTY = 10;
/** Penalty for a malefic planet placed in a dusthana (6/8/12). */
const SCORE_MALEFIC_DUSTHANA_PENALTY = 20;
/** Penalty for a malefic in a primary house without Pakka Ghar dignity. */
const SCORE_MALEFIC_NO_DIGNITY_PENALTY = 5;
/** Bonus when another area planet also sits in a primary house (mutual support). */
const SCORE_CO_SUPPORT_BONUS = 5;
/** Bonus for Vargottama placement (same sign in D1 and D9 charts). */
const SCORE_VARGOTTAMA_BONUS = 15;
/** Bonus when planet is exalted in Navamsa (D9) chart. */
const SCORE_NAVAMSA_EXALTED_BONUS = 12;
/** Penalty when planet is debilitated in Navamsa (D9) chart. */
const SCORE_NAVAMSA_DEBILITATED_PENALTY = 15;
/** Floor: minimum score any single planet evaluation can contribute. */
const SCORE_FLOOR = 5;
/** Ceiling: maximum score any single planet evaluation can contribute. */
const SCORE_CEILING = 100;
/** Default area score returned when no planets can be evaluated. */
const SCORE_DEFAULT_EMPTY = 50;

/** Threshold at or above which an area is classified as 'high' confidence. */
const CONFIDENCE_HIGH_THRESHOLD = 70;
/** Threshold at or above which an area is classified as 'moderate' confidence. */
const CONFIDENCE_MODERATE_THRESHOLD = 55;
/** Threshold at or above which an area is classified as 'low' confidence. */
const CONFIDENCE_LOW_THRESHOLD = 40;

/** Degrees per zodiac sign (360 / 12 signs). Used for longitude-to-house conversion. */
const DEGREES_PER_SIGN = 30;
/** Total degrees in the zodiac circle. */
const DEGREES_FULL_CIRCLE = 360;
/** Total number of houses in the chart. */
const TOTAL_HOUSES = 12;
/** Total number of Navamsa divisions per sign. */
const NAVAMSA_DIVISIONS_PER_SIGN = 9;
/** Total Navamsa signs in the cycle. */
const NAVAMSA_SIGN_COUNT = 12;

/** Approximate milliseconds in one year (365.25 days accounting for leap years). */
const MS_PER_YEAR = 365.25 * 24 * 60 * 60 * 1000;

/** Minimum number of malefics in dusthana houses to trigger Karmic Debt (Rini) Dosh. */
const KARMIC_DEBT_MIN_MALEFICS = 2;
/** Number of malefics in dusthana that escalates Karmic Debt severity to 'high'. */
const KARMIC_DEBT_HIGH_MALEFICS = 3;

/** Houses where Saturn placement triggers Shani Dosh. */
const SHANI_DOSH_HOUSES = [1, 4, 7, 8, 10] as const;
/** Saturn in 8th house specifically escalates Shani Dosh to 'high' severity. */
const SHANI_DOSH_HIGH_SEVERITY_HOUSE = 8;
/** Dusthana houses: houses of difficulty (enemies, obstacles, loss). */
const DUSTHANA_HOUSES = [6, 8, 12] as const;
/** House of father/fortune where Sun conjunction triggers Pitra Dosh. */
const PITRA_DOSH_HOUSE = 9;

// ═══ END SCORING CONSTANTS ═══

// Dosha detection
export interface DoshaResult {
  key: string;
  nameEn: string;
  nameHi: string;
  detected: boolean;
  severity: 'high' | 'medium' | 'low';
  descEn: string;
  descHi: string;
  remedyEn: string;
  remedyHi: string;
}

/**
 * Detect Lal Kitab doshas from planet positions.
 * NOTE: Frontend FALLBACK only. Backend source of truth is at:
 *   - GET /api/lalkitab/doshas/{kundli_id}  (dedicated endpoint)
 *   - GET /api/lalkitab/full/{kundli_id}     (consolidated, includes doshas section)
 * Backend engine: app/lalkitab_dosha.py (detect_lalkitab_doshas)
 * LalKitabDoshaTab.tsx prefers backend data and falls back to this function.
 */
function detectDoshas(planetPositions: Record<string, number>): DoshaResult[] {
  const results: DoshaResult[] = [];

  // Pitra Dosh: Sun in 9th house with Saturn or Rahu
  const sunH = planetPositions['Sun'];
  const satH = planetPositions['Saturn'];
  const rahuH = planetPositions['Rahu'];
  const ketuH = planetPositions['Ketu'];
  const moonH = planetPositions['Moon'];
  const pitraDetected = sunH === PITRA_DOSH_HOUSE && (satH === PITRA_DOSH_HOUSE || rahuH === PITRA_DOSH_HOUSE);
  results.push({
    key: 'pitraDosh',
    nameEn: 'Pitra Dosh',
    nameHi: 'पितृ दोष',
    detected: pitraDetected,
    severity: pitraDetected ? 'high' : 'low',
    descEn: 'Ancestors\' unfulfilled karmas causing obstacles in life. Issues with father figures and authority.',
    descHi: 'पूर्वजों के अधूरे कर्म जीवन में बाधाएं डाल रहे हैं। पिता और अधिकारियों से समस्या।',
    remedyEn: 'Feed crows with sweet chapati every Saturday. Donate food to Brahmins on Amavasya.',
    remedyHi: 'हर शनिवार कौओं को मीठी रोटी खिलाएं। अमावस्या पर ब्राह्मणों को भोजन दान करें।',
  });

  // Grahan Dosh: Sun/Moon conjunct Rahu or Ketu
  const grahanDetected = (sunH === rahuH || sunH === ketuH || moonH === rahuH || moonH === ketuH);
  results.push({
    key: 'grahanDosh',
    nameEn: 'Grahan Dosh',
    nameHi: 'ग्रहण दोष',
    detected: grahanDetected,
    severity: grahanDetected ? 'high' : 'low',
    descEn: 'Eclipse-like effect on luminaries. Mental confusion, health issues, and delayed success.',
    descHi: 'ग्रहों पर ग्रहण जैसा प्रभाव। मानसिक भ्रम, स्वास्थ्य समस्या और विलंबित सफलता।',
    remedyEn: 'Float coconut in flowing water. Donate black and white sesame seeds.',
    remedyHi: 'बहते पानी में नारियल बहाएं। काले और सफेद तिल दान करें।',
  });

  // Shani Dosh: Saturn in specific challenging houses
  const shaniDetected = SHANI_DOSH_HOUSES.includes(satH as typeof SHANI_DOSH_HOUSES[number]);
  results.push({
    key: 'shaniDosh',
    nameEn: 'Shani Dosh',
    nameHi: 'शनि दोष',
    detected: shaniDetected,
    severity: shaniDetected ? (satH === SHANI_DOSH_HIGH_SEVERITY_HOUSE ? 'high' : 'medium') : 'low',
    descEn: 'Saturn creating delays, hard work without reward, and karmic lessons in life.',
    descHi: 'शनि देरी, बिना फल के कठिन परिश्रम और कार्मिक सबक दे रहा है।',
    remedyEn: 'Feed crows and black dogs. Donate iron and mustard oil on Saturdays.',
    remedyHi: 'कौओं और काले कुत्तों को खिलाएं। शनिवार को लोहा और सरसों का तेल दान करें।',
  });

  // Karmic Debts: Multiple malefics in dusthana houses (6, 8, 12)
  const marsH = planetPositions['Mars'];
  const maleficsIn6812 = [satH, marsH, rahuH, ketuH].filter(h => (DUSTHANA_HOUSES as readonly number[]).includes(h)).length;
  const karmicDetected = maleficsIn6812 >= KARMIC_DEBT_MIN_MALEFICS;
  results.push({
    key: 'debtKarma',
    nameEn: 'Karmic Debts (Rini Dosh)',
    nameHi: 'कार्मिक ऋण (ऋणी दोष)',
    detected: karmicDetected,
    severity: karmicDetected ? (maleficsIn6812 >= KARMIC_DEBT_HIGH_MALEFICS ? 'high' : 'medium') : 'low',
    descEn: 'Past-life debts manifesting as recurring obstacles, financial issues, or relationship problems.',
    descHi: 'पूर्व जन्म के ऋण बार-बार बाधाओं, वित्तीय समस्याओं या संबंध समस्याओं के रूप में प्रकट हो रहे हैं।',
    remedyEn: 'Donate food and clothes to the needy. Serve elders and parents sincerely.',
    remedyHi: 'जरूरतमंदों को भोजन और कपड़े दान करें। बड़ों और माता-पिता की सच्ची सेवा करें।',
  });

  return results;
}

// House strength
function getHouseStrength(house: number, planetsInHouse: string[]): 'strong' | 'weak' | 'empty' {
  if (planetsInHouse.length === 0) return 'empty';
  const benefics = ['Jupiter', 'Venus', 'Moon', 'Mercury'];
  const malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu'];
  const hasBenefic = planetsInHouse.some(p => benefics.includes(p));
  const hasMalefic = planetsInHouse.some(p => malefics.includes(p));
  if (hasBenefic && !hasMalefic) return 'strong';
  if (hasMalefic && !hasBenefic) return 'weak';
  return 'strong'; // mixed = strong as benefic mitigates
}

// Compute which Lal Kitab age-planet is currently "active" for a given birth date.
// Real behavior: find the age-bucket that contains the person's current age.
// Falls back to first planet (Sun, age 1-6) if no birth date is available — because
// without a birth date we cannot know the age, and the caller must treat this as unknown.
function getActivePlanetForAge(birthDate: string | Date | undefined): typeof AGE_PLANET_ACTIVATION[number] {
  if (!birthDate) return AGE_PLANET_ACTIVATION[0];  // no birth date known
  const bd = typeof birthDate === 'string' ? new Date(birthDate) : birthDate;
  if (isNaN(bd.getTime())) return AGE_PLANET_ACTIVATION[0];
  const now = new Date();
  const ageMs = now.getTime() - bd.getTime();
  const ageYears = Math.floor(ageMs / MS_PER_YEAR);
  const match = AGE_PLANET_ACTIVATION.find(p => ageYears >= p.ageStart && ageYears <= p.ageEnd);
  return match || AGE_PLANET_ACTIVATION[AGE_PLANET_ACTIVATION.length - 1];  // beyond 84 = last one
}

/**
 * Generate a Lal Kitab chart from API data.
 * NOTE: This is a FRONTEND FALLBACK. Backend /api/lalkitab/full/{id}
 * provides the same data with authoritative calculations.
 */
export function generateLalKitabChart(apiData: any, birthDate?: string | Date): LalKitabChartData {
  const planetPositions: Record<string, number> = {};
  const planetLongitudes: Record<string, number> = {};
  const missingPlanets: string[] = [];
  const chartPlanets = apiData?.chart_data?.planets || apiData?.planets || {};

  // Map API planet data to house positions and longitudes
  for (const pObj of PLANETS) {
    const pData = chartPlanets[pObj.key] || chartPlanets[pObj.en];
    if (pData) {
      let house: number | null = null;
      if (typeof pData.house === 'number' && pData.house >= 1 && pData.house <= TOTAL_HOUSES) {
        house = pData.house;
      } else if (typeof pData.House === 'number' && pData.House >= 1 && pData.House <= TOTAL_HOUSES) {
        house = pData.House;
      } else if (typeof pData.longitude === 'number' && pData.longitude >= 0) {
        house = Math.ceil((pData.longitude % DEGREES_FULL_CIRCLE) / DEGREES_PER_SIGN) || null;
        if (house && house > TOTAL_HOUSES) house = ((house - 1) % TOTAL_HOUSES) + 1;
      } else if (typeof pData.degree === 'number' && pData.degree >= 0) {
        house = Math.ceil((pData.degree % DEGREES_FULL_CIRCLE) / DEGREES_PER_SIGN) || null;
        if (house && house > TOTAL_HOUSES) house = ((house - 1) % TOTAL_HOUSES) + 1;
      }

      if (house === null) {
        // Data present but house is indeterminable — treat as missing
        missingPlanets.push(pObj.key);
        planetPositions[pObj.key] = 0;
        planetLongitudes[pObj.key] = NaN;
      } else {
        planetPositions[pObj.key] = house;
        const rawLon = pData.longitude ?? pData.degree ?? 0;
        planetLongitudes[pObj.key] = typeof rawLon === 'number' ? rawLon : parseFloat(rawLon) || 0;
      }
    } else {
      // Planet missing from API — mark incomplete. Do NOT fabricate position.
      missingPlanets.push(pObj.key);
      planetPositions[pObj.key] = 0;  // 0 = unknown house (downstream code should check)
      planetLongitudes[pObj.key] = NaN;
    }
  }

  // Build houses
  const houses: LalKitabHouse[] = [];
  for (let h = 1; h <= TOTAL_HOUSES; h++) {
    const planetsInHouse = Object.entries(planetPositions)
      .filter(([, hNum]) => hNum === h)
      .map(([planet]) => planet);
    houses.push({
      house: h,
      planets: planetsInHouse,
      strength: getHouseStrength(h, planetsInHouse),
    });
  }

  const doshas = detectDoshas(planetPositions);

  // Find currently active planet from the native's age, using birthDate when supplied.
  const activePlanet = getActivePlanetForAge(birthDate);

  return {
    houses,
    planetPositions,
    planetLongitudes,
    doshas,
    activePlanet: activePlanet || null,
    isIncomplete: missingPlanets.length > 0,
    missingPlanets,
  };
}

// ─────────────────────────────────────────────────────────────────
// NISHANIYAN MATCHER DATA
// ─────────────────────────────────────────────────────────────────
export interface NishaniyaSign {
  id: string;
  en: string;
  hi: string;
  category: 'body' | 'household' | 'behavior' | 'family' | 'recurring';
  planet: string;
  badHouses: number[];
  ruleId: string;
}

export const NISHANIYAN_SIGNS: NishaniyaSign[] = [
  // Sun
  { id: 'sun_eye', en: 'Frequent eye strain or weak eyesight', hi: 'बार-बार आँखों में थकान या कमजोर नज़र', category: 'body', planet: 'Sun', badHouses: [4, 6, 8, 12], ruleId: 'N-SUN-001' },
  { id: 'sun_authority', en: 'Obstacles from bosses or authority figures', hi: 'अधिकारियों या वरिष्ठों से बाधाएं', category: 'recurring', planet: 'Sun', badHouses: [4, 8], ruleId: 'N-SUN-002' },
  { id: 'sun_father', en: "Father's health issues or conflicts with father", hi: 'पिता का स्वास्थ्य खराब या पिता से विवाद', category: 'family', planet: 'Sun', badHouses: [4, 9, 12], ruleId: 'N-SUN-003' },
  { id: 'sun_govt', en: 'Legal or government-related problems', hi: 'कानूनी या सरकारी समस्याएं', category: 'recurring', planet: 'Sun', badHouses: [6, 8, 12], ruleId: 'N-SUN-004' },
  // Moon
  { id: 'moon_sleep', en: 'Irregular sleep or vivid disturbing dreams', hi: 'अनियमित नींद या परेशान करने वाले सपने', category: 'body', planet: 'Moon', badHouses: [6, 8, 12], ruleId: 'N-MON-001' },
  { id: 'moon_mother', en: "Mother has frequent health issues", hi: 'माता को बार-बार स्वास्थ्य समस्याएं', category: 'family', planet: 'Moon', badHouses: [6, 8], ruleId: 'N-MON-002' },
  { id: 'moon_emotion', en: 'Strong emotional instability or mood swings', hi: 'भावनात्मक अस्थिरता या मनोदशा में उतार-चढ़ाव', category: 'behavior', planet: 'Moon', badHouses: [1, 6, 8], ruleId: 'N-MON-003' },
  { id: 'moon_water', en: 'Water-related problems at home (leaks, floods)', hi: 'घर में पानी की समस्याएं (रिसाव, बाढ़)', category: 'household', planet: 'Moon', badHouses: [4, 8, 12], ruleId: 'N-MON-004' },
  // Mars
  { id: 'mars_accident', en: 'Frequent minor cuts, burns, or accidents', hi: 'बार-बार छोटे कट, जलन या दुर्घटनाएं', category: 'body', planet: 'Mars', badHouses: [1, 6, 8], ruleId: 'N-MAR-001' },
  { id: 'mars_brother', en: 'Disputes with brothers or male relatives', hi: 'भाइयों या पुरुष रिश्तेदारों से विवाद', category: 'family', planet: 'Mars', badHouses: [3, 6], ruleId: 'N-MAR-002' },
  { id: 'mars_land', en: 'Land or property disputes recurring', hi: 'जमीन या संपत्ति विवाद बार-बार', category: 'recurring', planet: 'Mars', badHouses: [4, 7, 12], ruleId: 'N-MAR-003' },
  { id: 'mars_anger', en: 'Uncontrollable anger causing problems', hi: 'बेकाबू गुस्से से समस्याएं', category: 'behavior', planet: 'Mars', badHouses: [1, 4, 7], ruleId: 'N-MAR-004' },
  // Mercury
  { id: 'merc_memory', en: 'Memory lapses or difficulty concentrating', hi: 'स्मृति हानि या एकाग्रता में कठिनाई', category: 'body', planet: 'Mercury', badHouses: [6, 8, 12], ruleId: 'N-MER-001' },
  { id: 'merc_speech', en: 'Speech issues or communication misunderstandings', hi: 'वाणी समस्या या संवाद में गलतफहमी', category: 'behavior', planet: 'Mercury', badHouses: [2, 6, 8], ruleId: 'N-MER-002' },
  { id: 'merc_skin', en: 'Recurring skin rashes or nervous system issues', hi: 'बार-बार त्वचा पर चकत्ते या तंत्रिका समस्याएं', category: 'body', planet: 'Mercury', badHouses: [6, 8], ruleId: 'N-MER-003' },
  // Jupiter
  { id: 'jupi_children', en: 'Children face educational or health difficulties', hi: 'बच्चों को शैक्षिक या स्वास्थ्य कठिनाइयां', category: 'family', planet: 'Jupiter', badHouses: [5, 6, 8], ruleId: 'N-JUP-001' },
  { id: 'jupi_finance', en: 'Unexpected financial losses despite honest effort', hi: 'ईमानदार प्रयास के बावजूद अप्रत्याशित वित्तीय हानि', category: 'recurring', planet: 'Jupiter', badHouses: [6, 8, 12], ruleId: 'N-JUP-002' },
  { id: 'jupi_weight', en: 'Unexplained weight gain or liver issues', hi: 'अकारण वजन बढ़ना या लीवर की समस्या', category: 'body', planet: 'Jupiter', badHouses: [1, 2, 6], ruleId: 'N-JUP-003' },
  // Venus
  { id: 'venu_marriage', en: 'Marriage delays or repeated relationship breakdowns', hi: 'विवाह में देरी या बार-बार रिश्ते टूटना', category: 'recurring', planet: 'Venus', badHouses: [6, 8, 12], ruleId: 'N-VEN-001' },
  { id: 'venu_female', en: 'Female relatives (wife/sister) face frequent health issues', hi: 'पत्नी या बहन को बार-बार स्वास्थ्य समस्याएं', category: 'family', planet: 'Venus', badHouses: [6, 8], ruleId: 'N-VEN-002' },
  { id: 'venu_luxury', en: 'Repeated loss of valuables or luxury items', hi: 'बार-बार कीमती या विलास वस्तुओं का नुकसान', category: 'household', planet: 'Venus', badHouses: [8, 12], ruleId: 'N-VEN-003' },
  // Saturn
  { id: 'satu_delay', en: 'Projects and plans get endlessly delayed', hi: 'परियोजनाएं और योजनाएं बार-बार टलती रहती हैं', category: 'recurring', planet: 'Saturn', badHouses: [1, 4, 7], ruleId: 'N-SAT-001' },
  { id: 'satu_joints', en: 'Chronic joint pain, back pain, or bone issues', hi: 'पुराना जोड़ दर्द, कमर दर्द या हड्डी की समस्या', category: 'body', planet: 'Saturn', badHouses: [1, 6, 8], ruleId: 'N-SAT-002' },
  { id: 'satu_servant', en: 'Repeated issues with employees or servants', hi: 'कर्मचारियों या सेवकों से बार-बार समस्याएं', category: 'recurring', planet: 'Saturn', badHouses: [6, 10], ruleId: 'N-SAT-003' },
  { id: 'satu_isolation', en: 'Feeling of loneliness or social isolation', hi: 'अकेलेपन या सामाजिक एकांत की भावना', category: 'behavior', planet: 'Saturn', badHouses: [1, 12], ruleId: 'N-SAT-004' },
  // Rahu
  { id: 'rahu_fear', en: 'Unexplained fears or anxiety, especially at night', hi: 'रात को अकारण भय या चिंता', category: 'behavior', planet: 'Rahu', badHouses: [4, 8, 12], ruleId: 'N-RAH-001' },
  { id: 'rahu_tech', en: 'Technology devices repeatedly malfunction or break', hi: 'तकनीकी उपकरण बार-बार खराब होते हैं', category: 'household', planet: 'Rahu', badHouses: [3, 8], ruleId: 'N-RAH-002' },
  { id: 'rahu_foreign', en: 'Unexpected foreign connections or confusing situations', hi: 'अप्रत्याशित विदेशी संपर्क या भ्रामक स्थितियां', category: 'recurring', planet: 'Rahu', badHouses: [7, 9, 12], ruleId: 'N-RAH-003' },
  // Ketu
  { id: 'ketu_health', en: 'Mysterious illnesses doctors cannot easily diagnose', hi: 'रहस्यमय बीमारियां जो डॉक्टर पहचान नहीं सकते', category: 'body', planet: 'Ketu', badHouses: [1, 6, 8], ruleId: 'N-KET-001' },
  { id: 'ketu_pets', en: 'Pets fall ill or die repeatedly', hi: 'पालतू जानवर बार-बार बीमार पड़ते या मरते हैं', category: 'household', planet: 'Ketu', badHouses: [6, 8], ruleId: 'N-KET-002' },
  { id: 'ketu_detach', en: 'Feeling disconnected from material goals', hi: 'भौतिक लक्ष्यों से अलगाव की भावना', category: 'behavior', planet: 'Ketu', badHouses: [1, 7, 10], ruleId: 'N-KET-003' },
];

// ─────────────────────────────────────────────────────────────────
// PREDICTION STUDIO — life area categories
// ─────────────────────────────────────────────────────────────────
export interface PredictionArea {
  key: string;
  en: string;
  hi: string;
  primaryHouses: number[];
  primaryPlanets: string[];
  positiveEn: string;
  positiveHi: string;
  cautionEn: string;
  cautionHi: string;
  remedyEn: string;
  remedyHi: string;
}

export const PREDICTION_AREAS: PredictionArea[] = [
  {
    key: 'career',
    en: 'Career & Authority',
    hi: 'करियर और अधिकार',
    primaryHouses: [10, 1, 6],
    primaryPlanets: ['Sun', 'Saturn', 'Mars'],
    positiveEn: 'Career advancement and recognition in authority roles likely.',
    positiveHi: 'करियर में उन्नति और अधिकार पदों में पहचान संभव।',
    cautionEn: 'Avoid confrontations at workplace. Delays in promotions possible.',
    cautionHi: 'कार्यस्थल पर टकराव से बचें। पदोन्नति में देरी संभव।',
    remedyEn: 'Offer water to the Sun every morning. Donate wheat on Sundays.',
    remedyHi: 'प्रतिदिन सुबह सूर्य को जल चढ़ाएं। रविवार को गेहूं दान करें।',
  },
  {
    key: 'money',
    en: 'Money & Finance',
    hi: 'धन और वित्त',
    primaryHouses: [2, 11, 8],
    primaryPlanets: ['Jupiter', 'Venus', 'Mercury'],
    positiveEn: 'Financial gains and wealth accumulation favored.',
    positiveHi: 'वित्तीय लाभ और धन संचय अनुकूल।',
    cautionEn: 'Avoid risky investments. Unexpected expenses possible.',
    cautionHi: 'जोखिम भरे निवेश से बचें। अप्रत्याशित खर्च संभव।',
    remedyEn: 'Apply saffron tilak daily. Keep gold in your home.',
    remedyHi: 'प्रतिदिन केसर का तिलक लगाएं। घर में सोना रखें।',
  },
  {
    key: 'relationship',
    en: 'Relationship & Marriage',
    hi: 'रिश्ते और विवाह',
    primaryHouses: [7, 5, 2],
    primaryPlanets: ['Venus', 'Moon', 'Jupiter'],
    positiveEn: 'Harmonious relationships and marital happiness likely.',
    positiveHi: 'सामंजस्यपूर्ण रिश्ते और वैवाहिक सुख संभव।',
    cautionEn: 'Communication gaps in relationships. Avoid major decisions.',
    cautionHi: 'रिश्तों में संवाद की कमी। बड़े फैसलों से बचें।',
    remedyEn: 'Keep home fragrant. Donate white items on Fridays.',
    remedyHi: 'घर को सुगंधित रखें। शुक्रवार को सफेद वस्तुएं दान करें।',
  },
  {
    key: 'family',
    en: 'Family & Home',
    hi: 'परिवार और घर',
    primaryHouses: [4, 2, 9],
    primaryPlanets: ['Moon', 'Jupiter', 'Mercury'],
    positiveEn: 'Domestic happiness and family harmony. Property gains possible.',
    positiveHi: 'गृह सुख और पारिवारिक सामंजस्य। संपत्ति लाभ संभव।',
    cautionEn: "Family conflicts possible. Take care of mother's health.",
    cautionHi: 'पारिवारिक विवाद संभव। माता के स्वास्थ्य का ध्यान रखें।',
    remedyEn: 'Keep silver items at home. Offer water to plants daily.',
    remedyHi: 'घर में चांदी की वस्तुएं रखें। प्रतिदिन पौधों को जल दें।',
  },
  {
    key: 'health',
    en: 'Health & Vitality',
    hi: 'स्वास्थ्य और जीवन शक्ति',
    primaryHouses: [1, 6, 8],
    primaryPlanets: ['Sun', 'Mars', 'Saturn'],
    positiveEn: 'Good health and physical vitality. Fast recovery from illness.',
    positiveHi: 'अच्छा स्वास्थ्य और शारीरिक जीवन शक्ति। बीमारी से जल्दी ठीक होना।',
    cautionEn: 'Health needs attention. Avoid stress and overwork.',
    cautionHi: 'स्वास्थ्य पर ध्यान दें। तनाव और अति-परिश्रम से बचें।',
    remedyEn: 'Apply mustard oil before bath. Feed crows on Saturdays.',
    remedyHi: 'नहाने से पहले सरसों का तेल लगाएं। शनिवार को कौओं को खिलाएं।',
  },
  {
    key: 'travel',
    en: 'Travel & Foreign',
    hi: 'यात्रा और विदेश',
    primaryHouses: [9, 12, 3],
    primaryPlanets: ['Jupiter', 'Rahu', 'Mercury'],
    positiveEn: 'Beneficial travels and foreign opportunities.',
    positiveHi: 'लाभदायक यात्राएं और विदेशी अवसर।',
    cautionEn: 'Travel disruptions possible. Verify documents before trips.',
    cautionHi: 'यात्रा में बाधाएं संभव। यात्रा से पहले दस्तावेज जांचें।',
    remedyEn: 'Float coconut in flowing water. Keep a silver ball in pocket.',
    remedyHi: 'बहते पानी में नारियल बहाएं। जेब में चांदी की गोली रखें।',
  },
  {
    key: 'legal',
    en: 'Legal & Conflicts',
    hi: 'कानूनी और विवाद',
    primaryHouses: [6, 8, 12],
    primaryPlanets: ['Mars', 'Saturn', 'Rahu'],
    positiveEn: 'Legal matters resolve favorably. Enemies are defeated.',
    positiveHi: 'कानूनी मामले अनुकूल रूप से सुलझते हैं। शत्रुओं पर विजय।',
    cautionEn: 'Avoid legal disputes. Be careful of hidden enemies.',
    cautionHi: 'कानूनी विवादों से बचें। छिपे शत्रुओं से सावधान रहें।',
    remedyEn: 'Donate red lentils on Tuesdays. Float red items in water.',
    remedyHi: 'मंगलवार को मसूर दाल दान करें। पानी में लाल वस्तुएं बहाएं।',
  },
  {
    key: 'spiritual',
    en: 'Spiritual Growth',
    hi: 'आध्यात्मिक विकास',
    primaryHouses: [9, 12, 5],
    primaryPlanets: ['Jupiter', 'Ketu', 'Sun'],
    positiveEn: 'Strong spiritual progress and inner growth. Guru connection.',
    positiveHi: 'मजबूत आध्यात्मिक प्रगति और आंतरिक विकास। गुरु संबंध।',
    cautionEn: 'Spiritual practice needed. Connect with a mentor or teacher.',
    cautionHi: 'आध्यात्मिक अभ्यास आवश्यक। किसी गुरु या शिक्षक से जुड़ें।',
    remedyEn: 'Feed stray dogs. Apply turmeric tilak on Thursdays.',
    remedyHi: 'आवारा कुत्तों को खिलाएं। गुरुवार को हल्दी का तिलक लगाएं।',
  },
];

// Navamsa (D9) exaltation and debilitation signs (0-indexed, 0=Aries)
const NAVAMSA_EXALT: Record<string, number> = {
  Sun: 0, Moon: 1, Mars: 9, Mercury: 5, Jupiter: 3, Venus: 11, Saturn: 6, Rahu: 1, Ketu: 8,
};
const NAVAMSA_DEBIL: Record<string, number> = {
  Sun: 6, Moon: 7, Mars: 3, Mercury: 11, Jupiter: 9, Venus: 5, Saturn: 0, Rahu: 7, Ketu: 2,
};

/**
 * Compute area scores for chart analysis dashboard.
 * NOTE: Frontend fallback. Uses named constants below for all thresholds.
 * Backend strength model: app/lalkitab_engine.get_planet_strength_detailed()
 */
export function computeAreaScore(
  area: PredictionArea,
  planetPositions: Record<string, number>,
  houses: LalKitabHouse[],
  planetLongitudes?: Record<string, number>,
): number {
  let totalScore = 0;
  let count = 0;
  const benefics = new Set(['Jupiter', 'Venus', 'Moon', 'Mercury']);
  const malefics = new Set(['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']);
  const dushthanas = new Set(DUSTHANA_HOUSES);

  for (const planetKey of area.primaryPlanets) {
    const house = planetPositions[planetKey];
    if (house == null) continue;
    let score = SCORE_NEUTRAL_BASE;

    // Pakka Ghar: planet in its own LK house — strong dignity
    const isPakka = house === PAKKA_GHAR[planetKey];
    if (isPakka) score += SCORE_PAKKA_GHAR_BONUS;

    // Planet in a house that directly supports this life area
    const inPrimaryHouse = area.primaryHouses.includes(house);
    if (inPrimaryHouse) score += SCORE_PRIMARY_HOUSE_BONUS;

    // House strength from chart calculation
    const houseData = houses.find((h) => h.house === house);
    if (houseData?.strength === 'strong') score += SCORE_STRONG_HOUSE_BONUS;
    if (houseData?.strength === 'weak') score -= SCORE_WEAK_HOUSE_PENALTY;

    // Benefic in a primary house → extra support
    if (benefics.has(planetKey) && inPrimaryHouse) score += SCORE_BENEFIC_PRIMARY_BONUS;
    // Benefic in dusthana → less effective
    if (benefics.has(planetKey) && dushthanas.has(house)) score -= SCORE_BENEFIC_DUSTHANA_PENALTY;

    // Malefic in dusthana → harms the area
    if (malefics.has(planetKey) && dushthanas.has(house)) score -= SCORE_MALEFIC_DUSTHANA_PENALTY;
    // Malefic in primary house without dignity → mixed influence
    if (malefics.has(planetKey) && inPrimaryHouse && !isPakka) score -= SCORE_MALEFIC_NO_DIGNITY_PENALTY;

    // Mutual support: another area planet also placed in a primary house
    const coSupport = area.primaryPlanets.filter(
      (p) => p !== planetKey && area.primaryHouses.includes(planetPositions[p] ?? -1),
    ).length;
    if (coSupport > 0) score += SCORE_CO_SUPPORT_BONUS;

    // Navamsa (D9) dignity — vargottama, exaltation, debilitation
    if (planetLongitudes) {
      const lon = planetLongitudes[planetKey] ?? 0;
      const d1Sign = Math.floor(lon / DEGREES_PER_SIGN) % NAVAMSA_SIGN_COUNT;
      const pada = Math.floor((lon % DEGREES_PER_SIGN) * NAVAMSA_DIVISIONS_PER_SIGN / DEGREES_PER_SIGN);
      const navamsaSign = (d1Sign * NAVAMSA_DIVISIONS_PER_SIGN + pada) % NAVAMSA_SIGN_COUNT;
      if (d1Sign === navamsaSign) score += SCORE_VARGOTTAMA_BONUS;
      if (NAVAMSA_EXALT[planetKey] === navamsaSign) score += SCORE_NAVAMSA_EXALTED_BONUS;
      if (NAVAMSA_DEBIL[planetKey] === navamsaSign) score -= SCORE_NAVAMSA_DEBILITATED_PENALTY;
    }

    totalScore += Math.max(SCORE_FLOOR, Math.min(SCORE_CEILING, score));
    count++;
  }

  if (count === 0) return SCORE_DEFAULT_EMPTY;
  return Math.round(totalScore / count);
}

/** Map score 0-100 to a confidence label */
export function scoreToConfidence(score: number): 'high' | 'moderate' | 'low' | 'speculative' {
  if (score >= CONFIDENCE_HIGH_THRESHOLD) return 'high';
  if (score >= CONFIDENCE_MODERATE_THRESHOLD) return 'moderate';
  if (score >= CONFIDENCE_LOW_THRESHOLD) return 'low';
  return 'speculative';
}

// ─────────────────────────────────────────────────────────────────
// CHANDRA CHALANA — 43-day protocol tasks
// ─────────────────────────────────────────────────────────────────
export interface ChandraChaalanaTask {
  day: number;
  en: string;
  hi: string;
  category: 'action' | 'donation' | 'meditation' | 'fasting' | 'mantra';
}

export const CHANDRA_CHAALANA_TASKS: ChandraChaalanaTask[] = [
  { day: 1, en: 'Begin with a cold water bath at sunrise. Offer white flowers to Moon image.', hi: 'सूर्योदय पर ठंडे पानी से स्नान करें। चंद्रमा की छवि पर सफेद फूल चढ़ाएं।', category: 'action' },
  { day: 2, en: 'Donate white rice and milk to a needy family.', hi: 'किसी जरूरतमंद परिवार को सफेद चावल और दूध दान करें।', category: 'donation' },
  { day: 3, en: 'Recite "Om Som Somaya Namaha" 108 times after moonrise.', hi: 'चंद्रोदय के बाद "ॐ सोम सोमाय नमः" 108 बार जपें।', category: 'mantra' },
  { day: 4, en: 'Keep a silver glass of water by your bedside. Pour it on a plant in the morning.', hi: 'बिस्तर के पास चांदी के गिलास में पानी रखें। सुबह पौधे पर डालें।', category: 'action' },
  { day: 5, en: 'Fast on rice and milk only. No fried or spicy food.', hi: 'केवल चावल और दूध पर उपवास रखें। तला या मसालेदार नहीं।', category: 'fasting' },
  { day: 6, en: 'Feed fish or birds with rice at a water body.', hi: 'नदी या तालाब में मछलियों या पक्षियों को चावल खिलाएं।', category: 'action' },
  { day: 7, en: 'Meditate on a full moon image for 15 minutes. Visualize calm blue light.', hi: 'पूर्णिमा की छवि पर 15 मिनट ध्यान करें। शांत नीली रोशनी की कल्पना करें।', category: 'meditation' },
  { day: 8, en: 'Wear white or cream clothes all day. Avoid black and red.', hi: 'पूरे दिन सफेद या क्रीम कपड़े पहनें। काले और लाल से बचें।', category: 'action' },
  { day: 9, en: 'Donate a white bedsheet or white cloth to an elderly woman.', hi: 'किसी बुजुर्ग महिला को सफेद चादर या सफेद कपड़ा दान करें।', category: 'donation' },
  { day: 10, en: 'Offer milk to a Shivling. If no temple nearby, pour milk on a plant root.', hi: 'शिवलिंग पर दूध चढ़ाएं। नजदीक मंदिर न हो तो पौधे की जड़ में दूध डालें।', category: 'action' },
  { day: 11, en: 'Recite "Om Chandraya Namaha" 108 times while holding a silver piece.', hi: 'चांदी का टुकड़ा पकड़कर "ॐ चंद्राय नमः" 108 बार जपें।', category: 'mantra' },
  { day: 12, en: 'Avoid alcohol and non-vegetarian food strictly today.', hi: 'आज शराब और मांसाहारी भोजन से सख्ती से परहेज करें।', category: 'fasting' },
  { day: 13, en: 'Write a letter of gratitude to your mother. Keep it with you.', hi: 'अपनी माँ को कृतज्ञता का पत्र लिखें। उसे अपने पास रखें।', category: 'meditation' },
  { day: 14, en: 'Wash a square piece of silver and keep it on you all day.', hi: 'चांदी के चौकोर टुकड़े को धोएं और पूरे दिन अपने पास रखें।', category: 'action' },
  { day: 15, en: 'Mid-point milestone: donate white sweets to at least 7 people.', hi: 'मध्य बिंदु: कम से कम 7 लोगों को सफेद मिठाई दान करें।', category: 'donation' },
  { day: 16, en: 'Take a bath with sandalwood-mixed water. Avoid soap today.', hi: 'चंदन मिले पानी से स्नान करें। आज साबुन से बचें।', category: 'action' },
  { day: 17, en: 'Meditate near open water (river, lake, or fountain) for 20 minutes.', hi: 'खुले पानी (नदी, झील, फव्वारे) के पास 20 मिनट ध्यान करें।', category: 'meditation' },
  { day: 18, en: 'Recite "Om Hreem Chandraya Namaha" 108 times.', hi: '"ॐ ह्रीं चंद्राय नमः" 108 बार जपें।', category: 'mantra' },
  { day: 19, en: 'Donate milk and rice to a temple or orphanage.', hi: 'किसी मंदिर या अनाथालय में दूध और चावल दान करें।', category: 'donation' },
  { day: 20, en: 'Keep your home clean and free of clutter. Light a white candle.', hi: 'अपना घर साफ और गंदगी मुक्त रखें। एक सफेद मोमबत्ती जलाएं।', category: 'action' },
  { day: 21, en: 'Three-week milestone: observe silence for 2 hours in the evening.', hi: 'तीन सप्ताह का मील का पत्थर: शाम को 2 घंटे मौन रखें।', category: 'meditation' },
  { day: 22, en: 'Feed crows and birds with white rice in the morning.', hi: 'सुबह कौओं और पक्षियों को सफेद चावल खिलाएं।', category: 'action' },
  { day: 23, en: 'Donate a white umbrella or white cloth to a needy person.', hi: 'किसी जरूरतमंद को सफेद छाता या सफेद कपड़ा दान करें।', category: 'donation' },
  { day: 24, en: 'Recite the Chandra Gayatri Mantra 21 times after moonrise.', hi: 'चंद्रोदय के बाद चंद्र गायत्री मंत्र 21 बार जपें।', category: 'mantra' },
  { day: 25, en: 'Eat only sattvic food (no garlic or onion). Drink coconut water.', hi: 'केवल सात्विक भोजन करें (लहसुन-प्याज नहीं)। नारियल पानी पीएं।', category: 'fasting' },
  { day: 26, en: 'Spend time near a water body or watch the moon rise today.', hi: 'पानी के पास समय बिताएं या आज चंद्रोदय देखें।', category: 'meditation' },
  { day: 27, en: 'Write down 27 things you are grateful for in your life.', hi: 'अपने जीवन में जिन 27 चीजों के लिए आभारी हैं उन्हें लिखें।', category: 'meditation' },
  { day: 28, en: 'Float a coconut with white flowers in flowing water.', hi: 'बहते पानी में सफेद फूलों के साथ नारियल बहाएं।', category: 'action' },
  { day: 29, en: 'Donate a silver coin to a place of worship.', hi: 'किसी पूजा स्थल पर चांदी का सिक्का दान करें।', category: 'donation' },
  { day: 30, en: 'Recite Moon mantra 108 times. Meditate for 15 minutes.', hi: 'चंद्र मंत्र 108 बार जपें। 15 मिनट ध्यान करें।', category: 'mantra' },
  { day: 31, en: 'Keep a bowl of milk on your rooftop under moonlight overnight.', hi: 'रात भर छत पर दूध का कटोरा चांदनी में रखें।', category: 'action' },
  { day: 32, en: 'Complete fast today. Consume only water and milk.', hi: 'आज पूर्ण उपवास रखें। केवल पानी और दूध लें।', category: 'fasting' },
  { day: 33, en: 'Write a letter of intention — what change you want from this protocol.', hi: 'एक इरादे का पत्र लिखें — इस प्रोटोकॉल से आप क्या बदलाव चाहते हैं।', category: 'meditation' },
  { day: 34, en: 'Donate white sesame seeds and rice to a Shiva temple.', hi: 'शिव मंदिर में सफेद तिल और चावल दान करें।', category: 'donation' },
  { day: 35, en: 'Recite Moon mantra 108 times walking barefoot on grass at dawn.', hi: 'भोर में घास पर नंगे पांव चलते हुए चंद्र मंत्र 108 बार जपें।', category: 'mantra' },
  { day: 36, en: 'Keep your water intake high. Drink from a silver cup if possible.', hi: 'पानी की मात्रा अधिक रखें। हो सके तो चांदी के कप से पीएं।', category: 'action' },
  { day: 37, en: 'Donate food (rice, lentils, milk) to at least 43 people.', hi: 'कम से कम 43 लोगों को खाना (चावल, दाल, दूध) दान करें।', category: 'donation' },
  { day: 38, en: 'Meditate on white light filling your body for 20 minutes.', hi: 'सफेद रोशनी से अपना शरीर भरने पर 20 मिनट ध्यान करें।', category: 'meditation' },
  { day: 39, en: 'Recite "Om Shrim Chandra Namaha" 1008 times today.', hi: '"ॐ श्रीम् चंद्र नमः" आज 1008 बार जपें।', category: 'mantra' },
  { day: 40, en: 'Offer white flowers and milk at a Shiva or Devi temple.', hi: 'शिव या देवी मंदिर में सफेद फूल और दूध चढ़ाएं।', category: 'action' },
  { day: 41, en: 'Reflect on the last 40 days. Write what has changed or improved.', hi: 'पिछले 40 दिनों पर विचार करें। लिखें क्या बदला या बेहतर हुआ।', category: 'meditation' },
  { day: 42, en: 'Donate a small pearl or white cloth to a senior female family member.', hi: 'परिवार की वरिष्ठ महिला को छोटा मोती या सफेद कपड़ा दान करें।', category: 'donation' },
  { day: 43, en: 'Final day: Float 43 white flowers in flowing water. Chandra Chalana complete!', hi: 'अंतिम दिन: बहते पानी में 43 सफेद फूल बहाएं। चंद्र चालना पूर्ण!', category: 'action' },
];
