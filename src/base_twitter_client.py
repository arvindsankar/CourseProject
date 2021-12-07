class BaseTwitterClient:
    def __init__(self, api_key, api_secret_key, bearer_token):
        self._API_KEY_ = api_key
        self._API_SECRET_KEY_ = api_secret_key
        self._BEARER_TOKEN_ = bearer_token
        self.api = None
