from src.RequestSession.TestRequests import TestingRequestSession


class BasicRequestSession(TestingRequestSession):
    """
    This is a basic example of a Request Session.
    Each different "connector" you would need would have
    a different class.  You must have the `_build_url` method.
    """
    def __init__(self, verify_SSL=True):
        """This initailization method needs to initialize at least
        the `base_url`.  You can also set anything on the `requests.Session`
        that will be needed for this Object as well such as:
        * `headers`
        * `verify` - If the SSL Cert if verified
        * `cookies`
        """
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
