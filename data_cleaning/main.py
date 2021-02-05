from .database import Database, construct_database


def main() -> None:
    """Starting point."""
    db: Database = construct_database()
    print(db.einstaklingar.head)


if __name__ == "__main__":
    main()
