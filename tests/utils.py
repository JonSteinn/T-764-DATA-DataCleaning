from pathlib import Path

import pytest

skip_if_missing_data = pytest.mark.skipif(
    not (
        Path(__file__)
        .parent.parent.joinpath("data_cleaning", "resources", "blak-domarar.csv")
        .exists()
    ),
    reason="Data files missing",
)
