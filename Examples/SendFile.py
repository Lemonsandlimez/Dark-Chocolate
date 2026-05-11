from Core.Router import Router
from Core.Server import Run, Server
from Core.File import SendFile

router = Router()

@router.AddRoute("/GetText")
def text(req):
    return SendFile("text.txt")

server = Server(router, Port=8080)
Run(server)

#  run, go to http://127.0.0.1:8080/GetText . but make sure you have a file called text.txt!
