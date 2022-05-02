"""
Utilities for report rendering.
"""

import os
import tempfile
import webbrowser
from typing import Union, Optional

from .report import Report
from .html import _connected


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
