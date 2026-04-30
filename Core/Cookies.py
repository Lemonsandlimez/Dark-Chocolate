# Core/Cookies.py
class CookieParser:
    @staticmethod
    def Parse(raw_cookie_header):
        """
        Convert: "key=value; theme=dark; session=abc"
        Into:    {"key": "value", "theme": "dark", "session": "abc"}
        """
        cookies = {}

        if not raw_cookie_header:
            return cookies

        parts = raw_cookie_header.split(";")
        for part in parts:
            if "=" in part:
                key, value = part.strip().split("=", 1)
                cookies[key] = value

        return cookies


class CookieBuilder:
    @staticmethod
    def Build(name, value, **options):
        """
        Build a Set-Cookie header string.
        Example:
            CookieBuilder.Build("theme", "dark", Path="/", HttpOnly=True)
        """
        parts = [f"{name}={value}"]

        for k, v in options.items():
            if v is True:
                parts.append(k)
            else:
                parts.append(f"{k}={v}")

        return "; ".join(parts)

