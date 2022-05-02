"""
Utilities for report rendering.
"""

import os
import socket
import tempfile
import webbrowser
from typing import Union, Optional

from .report import Report


def _connected(host: str = "8.8.8.8", port: int = 53, timeout: int = 2) -> bool:
    """
    Determine if internet connectivity is available.

    :param host: The host used to test connectivity
    :type host: str
    :param port: The port used to test connectivity
    :type port: int
    :param timeout: The connection timeout
    :type timeout: int

    :return `True` if connected to the internet, `False` otherwise
    :rtype: bool
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def render(target: Union[Report, str]):
    """
    Render a Report as a web page.

    If possible, the rendered report is automatically
    opened in an available window in the default browser.

    The argument `target` may be specified as either the
    Report instance itself, or the HTML content generated
    via a call to Report.to_html(). Rendering reports from
    the local filesystem is currently unsupported.

    :param target: The report content to render
    :type target: Union[Report, str]
    """
    # TODO(Kyle): Validate HTML input.

    if not _connected():
        raise RuntimeError(
            "An internet connection is required to render a report."
        )

    html: Optional[str] = (
        target.to_html() if isinstance(target, Report) else target
    )
    assert html is not None, "Broken invariant."

    with tempfile.TemporaryDirectory() as dirname:
        path = os.path.join(dirname, "index.html")
        with open(path, "w") as f:
            f.write(html)
        webbrowser.open(f"file://{os.path.realpath(path)}")
