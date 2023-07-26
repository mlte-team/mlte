"""
test/session/test_session.py

Unit tests for global session management.
"""

from mlte.session import session, set_context, set_store


def test_session() -> None:
    namespace = "ns"
    model = "model"
    version = "v0.0.1"
    uri = "memory://"

    set_context(namespace, model, version)
    set_store(uri)

    s = session()

    assert s.context.namespace == namespace
    assert s.context.model == model
    assert s.context.version == version
    assert s.store.uri.uri == uri
