from data_cleaning.database import Database, construct_database

from .utils import skip_if_missing_data


@skip_if_missing_data
def test_database_creation():
    db: Database = construct_database()
    assert [col for col in db.domarar.columns] == [
        "MotID",
        "EinstID",
        "Timastimpill",
        "Upphafsstafir",
    ]
    assert [col for col in db.einstaklingar.columns] == [
        "EinstID",
        "Nafn",
        "Fdagur",
        "Kyn",
        "FelagISI",
        "Netfang",
        "Heimilisfang1",
        "Heimilisfang2",
        "Heimilisfang3",
        "Simi1",
        "Simi2",
        "Simi3",
        "Timastimpill",
        "Haed",
    ]
    assert [col for col in db.forsvarsmenn.columns] == [
        "MotID",
        "LidID",
        "EinstID",
        "Timastimpill",
    ]
    assert [col for col in db.lid.columns] == [
        "LidID",
        "Nafn",
        "Radnumer",
        "LidaTegundID",
        "SyndarLid",
        "Timastimpill",
        "SyndarlidID",
    ]
    assert [col for col in db.lidimoti.columns] == [
        "MotID",
        "LidID",
        "Oskadeild",
        "Styrkur",
        "Gestalid",
        "Timastimpill",
        "LidaTegundID",
    ]
    assert [col for col in db.lidsmenn.columns] == [
        "MotID",
        "LidID",
        "EinstID",
        "Timastimpill",
    ]
    assert [col for col in db.lidsstjorar.columns] == [
        "MotID",
        "LidID",
        "EinstID",
        "Timastimpill",
    ]
    assert [col for col in db.mot.columns] == [
        "MotID",
        "Heiti",
        "Stadur",
        "Upphafsdagur",
        "Lokadagur",
        "LidID",
        "EinstID",
        "Lysing",
        "Timastimpill",
        "ByrjaTimi",
        "EndaTimi",
        "MinuturALeik",
        "Stigaregla",
        "Stada",
        "MaxHrinur",
        "TwitterTag",
    ]
    assert [col for col in db.thjalfarar.columns] == [
        "MotID",
        "LidID",
        "EinstID",
        "Timastimpill",
    ]

    assert db.domarar.shape == (840, 4)
    assert db.einstaklingar.shape == (4497, 14)
    assert db.forsvarsmenn.shape == (7037, 4)
    assert db.lid.shape == (1242, 7)
    assert db.lidimoti.shape == (1000, 7)
    assert db.lidsmenn.shape == (25852, 4)
    assert db.lidsstjorar.shape == (1772, 4)
    assert db.mot.shape == (242, 16)
    assert db.thjalfarar.shape == (3495, 4)
