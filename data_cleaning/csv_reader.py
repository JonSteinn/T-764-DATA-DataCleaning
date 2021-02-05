import csv
from pathlib import Path
from typing import Iterator, List, Tuple


class CSVReader:
    """A class that handles reading the data files."""

    _CSV_ROOT_PATH: Path = Path(__file__).parent.joinpath("resources", "csv")
    _FILES: List[str] = [x.name for x in _CSV_ROOT_PATH.glob("**/*") if x.is_file()]

    @staticmethod
    def read_csv_file(
        csv_file: str, delimiter: str = ";", quotechar: str = "|"
    ) -> Iterator[List[str]]:
        """Read a csv file."""
        with open(
            CSVReader._CSV_ROOT_PATH.joinpath(csv_file), encoding="utf-8-sig"
        ) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            yield from spamreader

    @staticmethod
    def _seperate(iterator: Iterator[List[str]]) -> Tuple[List[str], List[List[str]]]:
        return next(iterator), list(iterator)

    @staticmethod
    def get_all(
        delimiter: str = ";", quotechar: str = "|"
    ) -> Iterator[Tuple[str, List[str], List[List[str]]]]:
        """Get all data files."""
        return (
            (
                filename,
                *CSVReader._seperate(
                    CSVReader.read_csv_file(filename, delimiter, quotechar)
                ),
            )
            for filename in CSVReader._FILES
        )
