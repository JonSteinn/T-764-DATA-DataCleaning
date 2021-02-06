from typing import Optional

import textdistance


class StringUtils:
    """Contains string util functions."""

    ICE_MAP = str.maketrans("".join("áéíóúðýö"), "".join("aeioudyo"))
    NICK_NAME_MAP = {
        "sigridur": "sigga",
        "sigrun": "sigga",
        "gudmundur": "gummi",
        "gunnar": "gunni",
        "sigurdur": "siggi",
    }

    @staticmethod
    def unicelandicify(string: str) -> str:
        """Returns a copy of `string` replacing some common icelandic letters
        that are sometimes written with english counterparts. The icelandic letters
        that we do not map are `æ` and `þ` as they are usually represented with
        two letters (`ae` and `th`) when written with the english alphabet.
        """
        return string.translate(StringUtils.ICE_MAP)

    @staticmethod
    def common_nick_for(name: str) -> Optional[str]:
        """Maps a icelandic name (with no icelandic chars and in lower case)
        to a common nickname assoicated with the name. If the name
        """
        return StringUtils.NICK_NAME_MAP.get(name)

    @staticmethod
    def initials(name: str) -> str:
        """Return a name as a string of initials.
        'Jón Steinn Elíasson' would map to 'JSE'.
        """
        return "".join(map(lambda w: w[0], name.split()))

    @staticmethod
    def levenshtein(string1: str, string2: str) -> int:
        """The minimum number of single-character edits (insertions, deletions
        or substitutions) required to change one word into the other.

        https://en.wikipedia.org/wiki/Levenshtein_distance
        """
        dist: int = textdistance.levenshtein(string1, string2)
        return dist

    @staticmethod
    def remove_son_dottir(name: str) -> str:
        """Remove son/dottir from icelandic names."""
        if name.endswith("dottir"):
            return name[:-6]
        if name.endswith("son"):
            return name[:-3]
        return name
