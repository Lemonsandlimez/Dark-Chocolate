from Core.Router import Router
from Core.Server import Run, Server
from Core.Response import Response

router = Router()

@router.AddRoute("/hello/:name")
def Hello(req, name):
    return Response(f"<h1>Hello, {name}!</h1>", Headers={"Content-Type": "text/html"})

server = Server(router, Port=8080)
Run(server)
