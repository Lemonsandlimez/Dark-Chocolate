# Core/Post.py

# Dark Chocolate POST Body Parser

import urllib.parse
import json

class PostParser:

    @staticmethod
    def Parse(body_bytes, content_type):
        """
        Parse POST body based on Content-Type.
        Returns a dict.
        """

        if not body_bytes:
            return {}

        try:
            text = body_bytes.decode("utf-8", errors="replace")
        except:
            return {}

        if not content_type:
            return {"raw": text}

        content_type = content_type.split(";", 1)[0].strip().lower()

        # JSON
        if content_type == "application/json":
            try:
                return json.loads(text)
            except:
                return {}

        # Form URL Encoded
        if content_type == "application/x-www-form-urlencoded":
            return dict(urllib.parse.parse_qsl(text))

        # Unknown type -> raw text
        return {"raw": text}

