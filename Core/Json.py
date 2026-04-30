# Core/Json.py
import json
from Core.Response import Response

def Json(Data, Status=200):
    return Response(
        Body=json.dumps(Data),
        Status=Status,
        Headers={"Content-Type": "application/json"}
    )

