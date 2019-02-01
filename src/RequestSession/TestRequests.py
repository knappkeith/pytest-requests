import requests
from src.tools.stopwatch import Timer


class TestingRequestSession(requests.Session):
    '''Base Extension Class of the request Session object
    '''
    def __init__(self):
        super().__init__()

        # Start the History
        self.history = HistoryStack(max_length=100)

        # Verbosity for Printing
        self.verbosity = 0

        # `mount` a custom adapter that retries failed connections for HTTP
        # and HTTPS requests.
        self.mount("http://", requests.adapters.HTTPAdapter(max_retries=1))
        self.mount("https://", requests.adapters.HTTPAdapter(max_retries=1))

    def _send_request(self, method, url_path, *args, **kwargs):
        '''Forwards on the requet to the Session.request method after
        expanding the url_path to include the base_url.  upon receipt of the
        response it is added to the history, monkeypatching the response object
        and adding timing information.
        '''
        # Build the correct URL
        url = self._build_url(url_path)

        # Start the Timer
        request_timer = Timer()

        # Send request to super
        response = TestingResponse(super().request(method=method.upper(),
                                                   url=url, *args, **kwargs))

        # Add duration to repose object
        request_timer.stop()
        response.duration = request_timer.elapsed

        # Add to history
        self.history.append(response)

        # return
        return response

    def get(self, url_path, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self._send_request('GET', url_path, **kwargs)

    def options(self, url_path, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self._send_request('OPTIONS', url_path, **kwargs)

    def head(self, url_path, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        return self._send_request('HEAD', url_path, **kwargs)

    def post(self, url_path, data=None, json=None, **kwargs):
        return self._send_request('POST', url_path, data=data, json=json, **kwargs)

    def put(self, url_path, data=None, **kwargs):
        return self._send_request('PUT', url_path, data=data, **kwargs)

    def patch(self, url_path, data=None, **kwargs):
        return self._send_request('PATCH', url_path, data=data, **kwargs)

    def delete(self, url_path, **kwargs):
        return self._send_request('DELETE', url_path, **kwargs)

    # Add the __str__ method to print out the history array

    # Add method to handle the reauthentication if expires, will need
    #  to add to _send_request as well.


class TestingResponse(requests.Response):
    """Base Tesing Response Object, Monkey Patches the requests.Sessions.response Object.
    """
    def __init__(self, req):
        super().__init__()
        for k, v in req.__dict__.items():
            self.__dict__[k] = v

    def __str__(self):
        if self.ok:
            err_message = ""
        else:
            err_message = " [ERROR: {}]"
            try:
                err_message = err_message.format(
                    self.json())
            except Exception:
                err_message = err_message.format(
                    self.text[0:500])
        return "[{duration}s]{method:>7}: {url} --> {stat}{err}".format(
            duration=round(self.duration, 3),
            method=self.request.method,
            url=self.request.url,
            stat=self.status_code,
            err=err_message)

    # Add the generate_cURL method to print the curl version

    # Add the printout method to print out the nice version


class HistoryStack(list):
    '''Simple list object that has a set length, overrode all "adding"
    native methods.
    '''
    def __init__(self, max_length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_length = max_length
        self._trim_to_max()

    def append(self, item):
        super().append(item)
        self._trim_to_max()

    def extend(self, item):
        super().extend(item)
        self._trim_to_max()

    def insert(self, item, pos):
        super().insert(item, pos)
        self._trim_to_max()

    def _trim_to_max(self):
        '''method to pop off extras
        '''
        while len(self) > self._max_length:
            self.pop(0)

    def __str__(self):
        return "\n".join([str(x) for x in self])
