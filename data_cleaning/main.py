from .cleaner import Cleaner
from .database import Database, construct_database
from .results import process_results


def main() -> None:
    """Starting point."""
    db: Database = construct_database()
    cleaner = Cleaner(db)
    db.einstaklingar.set_index("EinstID", inplace=True)
    process_results(cleaner.get_duplicates(), db.einstaklingar)


if __name__ == "__main__":
    main()
