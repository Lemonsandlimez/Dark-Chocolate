from Core.Router import Router
from Core.Server import Run, Server
from Core.Response import Response

router = Router()

@router.AddRoute("/")
def Form(req):
    return Response("""
        <form method='POST' action='/echo'>
            <input name='text'>
            <button>Send</button>
        </form>
    """, Headers={"Content-Type": "text/html"})

@router.AddRoute("/echo")
def Echo(req):
    text = req.POST.get("text", "")
    return Response(f"You said: {text}")

server = Server(router, Port=8080)
Run(server)

# run, then enter data. 
