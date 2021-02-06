from .cleaner import Cleaner
from .database import Database, construct_database


def main() -> None:
    """Starting point."""
    db: Database = construct_database()
    cleaner = Cleaner(db)
    db.einstaklingar.set_index("EinstID", inplace=True)
    for i, duplicates in enumerate(cleaner.get_duplicates()):
        if i == 0:
            db.einstaklingar.loc[duplicates].to_csv(
                "duplicates.csv", encoding="utf-8-sig", sep=";"
            )
        else:
            with open("duplicates.csv", "a", encoding="utf-8-sig") as f:
                f.write(f"{';' * 13}\n")
            db.einstaklingar.loc[duplicates].to_csv(
                "duplicates.csv", mode="a", header=False, encoding="utf-8-sig", sep=";"
            )


if __name__ == "__main__":
    main()
