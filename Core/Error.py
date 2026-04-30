# Core/Error.py

from Core.Response import Response
import traceback


def Error(Status=500, Message="Something went wrong", Details=None):
    # generic errors
    body = Message
    if Details:
        body += f"\n\nDetails: {Details}"

    return Response(
        Body=body,
        Status=Status,
        Headers={"Content-Type": "text/plain; charset=utf-8"}
    )


def BadRequest(Message="Bad Request"):
    return Error(400, Message)


def Unauthorized(Message="Unauthorized"):
    return Error(401, Message)


def Forbidden(Message="Forbidden"):
    return Error(403, Message)


def NotFound(Message="Not Found"):
    return Error(404, Message)


def ServerError(Message="Internal Server Error"):
    return Error(500, Message)


# validation helpers

def RequireFields(data, fields, error_message_prefix="Missing field"):
    """
    Check that all fields exist in a dict-like object.
    Returns:
        None if OK
        Response (400) if something is missing
    """
    missing = [f for f in fields if f not in data]
    if missing:
        msg = f"{error_message_prefix}: {', '.join(missing)}"
        return BadRequest(msg)
    return None


def Require(condition, message="Invalid request"):
    """
    If condition is False, return a 400 Response.
    Otherwise return None.
    """
    if not condition:
        return BadRequest(message)
    return None


# safe handler

def Safe(handler, show_traceback=False):
    """
    Wrap a handler so any uncaught exception becomes a 500 Response,
    instead of crashing the server.

    Usage:
        @Safe
        def MyHandler(req):
            ...
    """
    def Wrapped(request, *args, **kwargs):
        try:
            return handler(request, *args, **kwargs)
        except Exception as e:
            if show_traceback:
                tb = traceback.format_exc()
                return ServerError(f"Internal Server Error\n\n{tb}")
            return ServerError()
    return Wrapped

