# Core/Server.py

import asyncio
import urllib.parse

from Core.Request import Request
from Core.Post import PostParser
from Core.Cookies import CookieParser


class Server:
    def __init__(self, Router, Host="127.0.0.1", Port=8080):
        self.Router = Router
        self.Host = Host
        self.Port = Port

    async def HandleClient(self, reader, writer):
        # Read headers (until \r\n\r\n)
        try:
            header_data = await reader.readuntil(b"\r\n\r\n")
        except asyncio.IncompleteReadError:
            writer.close()
            return

        header_text = header_data.decode("utf-8", errors="replace")
        lines = header_text.split("\r\n")

        # Request line
        RequestLine = lines[0]
        Method, RawPath, _ = RequestLine.split(" ", 3)

        # Path + Query
        if "?" in RawPath:
            Path, QueryString = RawPath.split("?", 1)
        else:
            Path, QueryString = RawPath, ""

        # Parse headers
        Headers = {}
        for line in lines[1:]:
            if ": " in line:
                k, v = line.split(": ", 1)
                Headers[k] = v

        content_length = int(Headers.get("Content-Length", 0))

        # Read body if present
        body = b""
        if content_length > 0:
            try:
                body = await reader.readexactly(content_length)
            except asyncio.IncompleteReadError:
                body = b""

        # Build Request object
        Req = Request(
            Method,
            Path,
            Headers,
            body,
            writer.get_extra_info("peername")
        )

        # Query parsing
        Req.Query = dict(urllib.parse.parse_qsl(QueryString))

        # Cookie parsing
        raw_cookie = Headers.get("Cookie", "")
        Req.Cookies = CookieParser.Parse(raw_cookie)

        # POST parsing
        content_type = Headers.get("Content-Type", "")
        Req.POST = PostParser.Parse(body, content_type)

        # Route handling
        ResponseObject = self.Router.Handle(Req)

        if ResponseObject is None:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
        else:
            writer.write(ResponseObject.ToBytes())

        await writer.drain()
        writer.close()

    async def Start(self):
        server = await asyncio.start_server(
            self.HandleClient,
            self.Host,
            self.Port
        )

        print(f"Dark Chocolate Async Server running at http://{self.Host}:{self.Port}")

        async with server:
            await server.serve_forever()

