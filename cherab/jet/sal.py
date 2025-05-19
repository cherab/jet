import os

from sal.client import SALClient


sal_server = os.environ.get('JET_SAL_SERVER', 'https://sal.jetdata.eu')
sal = SALClient(host=sal_server)
