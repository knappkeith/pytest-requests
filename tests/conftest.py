# These lines will add the parent directory of this file working directory to the
# python path, This helps with Import issues and relative paths.  We could do this
# better though!
import sys
import os
sys.path.append(os.path.split(os.path.dirname(__file__))[0])

import pytest
from src.RequestSession.SimpleRequests import BasicRequestSession


@pytest.fixture(scope="session")
def basic_api():
    return BasicRequestSession()
