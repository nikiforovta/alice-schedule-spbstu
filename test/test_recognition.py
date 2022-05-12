import pytest

from src.recognition import group_recognition


@pytest.mark.parametrize("answer, possible_group", [
    (["3530901", "80203"], "3530901/80203"),
    (["з", "3", "5", "3", "0", "9", "0", "1", "дробь", "8", "0", "2", "0", "3"], "з3530901/80203"),
    (["353", "0901", "слеш", "80203"], "3530901/80203"),
    (["353", "0901", "косая", "черта", "80", "203"], "3530901/80203"),
    (["353", "0902", ",", "81565"], "3530902/81565"),
    (["353", "09", "01", "8", "0", "2", "0", "3"], "3530901/80203"),
    (['ooooo'], None),
    (['ooooooooooooo'], "oooooooo/ooooo")])
def test_group_recognition(answer, possible_group):
    assert group_recognition(answer) == possible_group
