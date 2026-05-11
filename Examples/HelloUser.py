# imports

from Core.Router import Router
from Core.Server import Run, Server
from Core.Response import Response

router = Router() # start router

@router.AddRoute("/hello/:name")
def Hello(req, name):
    return Response(f"<h1>Hello, {name}!</h1>", Headers={"Content-Type": "text/html"}) # html 

# run

server = Server(router, Port=8080)
Run(server)

# Use with http://127.0.0.1:8080/hello/john when running
