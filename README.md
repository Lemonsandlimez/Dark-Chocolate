# Dark Chocolate 🍫
dark chocolate is a lightweight, fast, easy, readable python frame-work with *zero* external dependencies.

## Overview 🚀

Dark Chocolate is a lightweight, hand‑crafted web framework designed for clarity and simplicity.
It gives you everything you need for a tiny website, all in a tiny codebase you can read in one sitting.

If you want a framework that feels like early Flask mixed with Express.js minimalism, and python simplicity this is it.

## Features ⭐

1) Simple routing with params
2) Middleware support
3) sync + Async servers
4) Cookie parsing + building
5) POST body parsing (JSON + forms)
6) JSON responses
7) File sending
8) Safe error wrapper  
.. All with zero external dependencies.

## Installation 💻

to Install, run:

```git clone https://github.com/Lemonsandlimez/Dark-chocolate```  
Or drop the Core/ folder into your project.

## Quick Examples 🧁

All examples are in the [Examples](Examples/) folder

## Getting Started 🏁

Here’s the smallest possible Dark Chocolate app:

```python
from Core.Router import Router
from Core.Server import Run, Server
from Core.Response import Response

router = Router()

@router.AddRoute("/")
def Home(req):
    return Response("Hello from Dark Chocolate!")

server = Server(router, Port=8080)
Run(server)
```

Run it with python app.py, then visit http://localhost:8080


## Included Examples 📂

Dark Chocolate comes with small, focused examples:

- **[HelloUser.py](Examples/HelloUser.py)** - route parameters  
- **[ApiTime.py](Examples/ApiTime.py)** - JSON API endpoint  
- **[EchoForm.py](Examples/EchoForm.py)** - POST form handling  
- **[CookieCounter.py](Examples/CookieCounter.py)** - cookies  
- **[SendLogo.py](Examples/SendLogo.py)** -  file sending

## Why Dark Chocolate? 🍫

- You can read the entire framework in minutes  
- Zero dependencies  
- Perfect for learning how web servers work  
- Great for tiny apps, demos, and teaching  
- Clean, expressive, Pythonic API  

## Liscense ⚖️

Dark Chocolate uses the [MIT Liscense](LISCENSE.md) and the Contributor Covenant Code of Conduct.

