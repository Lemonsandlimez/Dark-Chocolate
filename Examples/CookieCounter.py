from Core.Router import Router
from Core.Server import Server, Run
from Core.Response import Response

router = Router()

@router.AddRoute("/")
def Counter(req):
    # Get current count from cookie
    count = int(req.Cookies.get("count", 0))

    # Increment
    count += 1

    # Build response
    resp = Response(f"You have visited this page {count} times.")

    # Update cookie
    resp.SetCookie("count", str(count), Path="/")

    return resp


server = Server(router, Host="127.0.0.1", Port=8080)

if __name__ == "__main__":
    Run(server)

# refresh the page 
