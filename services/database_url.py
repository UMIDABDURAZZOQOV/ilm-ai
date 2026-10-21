"""Select the PostgreSQL driver installed by requirements, across SQLAlchemy versions."""


def normalize_database_url(url):
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg2://" + url[len(prefix):]
    return url
