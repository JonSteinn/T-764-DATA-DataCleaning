from data_cleaning.str_utils import StringUtils as su


def test_unicelandicify():
    name_lower = "Ýmir Ólafur Þórhallsson".lower()
    assert su.unicelandicify(name_lower) == "ymir olafur þorhallsson"


def test_nicknames():
    name_lower_unice = su.unicelandicify("Sigríður".lower())
    assert su.common_nick_for(name_lower_unice) == "sigga"


def test_initials():
    name = "Jón Steinn Elíasson"
    assert su.initials(name) == "JSE"


def test_remove_son_daughter():
    assert su.remove_son_dottir("abcson") == "abc"
    assert su.remove_son_dottir("cdedottir") == "cde"
