"""
test/session/test_session.py

Unit tests for global session management.
"""

from mlte.session import session, set_model, set_namespace, set_uri, set_version


def test_session() -> None:
    namespace = "ns"
    model = "model"
    version = "v0.0.1"
    uri = "http://localhost:8080"

    set_namespace(namespace)
    set_model(model)
    set_version(version)
    set_uri(uri)

    s = session()

    assert s.context.namespace == namespace
    assert s.context.model == model
    assert s.context.version == version
    assert s.context.uri == uri
