import datetime

from .cleaner import Cleaner
from .database import Database, construct_database
from .results import process_results


def main() -> None:
    """Starting point."""
    db: Database = construct_database()
    comparator = {
        _id: datetime.datetime.strptime(_time, "%Y-%m-%d %H:%M:%S.%f")
        for _id, (_id, _time) in db.einstaklingar[
            ["EinstID", "Timastimpill"]
        ].iterrows()
    }
    db.einstaklingar.set_index("EinstID", inplace=True)
    cleaner = Cleaner(db, comparator)
    process_results(cleaner.get_duplicates(), db.einstaklingar)


if __name__ == "__main__":
    main()
