from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

token_url='https://auth.weather.mg/oauth/token'

def getMeteoSession(logindatapath):
    """ Athenticate with logindata at Meteo API.
    Return Session.
    """
    with open(logindatapath, "r") as f:
        login = f.read().split()
        client_id = login[0]
        client_secret = login[1]
        f.close()

    client = BackendApplicationClient(client_id=client_id)
    client.prepare_request_body(scope=[])

    # fetch an access token
    session = OAuth2Session(client=client)
    session.fetch_token(token_url=token_url,
                        client_id=client_id,
                        client_secret=client_secret)
    return session
