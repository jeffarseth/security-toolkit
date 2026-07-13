# Jeffar - test_hash.py
# Description - hash_tool pytest
# Created - 2026-07-13
# Last updated - 2026-07-13

# Modules
from hash_tool.generator import md5_text
from hash_tool.generator import sha1_text
from hash_tool.generator import sha256_text
from hash_tool.generator import sha512_text
from hash_tool.generator import sha3_256_text
from hash_tool.generator import sha3_512_text

def test_md5_test():
    """
    test_md5_test - True if known md5 hash checks out
    """

    assert md5_text("abc", "").hexdigest() == "900150983cd24fb0d6963f7d28e17f72"

def test_sha1_test():
    """
    test_sha1_test - True if known sha1 hash checks out
    """

    assert sha1_text("abc", "").hexdigest() == "a9993e364706816aba3e25717850c26c9cd0d89d"

def test_sha256_test():
    """
    test_sha256_test - True if known sha256 hash checks out
    """

    assert sha256_text("abc", "").hexdigest() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

def test_sha512_test():
    """
    test_sha512_test - True if known sha512 hash checks out
    """

    assert sha512_text("abc", "").hexdigest() == "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"

def test_sha3_256_test():
    """
    test_sha3_256_test - True if known sha3-256 hash checks out
    """

    assert sha3_256_text("abc", "").hexdigest() == "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"

def test_sha3_512_test():
    """
    test_sha3_512_test - True if known sha3-512 hash checks out
    """

    assert sha3_512_text("abc", "").hexdigest() == "b751850b1a57168a5693cd924b6b096e08f621827444f70d884f5d0240d2712e10e116e9192af3c91a7ec57647e3934057340b4cf408d5a56592f8274eec53f0"