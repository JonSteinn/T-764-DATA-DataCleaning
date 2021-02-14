import datetime
from itertools import combinations
from typing import Dict, Iterator, List

import pandas as pd
import tqdm

from .database import Database
from .graph import Graph
from .str_utils import StringUtils as su


class Cleaner:
    """Data cleaning. No actual changes are made. They are only recorded."""

    # pylint: disable=too-few-public-methods

    def __init__(self, db: Database, comparator: Dict[int, datetime.datetime]):
        self.db: Database = db
        self.duplicate_tracker: Dict[str, Graph] = {}
        self.cmp = comparator

    def _process(self):
        by_first_letter: pd.core.groupby.generic.DataFrameGroupBy = (
            self.db.einstaklingar.groupby(
                su.unicelandicify(self.db.einstaklingar["Nafn"].str[0].str.lower().str),
            )
        )
        for grp in tqdm.tqdm(by_first_letter.groups):
            self.duplicate_tracker[grp] = Graph()
            grp_df = by_first_letter.get_group(grp)
            Cleaner._find_duplicates(grp_df, self.duplicate_tracker[grp])

    @staticmethod
    def _find_duplicates(individuals: pd.DataFrame, graph: Graph):
        for id1, id2 in combinations(individuals.index, 2):
            if Cleaner._are_duplicates(individuals.loc[id1], individuals.loc[id2]):
                graph.add_edge(id1, id2)

    @staticmethod
    def _are_duplicates(
        person1: pd.core.series.Series, person2: pd.core.series.Series
    ) -> bool:
        name1 = su.remove_son_dottir(su.unicelandicify(person1["Nafn"].lower()))
        name2 = su.remove_son_dottir(su.unicelandicify(person2["Nafn"].lower()))
        threshold = 0.95
        shared = False
        if Cleaner._share_birthday(person1, person2):
            threshold -= 0.1
            shared = True
        if Cleaner._share_email(person1, person2):
            threshold -= 0.15
            shared = True
        if Cleaner._share_phone(person1, person2):
            threshold -= 0.15
            shared = True
        if shared:
            if Cleaner._nickname_match(name1, name2):
                threshold -= 0.25
            if Cleaner._initials_match(name1, name2):
                threshold -= 0.25
        elif not Cleaner._share_team(person1, person2):
            return False
        return (
            1 - su.levenshtein(name1, name2) / max(len(name1), len(name2)) > threshold
        )

    @staticmethod
    def _share_birthday(
        person1: pd.core.series.Series, person2: pd.core.series.Series
    ) -> bool:
        bday1 = datetime.datetime.strptime(person1["Fdagur"], "%Y-%m-%d %H:%M:%S.%f")
        bday2 = datetime.datetime.strptime(person2["Fdagur"], "%Y-%m-%d %H:%M:%S.%f")
        return (
            bday1.year == bday2.year
            and bday1.month == bday2.month
            and bday1.day == bday2.day
        )

    @staticmethod
    def _share_email(
        person1: pd.core.series.Series, person2: pd.core.series.Series
    ) -> bool:
        email1 = person1["Netfang"]
        email2 = person2["Netfang"]
        return isinstance(email1, str) and isinstance(email2, str) and email1 == email2

    @staticmethod
    def _share_phone(
        person1: pd.core.series.Series, person2: pd.core.series.Series
    ) -> bool:
        def _get_all_phone_numbers(*args) -> Iterator[str]:
            for number in args:
                if isinstance(number, str):
                    just_digits = "".join(c for c in number if c.isdigit())
                    if len(just_digits) > 6:
                        yield just_digits[-7:]

        return not set(
            _get_all_phone_numbers(person1["Simi1"], person1["Simi2"], person1["Simi3"])
        ).isdisjoint(
            set(
                _get_all_phone_numbers(
                    person2["Simi1"], person2["Simi2"], person2["Simi3"]
                )
            )
        )

    @staticmethod
    def _share_team(
        person1: pd.core.series.Series, person2: pd.core.series.Series
    ) -> bool:
        team1 = person1["FelagISI"]
        team2 = person2["FelagISI"]
        if not (isinstance(team1, str) and isinstance(team2, str)):
            return False
        team1 = su.unicelandicify(team1.lower())
        team2 = su.unicelandicify(team2.lower())
        team1_i = su.initials(team1)
        team2_i = su.initials(team2)
        if (
            team1 == team2
            or team1.replace(" ", "") == team1_i
            or team2.replace(" ", "") == team1_i
            or team1_i == team2_i
        ):
            return True
        return 1 - su.levenshtein(team1, team2) / max(len(team1), len(team2)) > 0.9

    @staticmethod
    def _initials_match(name1: str, name2: str) -> bool:
        return (
            su.initials(name1) == su.initials(name2)
            or su.initials(name1) == name2.replace(" ", "")
            or su.initials(name2) == name1.replace(" ", "")
        )

    @staticmethod
    def _nickname_match(name1: str, name2: str) -> bool:
        nick1 = su.common_nick_for(name1)
        nick2 = su.common_nick_for(name2)
        if nick1 is None and nick2 is None:
            return False
        if nick1 is None:
            return name1.split()[0] == nick2
        if nick2 is None:
            return name2.split()[0] == nick1
        return False

    def get_duplicates(self) -> Iterator[List[int]]:
        """Get graphs connecting duplicates."""
        self.duplicate_tracker.clear()
        self._process()
        yield from (
            sorted(grp, key=lambda k: self.cmp[k])
            for graph in self.duplicate_tracker.values()
            for grp in graph.find_grps()
        )
