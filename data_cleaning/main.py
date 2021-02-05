from .database import Database, construct_database


def main() -> None:
    """Starting point."""
    db: Database = construct_database()
    print(db.domarar.iloc[0])


if __name__ == "__main__":
    main()
