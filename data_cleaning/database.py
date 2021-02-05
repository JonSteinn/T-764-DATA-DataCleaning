from pathlib import Path
from typing import NamedTuple

import pandas as pd

_CSV_ROOT_PATH: Path = Path(__file__).parent.joinpath("resources")


class Database(NamedTuple):
    """A object containing all csv files."""

    # pylint: disable=inherit-non-class

    domarar: pd.DataFrame
    einstaklingar: pd.DataFrame
    forsvarsmenn: pd.DataFrame
    lid: pd.DataFrame
    lidimoti: pd.DataFrame
    lidsmenn: pd.DataFrame
    lidsstjorar: pd.DataFrame
    mot: pd.DataFrame
    thjalfarar: pd.DataFrame


def read_csv_file(csv_file: str) -> pd.DataFrame:
    """Read a csv file."""
    return pd.read_csv(_CSV_ROOT_PATH.joinpath(csv_file), encoding="utf-8-sig", sep=";")


def construct_database() -> Database:
    """Read all csv file into a `Database` object."""
    return Database(
        *map(
            read_csv_file,
            sorted(
                glob.name
                for glob in _CSV_ROOT_PATH.glob("**/*")
                if glob.is_file() and glob.name.endswith(".csv")
            ),
        )
    )
