from src.RequestSession.TestRequests import TestingRequestSession


class BasicRequestSession(TestingRequestSession):
    def __init__(self, verify_SSL=True):
        super().__init__()

        # Set whether to verify the SSL cert
        self.verify = verify_SSL

        # Set base_url
        self.base_url = "https://reqres.in/api"

    def _build_url(self, url_path):
        '''Return the Full URL to be used based on the specific
        use case of this object
        '''

        return "/".join([self.base_url, url_path])
