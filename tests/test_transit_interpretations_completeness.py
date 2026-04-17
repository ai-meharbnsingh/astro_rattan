from app.transit_interpretations import TRANSIT_FRAGMENTS


def test_transit_fragments_include_9_planets_and_full_matrix():
    expected_planets = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(TRANSIT_FRAGMENTS.keys()) == expected_planets

    expected_houses = set(range(1, 13))
    expected_areas = {"general", "love", "career", "finance", "health"}
    expected_langs = {"en", "hi"}

    for planet in expected_planets:
        houses = TRANSIT_FRAGMENTS[planet]
        assert set(houses.keys()) == expected_houses
        for house in expected_houses:
            areas = houses[house]
            assert set(areas.keys()) == expected_areas
            for area in expected_areas:
                langs = areas[area]
                assert set(langs.keys()) == expected_langs
                for lang in expected_langs:
                    s = langs[lang]
                    assert isinstance(s, str)
                    assert s.strip(), f"empty fragment: planet={planet} house={house} area={area} lang={lang}"

