from collections import deque
from typing import Deque, Iterable, List, Set

import pandas as pd


def _to_tikz(dups: Set[int], individuals: pd.DataFrame):
    with open("latex.txt", "w") as f:
        f.write("\\begin{tikzpicture}[yscale=0.1, xscale=0.07]\n")
        f.write("\\draw (0,0) rectangle (50, 4498/85);\n")
        for i, _id in enumerate(individuals.index):
            if _id in dups:
                f.write(
                    f"\\draw[line width=0.00666666667] (0,{i}/85) -- (50,{i}/85);\n"
                )
        f.write("\\end{tikzpicture}")


def _dup_yielder(lis: Deque[Deque[int]]):
    while lis:
        grp = lis.popleft()
        grp.popleft()  # Dump first
        yield from grp


def _plot(lis: Deque[Deque[int]], individuals: pd.DataFrame):
    dups = set(_dup_yielder(lis))
    perc = (len(dups) / individuals.shape[0]) * 100
    print(f"Total duplicates found: {len(dups)} ({perc:.2f}%)")
    _to_tikz(dups, individuals)


def _write_to_csv(
    duplicated: Iterable[List[int]], individuals: pd.DataFrame
) -> Deque[Deque[int]]:
    lis: Deque[Deque[int]] = deque([])
    for i, duplicates in enumerate(duplicated):
        if i == 0:
            individuals.loc[duplicates].to_csv(
                "duplicates.csv", encoding="utf-8-sig", sep=";"
            )
        else:
            with open("duplicates.csv", "a", encoding="utf-8-sig") as f:
                f.write(f"{';' * 13}\n")
            individuals.loc[duplicates].to_csv(
                "duplicates.csv", mode="a", header=False, encoding="utf-8-sig", sep=";"
            )
        lis.append(deque(duplicates))
    return lis


def process_results(duplicated: Iterable[List[int]], individuals: pd.DataFrame):
    """Process the results. This will write the groups to a .csv and visualize."""
    _plot(_write_to_csv(duplicated, individuals), individuals)
