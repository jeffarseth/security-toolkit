# Jeffar - test_password.py
# Description - password_tool pytest
# Created - 2026-07-13
# Last updated - 2026-07-13

# Modules
import pytest
from password_tool.checker import check_length
from password_tool.checker import check_uppercase
from password_tool.checker import check_lowercase
from password_tool.checker import check_digit
from password_tool.checker import check_symbol
from password_tool.checker import check_wordlist
from password_tool.generator import generate_basic

@pytest.mark.parametrize("password, expected", [
    ('abcdefgh', True),         # 8 characters PASS
    ('abc', False),             # 3 characters FAIL
    ('abcdefghijkl', True),     # 12 characters PASS
    ('', False)                 # empty FAIL
])
def test_check_length(password, expected):
    """
    test_check_length - True if above MIN_LENGTH
    """
    assert check_length(password) == expected

@pytest.mark.parametrize("password, expected", [
    ('ABC', True),              # ABC is uppercase PASS
    ('Abc', True),              # A is uppercase PASS
    ('abc', False),             # no uppercase character FAIL
    ('abc123!', False),         # no uppercase character but have other types FAIL
    ('', False)                 # empty FAIL
])
def test_check_uppercase(password, expected):
    """
    test_check_uppercase - True if password str has an UPPERCASE
    """
    assert check_uppercase(password) == expected

@pytest.mark.parametrize("password, expected", [
    ('abc', True),              # abc is lowercase PASS
    ('aBC', True),              # a is lowercase PASS
    ('ABC', False),             # no lowercase character FAIL
    ('ABC123!', False),         # no lowercase character but have other types FAIL
    ('', False)                 # empty FAIL
])
def test_check_lowercase(password, expected):
    """
    test_check_lowercase - True if password str has a lowercase
    """
    assert check_lowercase(password) == expected

@pytest.mark.parametrize("password, expected", [
    ('123', True),              # 123 are digits PASS
    ('1ab', True),              # 1 is a digit PASS
    ('ABC', False),             # no digit character FAIL
    ('ABC123!', True),          # str has digit characters PASS
    ('', False)                 # empty FAIL
])
def test_check_digit(password, expected):
    """
    test_check_digit - True if password str has a digit
    """
    assert check_digit(password) == expected

@pytest.mark.parametrize("password, expected", [
    ('!@#', True),              # !@# are digits PASS
    ('!ab', True),              # ! is a symbol PASS
    ('ABC', False),             # no symbol character FAIL
    ('ABC123!', True),          # str has symbol character PASS
    ('', False)                 # empty FAIL
])
def test_check_symbol(password, expected):
    """
    test_check_symbol - True if password str has a symbol
    """
    assert check_symbol(password) == expected

@pytest.mark.parametrize("password, expected", [
    ('123456', True),               # password is found in wordlist PASS
    ('password', True),             # password is found in wordlist PASS
    ('PASSWORD', True),             # case-insensitivity test PASS
    ('3QF@=aGQ`1e:j3BQ', False)     # strong password FAIL
])
def test_check_wordlist(password, expected):
    """
    test_check_wordlist - True if password str contains a str from wordlist
    """
    wordlist = {'123456', 'password', 'qwerty'}   # mini version of passwords.txt
    assert check_wordlist(password, wordlist) == expected

def test_generate_basic():
    """
    test_generate_basic - True if the generated password is 16 chars and a string
    """
    password = generate_basic()         # generate and store the result
    assert len(password) == 16          # True for correct length
    assert isinstance(password, str)    # True if it's a string