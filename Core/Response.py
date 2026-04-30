# Core/Response.py

from Core.Cookies import CookieBuilder

class Response:
    def __init__(self, Body="", Status=200, Headers=None):
        self.Body = Body
        self.Status = Status
        self.Headers = Headers or {}
        # Optional: RawBody for binary responses
        # Set externally: resp.RawBody = b"..."

    def ToBytes(self):
        if hasattr(self, "RawBody") and self.RawBody is not None:
            BodyBytes = self.RawBody
        else:
            BodyBytes = self.Body.encode("utf-8")

        StatusLine = f"HTTP/1.1 {self.Status} {self.GetStatusText()}\r\n"

        header_lines = []

        # Handle multiple Set-Cookie headers
        headers = self.Headers.copy()
        set_cookie = headers.get("Set-Cookie")
        if isinstance(set_cookie, list):
            for c in set_cookie:
                header_lines.append(f"Set-Cookie: {c}\r\n")
            del headers["Set-Cookie"]

        for Key, Value in headers.items():
            header_lines.append(f"{Key}: {Value}\r\n")

        HeaderLines = "".join(header_lines)

        return (StatusLine + HeaderLines + "\r\n").encode("utf-8") + BodyBytes

    def SetCookie(self, name, value, **options):
        cookie_str = CookieBuilder.Build(name, value, **options)

        if "Set-Cookie" in self.Headers:
            existing = self.Headers["Set-Cookie"]
            if isinstance(existing, list):
                existing.append(cookie_str)
            else:
                self.Headers["Set-Cookie"] = [existing, cookie_str]
        else:
            self.Headers["Set-Cookie"] = cookie_str

    def DeleteCookie(self, name, Path="/"):
        self.SetCookie(name, "", Path=Path, MaxAge=0)

    def GetStatusText(self):
        StatusTexts = {
            200: "OK",
            201: "Created",
            204: "No Content",
            301: "Moved Permanently",
            302: "Found",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error"
        }
        return StatusTexts.get(self.Status, "Unknown")

