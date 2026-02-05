import os

from sal.client import SALClient


SAL_SERVER = os.environ.get('JET_SAL_SERVER', 'https://sal.jetdata.eu')


class JETSALClient(SALClient):
    """SALClient with host `sal.jetdata.eu` by default, or env variable `JET_SAL_SERVER`."""
    def __init__(self, host: str = SAL_SERVER, **kwargs):
        super().__init__(host=host, **kwargs)


def get_jet_sal(host: str = SAL_SERVER, **kwargs) -> SALClient:
    """Creates a SALClient instance connected to `host` if provided.
    By default uses env variable `JET_SAL_SERVER` if set, `https://sal.jetdata.eu` otherwise.
    """
    return SALClient(host=host, **kwargs)


def __getattr__(name: str):
    if name == "sal":
        value = get_jet_sal()
        globals()[name] = value  # cache on the module
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
