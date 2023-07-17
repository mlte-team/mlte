"""
test/negotiation/test_negotiation_card.py

Unit tests for negotiation card.
"""

import mlte.negotiation as nc

# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


def test_model_resources_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    mrd = nc.ModelResourcesDescriptor()
    mrd.cpu = "cpu"
    mrd.gpu = "gpu"
    mrd.memory = "memory"
    mrd.storage = "storage"

    s = mrd.to_json()
    d = nc.ModelResourcesDescriptor.from_json(s)

    assert d == mrd

    # An empty instance can be serialized / deserialized successfull
    mrd = nc.ModelResourcesDescriptor()

    s = mrd.to_json()
    d = nc.ModelResourcesDescriptor.from_json(s)

    assert d == mrd


def test_model_input_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    mid = nc.ModelInputDescriptor()
    mid.description = "description"

    s = mid.to_json()
    d = nc.ModelInputDescriptor.from_json(s)

    assert d == mid

    # An empty instance can be serialized / deserialized successfull
    mid = nc.ModelInputDescriptor()

    s = mid.to_json()
    d = nc.ModelInputDescriptor.from_json(s)

    assert d == mid


def test_model_output_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    mod = nc.ModelOutputDescriptor()
    mod.description = "description"

    s = mod.to_json()
    d = nc.ModelOutputDescriptor.from_json(s)

    assert d == mod

    # An empty instance can be serialized / deserialized successfull
    mod = nc.ModelOutputDescriptor()

    s = mod.to_json()
    d = nc.ModelOutputDescriptor.from_json(s)

    assert d == mod


def test_model_interface_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    mid = nc.ModelInterfaceDescriptor()
    mid.input = nc.ModelInputDescriptor(description="description")
    mid.output = nc.ModelOutputDescriptor(description="description")

    s = mid.to_json()
    d = nc.ModelInterfaceDescriptor.from_json(s)

    assert d == mid

    # An empty instance can be serialized / deserialized successfull
    mid = nc.ModelInterfaceDescriptor()

    s = mid.to_json()
    d = nc.ModelInterfaceDescriptor.from_json(s)

    assert d == mid


def test_model_development_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    mdd = nc.ModelDevelopmentDescriptor()
    mdd.resources = nc.ModelResourcesDescriptor(
        cpu="cpu", gpu="gpu", memory="memory", storage="storage"
    )

    s = mdd.to_json()
    d = nc.ModelDevelopmentDescriptor.from_json(s)

    assert d == mdd

    # An empty instance can be serialized / deserialized successfull
    mdd = nc.ModelDevelopmentDescriptor()

    s = mdd.to_json()
    d = nc.ModelDevelopmentDescriptor.from_json(s)

    assert d == mdd


def test_model_production_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    mpd = nc.ModelProductionDescriptor()
    mpd.integration = "integration"
    mpd.interface = nc.ModelInterfaceDescriptor(
        input=nc.ModelInputDescriptor(description="description"),
        output=nc.ModelOutputDescriptor(description="description"),
    )
    mpd.resources = nc.ModelResourcesDescriptor(
        cpu="cpu", gpu="gpu", memory="memory", storage="storage"
    )

    s = mpd.to_json()
    d = nc.ModelProductionDescriptor.from_json(s)

    assert d == mpd

    # An empty instance can be serialized / deserialized successfull
    mpd = nc.ModelProductionDescriptor()

    s = mpd.to_json()
    d = nc.ModelProductionDescriptor.from_json(s)

    assert d == mpd


def test_model_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    md = nc.ModelDescriptor()
    md.development = nc.ModelDevelopmentDescriptor(
        resources=nc.ModelResourcesDescriptor(
            cpu="cpu", gpu="gpu", memory="memory", storage="storage"
        )
    )
    md.production = nc.ModelProductionDescriptor(
        integration="integration",
        interface=nc.ModelInterfaceDescriptor(
            input=nc.ModelInputDescriptor(description="description"),
            output=nc.ModelOutputDescriptor(description="description"),
        ),
        resources=nc.ModelResourcesDescriptor(
            cpu="cpu", gpu="gpu", memory="memory", storage="storage"
        ),
    )

    s = md.to_json()
    d = nc.ModelDescriptor.from_json(s)

    assert d == md
