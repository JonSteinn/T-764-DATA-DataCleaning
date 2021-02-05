from data_cleaning.database import Database, construct_database


def test_placeholder():
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
