from urllib.parse import urlparse


def http_program(url: str) -> bool:
    supported_schemes = {"http", "https"}  # Используем множество для быстрого поиска
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    host = parsed_url.hostname

    if scheme not in supported_schemes:
        raise ValueError(f"Scheme must be one of {supported_schemes}")
    if host is None or host == "":
        raise ValueError("Host must be non-empty")

    # Выполнение каких-либо действий с URL
    return True
