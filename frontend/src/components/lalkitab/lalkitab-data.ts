// Lal Kitab data types and constants

export interface LalKitabHouse {
  house: number;
  planets: string[];
  strength: 'strong' | 'weak' | 'empty';
}

export interface LalKitabChartData {
  houses: LalKitabHouse[];
  planetPositions: Record<string, number>;
  doshas: DoshaResult[];
  activePlanet: { planet: string; ageStart: number; ageEnd: number } | null;
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

export function detectDoshas(planetPositions: Record<string, number>): DoshaResult[] {
  const results: DoshaResult[] = [];

  // Pitra Dosh: Sun in 9th house with Saturn or Rahu
  const sunH = planetPositions['Sun'];
  const satH = planetPositions['Saturn'];
  const rahuH = planetPositions['Rahu'];
  const ketuH = planetPositions['Ketu'];
  const moonH = planetPositions['Moon'];
  const pitraDetected = sunH === 9 && (satH === 9 || rahuH === 9);
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

  // Shani Dosh: Saturn in 1, 4, 7, 8, or 10
  const shaniDetected = [1, 4, 7, 8, 10].includes(satH);
  results.push({
    key: 'shaniDosh',
    nameEn: 'Shani Dosh',
    nameHi: 'शनि दोष',
    detected: shaniDetected,
    severity: shaniDetected ? (satH === 8 ? 'high' : 'medium') : 'low',
    descEn: 'Saturn creating delays, hard work without reward, and karmic lessons in life.',
    descHi: 'शनि देरी, बिना फल के कठिन परिश्रम और कार्मिक सबक दे रहा है।',
    remedyEn: 'Feed crows and black dogs. Donate iron and mustard oil on Saturdays.',
    remedyHi: 'कौओं और काले कुत्तों को खिलाएं। शनिवार को लोहा और सरसों का तेल दान करें।',
  });

  // Karmic Debts: Multiple malefics in 6, 8, 12
  const marsH = planetPositions['Mars'];
  const maleficsIn6812 = [satH, marsH, rahuH, ketuH].filter(h => [6, 8, 12].includes(h)).length;
  const karmicDetected = maleficsIn6812 >= 2;
  results.push({
    key: 'debtKarma',
    nameEn: 'Karmic Debts (Rini Dosh)',
    nameHi: 'कार्मिक ऋण (ऋणी दोष)',
    detected: karmicDetected,
    severity: karmicDetected ? (maleficsIn6812 >= 3 ? 'high' : 'medium') : 'low',
    descEn: 'Past-life debts manifesting as recurring obstacles, financial issues, or relationship problems.',
    descHi: 'पूर्व जन्म के ऋण बार-बार बाधाओं, वित्तीय समस्याओं या संबंध समस्याओं के रूप में प्रकट हो रहे हैं।',
    remedyEn: 'Donate food and clothes to the needy. Serve elders and parents sincerely.',
    remedyHi: 'जरूरतमंदों को भोजन और कपड़े दान करें। बड़ों और माता-पिता की सच्ची सेवा करें।',
  });

  return results;
}

// House strength
export function getHouseStrength(house: number, planetsInHouse: string[]): 'strong' | 'weak' | 'empty' {
  if (planetsInHouse.length === 0) return 'empty';
  const benefics = ['Jupiter', 'Venus', 'Moon', 'Mercury'];
  const malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu'];
  const hasBenefic = planetsInHouse.some(p => benefics.includes(p));
  const hasMalefic = planetsInHouse.some(p => malefics.includes(p));
  if (hasBenefic && !hasMalefic) return 'strong';
  if (hasMalefic && !hasBenefic) return 'weak';
  return 'strong'; // mixed = strong as benefic mitigates
}

// Generate Lal Kitab chart from API data
export function generateLalKitabChart(apiData: any): LalKitabChartData {
  const planetPositions: Record<string, number> = {};
  const chartPlanets = apiData?.chart_data?.planets || apiData?.planets || {};

  // Map API planet data to house positions
  for (const pObj of PLANETS) {
    const pData = chartPlanets[pObj.key] || chartPlanets[pObj.en];
    if (pData) {
      const house = pData.house || pData.House || Math.ceil(((pData.longitude || pData.degree || 0) % 360) / 30) || 1;
      planetPositions[pObj.key] = typeof house === 'number' ? house : parseInt(house) || 1;
    } else {
      // Fallback: distribute planets across houses
      planetPositions[pObj.key] = (PLANETS.indexOf(pObj) % 12) + 1;
    }
  }

  // Build houses
  const houses: LalKitabHouse[] = [];
  for (let h = 1; h <= 12; h++) {
    const planetsInHouse = Object.entries(planetPositions)
      .filter(([_, hNum]) => hNum === h)
      .map(([planet]) => planet);
    houses.push({
      house: h,
      planets: planetsInHouse,
      strength: getHouseStrength(h, planetsInHouse),
    });
  }

  const doshas = detectDoshas(planetPositions);

  // Find currently active planet (placeholder — actual age would be calculated in component)
  const activePlanet = AGE_PLANET_ACTIVATION[0];

  return {
    houses,
    planetPositions,
    doshas,
    activePlanet: activePlanet || null,
  };
}
