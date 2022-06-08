"""App exceptions handlers

Example:

    async def some_exception_handler(rq, exc):
        ...

        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

    And add to function add_exception_handlers:
        app.exception_handler(SomeException)(some_exception_handler)
"""


def add_exception_handlers(app):
    pass


__all__ = ["add_exception_handlers"]
