"""Keep OAuth query credentials out of Uvicorn's default access logs."""

import logging


class AuthQueryRedaction(logging.Filter):
    def filter(self, record):
        args = record.args
        if isinstance(args, tuple) and len(args) == 5 and isinstance(args[2], str):
            path = args[2]
            if path.split("?", 1)[0].startswith("/auth/"):
                record.args = (*args[:2], path.split("?", 1)[0], *args[3:])
        return True


def install_auth_access_redaction():
    logger = logging.getLogger("uvicorn.access")
    if not any(isinstance(f, AuthQueryRedaction) for f in logger.filters):
        logger.addFilter(AuthQueryRedaction())
