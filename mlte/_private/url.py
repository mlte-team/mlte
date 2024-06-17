from typing import Optional, Tuple
from urllib.parse import ParseResult, quote, urlparse


def set_url_username_password(url: str, username: str, password: str) -> str:
    """Adds the given username and password to an URL."""
    _username = quote(username)
    _password = quote(password)
    _url = urlparse(url)
    _netloc = _url.netloc.split("@")[-1]
    _url = _url._replace(netloc=f"{_username}:{_password}@{_netloc}")
    return _url.geturl()


def remove_url_username_password(
    url: str,
) -> Tuple[str, Optional[str], Optional[str]]:
    """Removes user and password from URL, and returns the cleaned url, as well as the user and password, if any."""
    parsed_uri: ParseResult = urlparse(url)

    # Remove them from uri.
    if parsed_uri.hostname is not None:
        new_netloc = parsed_uri.hostname
        if parsed_uri.port is not None:
            new_netloc = f"{new_netloc}:{parsed_uri.port}"
        clear_uri = parsed_uri._replace(netloc=new_netloc)
        url = clear_uri.geturl()

    return url, parsed_uri.username, parsed_uri.password
