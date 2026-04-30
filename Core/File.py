# Core/File.py
import os
import mimetypes
from Core.Response import Response

def SendFile(Path, DownloadName=None):
    if not os.path.exists(Path) or not os.path.isfile(Path):
        return Response("File not found", 404)

    with open(Path, "rb") as f:
        data = f.read()

    content_type, _ = mimetypes.guess_type(Path)
    if content_type is None:
        content_type = "application/octet-stream"

    if DownloadName is None:
        DownloadName = os.path.basename(Path)

    headers = {
        "Content-Type": content_type,
        "Content-Length": str(len(data)),
        "Content-Disposition": f'attachment; filename="{DownloadName}"'
    }

    resp = Response(Status=200, Headers=headers)
    resp.RawBody = data
    resp.Body = ""
    return resp

