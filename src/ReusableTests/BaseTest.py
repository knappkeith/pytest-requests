class BaseTestObject(object):
    def __init__(self):
        self._result = None

    @property
    def result(self):
        if self._result is not None:
            return self._result

        self._result = self.run_tests()
        return self._result

    @property
    def result_str(self):
        return "test results: \n{}".format(
            "\n".join(
                ["{:>5} - {}{}".format(
                    str(x.get('result')), x['desc'], x.get('error', ""))
                 for x in self.steps]))

    def run_tests(self):
        for step in self.steps:
            if step.get("result") is None:
                try:
                    res = step['method']()
                    step['result'] = res
                except Exception as e:
                    step['result'] = False
                    step['error'] = str(e)
                if step['result'] is False:
                    return False
        if len([x for x in self.steps if x['result'] is False]) > 0:
            return False
        return True

    def __nonzero__(self):
        if self._result is not None:
            return self._result
        return self.result

    def __bool__(self):
        return self.__nonzero__()


class RequestTestGet(BaseTestObject):
    def __init__(self, session, resource, model, *args, **kwargs):
        super().__init__()
        self.session = session
        self.resource = resource
        self.model = model
        self.steps = [
            {"method": self.get_call, "desc": "test get call"},
            {"method": self.verify_get_data, "desc": "verify get data type"},
            {"method": self.verify_get_model, "desc": "verify get model"}
        ]
        if 'mapping' in kwargs.keys():
            self.mapping = kwargs['mapping']
        else:
            self.mapping = None

    def get_call(self):
        r = self.session.get(url_path=self.resource)
        self.get_response = r
        if r.ok:
            return True
        else:
            return False

    def verify_get_data(self):
        if self.mapping is not None:
            self.my_data = self.get_response.json()[self.mapping]
        else:
            self.my_data = self.get_response.json()
        if not isinstance(self.my_data, list):
            return False
        return True

    def verify_get_model(self):
        for item in self.my_data:
            if self.model.keys() != item.keys():
                return False
        return True


class RequestTestPost(BaseTestObject):
    def __init__(self, session, resource, payload, model, *args, **kwargs):
        super().__init__()
        self.session = session
        self.resource = resource
        self.model = model
        self.payload = payload
        self.steps = [
            {"method": self.post_call, "desc": "test post call"},
            {"method": self.verify_post_data_type, "desc": "verify post data type"},
            {"method": self.verify_post_model, "desc": "verify post model"},
            {"method": self.verify_post_data, "desc": "verify post model"}
        ]

    def post_call(self):
        r = self.session.post(url_path=self.resource, json=self.payload)
        self.post_response = r
        if r.ok:
            return True
        else:
            return False

    def verify_post_data_type(self):
        self.my_data = self.post_response.json()
        if not isinstance(self.my_data, dict):
            return False
        return True

    def verify_post_model(self):
        if self.model.keys() != self.my_data.keys():
            return False
        return True

    def verify_post_data(self):
        for key, value in self.payload.items():
            if self.my_data[key] != value:
                return False
        return True
