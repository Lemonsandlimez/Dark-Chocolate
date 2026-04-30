# Core/Request.py

class Request:
    def __init__(self, Method="", Path="", Headers=None, Body=b"", Address=None):
        self.Method = Method
        self.Path = Path
        self.HttpVersion = "HTTP/1.1"
        self.Headers = Headers or {}
        self.Cookies = {}
        self.Body = Body
        self.POST = {}
        self.Query = {}
        self.Params = {}
        self.Address = Address

