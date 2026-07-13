# Jeffar - test_scanner.py
# Description - port_scanner pytest
# Created - 2026-07-13
# Last updated - 2026-07-13

# Modules
import pytest
from port_scanner.services import get_service

@pytest.mark.parametrize("port, expected_service", [
    (80, 'HTTP'),
    (443, 'HTTPS'),
    (22, 'SSH'),
    (99999, 'unknown'),     # not in the dict
])
def test_get_service(port, expected_service):
    """
    test_get_service - True if port number returns the matching service name
    """
    assert get_service(port) == expected_service