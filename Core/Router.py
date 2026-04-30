# Core/Router.py

class Router:
    def __init__(self):
        self.Routes = []
        self.Middleware = []

    def Use(self, func):
        self.Middleware.append(func)

    def AddRoute(self, Pattern, Handler=None):
        """
        Supports both:
            router.AddRoute("/path", handler)
        And:
            @router.AddRoute("/path")
            def handler(req):
                ...
        """

        # Decorator mode
        if Handler is None:
            def wrapper(func):
                parts = [p for p in Pattern.split("/") if p]
                self.Routes.append((parts, func))
                return func
            return wrapper

        # Direct call mode
        parts = [p for p in Pattern.split("/") if p]
        self.Routes.append((parts, Handler))
        return Handler

    def Match(self, Path):
        parts = [p for p in Path.split("/") if p]

        for route_parts, handler in self.Routes:
            if len(route_parts) != len(parts):
                continue

            params = {}
            matched = True

            for rp, pp in zip(route_parts, parts):
                if rp.startswith(":"):
                    params[rp[1:]] = pp
                elif rp != pp:
                    matched = False
                    break

            if matched:
                return handler, params

        return None, {}

    def Handle(self, Request):
        # Run middleware
        for func in self.Middleware:
            result = func(Request)
            if result is not None:
                return result

        # Match route
        handler, params = self.Match(Request.Path)
        if handler is None:
            return None

        Request.Params = params
        return handler(Request, **params)

