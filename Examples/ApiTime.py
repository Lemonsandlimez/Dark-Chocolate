from Core.Router import Router
from Core.Server import Run, Server
from Core.Json import Json
import time

router = Router()

@router.AddRoute("/api/time")
def Time(req):
    return Json({"server_time": time.ctime()})

server = Server(router, Port=8080)
Run(server)
