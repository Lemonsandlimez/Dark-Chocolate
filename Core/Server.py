# Core/Server.py

import asyncio
import socket
import urllib.parse
from Core.Request import Request
from Core.Post import PostParser
from Core.Cookies import CookieParser


# async server

class Server:
    def __init__(self, Router, Host="127.0.0.1", Port=8080):
        self.Router = Router
        self.Host = Host
        self.Port = Port

    async def HandleClient(self, reader, writer):
        try:
            header_data = await reader.readuntil(b"\r\n\r\n")
        except asyncio.IncompleteReadError:
            writer.close()
            return

        header_text = header_data.decode("utf-8", errors="replace")
        lines = header_text.split("\r\n")

        RequestLine = lines[0]
        Method, RawPath, _ = RequestLine.split(" ", 3)

        if "?" in RawPath:
            Path, QueryString = RawPath.split("?", 1)
        else:
            Path, QueryString = RawPath, ""

        Headers = {}
        for line in lines[1:]:
            if ": " in line:
                k, v = line.split(": ", 1)
                Headers[k] = v

        content_length = int(Headers.get("Content-Length", 0))

        body = b""
        if content_length > 0:
            try:
                body = await reader.readexactly(content_length)
            except asyncio.IncompleteReadError:
                body = b""

        Req = Request(
            Method,
            Path,
            Headers,
            body,
            writer.get_extra_info("peername")
        )

        Req.Query = dict(urllib.parse.parse_qsl(QueryString))
        Req.Cookies = CookieParser.Parse(Headers.get("Cookie", ""))
        Req.POST = PostParser.Parse(body, Headers.get("Content-Type", ""))

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

# normal server

class SyncServer:
    def __init__(self, Router, Host="127.0.0.1", Port=8080):
        self.Router = Router
        self.Host = Host
        self.Port = Port

    def Start(self):
        print(f"Dark Chocolate Sync Server running at http://{self.Host}:{self.Port}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.Host, self.Port))
            s.listen(5)

            while True:
                conn, addr = s.accept()
                self.HandleClient(conn, addr)

    def HandleClient(self, conn, addr):
        try:
            data = conn.recv(65535)
            if not data:
                conn.close()
                return

            text = data.decode("utf-8", errors="replace")
            headers, body = text.split("\r\n\r\n", 1)

            lines = headers.split("\r\n")
            method, raw_path, _ = lines[0].split(" ", 2)

            if "?" in raw_path:
                path, query_string = raw_path.split("?", 1)
            else:
                path, query_string = raw_path, ""

            hdrs = {}
            for line in lines[1:]:
                if ": " in line:
                    k, v = line.split(": ", 1)
                    hdrs[k] = v

            req = Request(
                Method=method,
                Path=path,
                Headers=hdrs,
                Body=body.encode("utf-8"),
                Address=addr
            )

            req.Query = dict(urllib.parse.parse_qsl(query_string))
            req.Cookies = CookieParser.Parse(hdrs.get("Cookie", ""))
            req.POST = PostParser.Parse(req.Body, hdrs.get("Content-Type", ""))

            resp = self.Router.Handle(req)

            if resp is None:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            else:
                conn.sendall(resp.ToBytes())

        except Exception:
            conn.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

        finally:
            conn.close()



# pub API

def Run(server):
    # Run the server normaly.
    SyncServer(server.Router, server.Host, server.Port).Start()


def AsyncRun(server):
    # Run the server with async.
    asyncio.run(server.Start())
