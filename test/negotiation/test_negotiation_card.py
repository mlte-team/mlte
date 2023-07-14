"""
test/negotiation/test_negotiation_card.py

Unit tests for negotiation card.
"""

import mlte.negotiation as nc

# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


def test_problem_type() -> None:
    for problem_type in nc.ProblemType:
        s = problem_type.to_json()
        d = nc.ProblemType.from_json(s)
        assert d == problem_type


def test_metric_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    m = nc.MetricDescriptor()
    m.description = "description"
    m.baseline = "baseline"

    s = m.to_json()
    d = nc.MetricDescriptor.from_json(s)

    assert m == d

    # An empty instance can be serialized / deserialized successfully
    m = nc.MetricDescriptor()

    s = m.to_json()
    d = nc.MetricDescriptor.from_json(s)

    assert m == d


def test_goal_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    g = nc.GoalDescriptor()
    g.description = "description"
    g.metrics = [
        nc.MetricDescriptor(description="description", baseline="baseline")
    ]

    s = g.to_json()
    d = nc.GoalDescriptor.from_json(s)

    assert g == d

    # An empty instance can be serialized / deserialized successfully
    g = nc.GoalDescriptor()

    s = g.to_json()
    d = nc.GoalDescriptor.from_json(s)

    assert g == d


def test_risk_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    r = nc.RiskDescriptor()
    r.fp = "fp"
    r.fn = "fn"
    r.other = "other"

    s = r.to_json()
    d = nc.RiskDescriptor.from_json(s)

    assert r == d

    # An empty instance can be serialized / deserialized successfully
    r = nc.RiskDescriptor()

    s = r.to_json()
    d = nc.RiskDescriptor.from_json(s)

    assert r == d


def test_system_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    sys = nc.SystemDescriptor()
    sys.goals = [
        nc.GoalDescriptor(
            description="description",
            metrics=[
                nc.MetricDescriptor(
                    description="description", baseline="baseline"
                )
            ],
        )
    ]
    sys.problem_type = nc.ProblemType.CLASSIFICATION
    sys.task = "task"
    sys.usage_context = "usage_context"
    sys.risks = nc.RiskDescriptor(fp="fp", fn="fn", other="other")

    s = sys.to_json()
    d = nc.SystemDescriptor.from_json(s)

    assert sys == d

    # An empty instance can be serialized / deserialized successfull
    sys = nc.SystemDescriptor()

    s = sys.to_json()
    d = nc.SystemDescriptor.from_json(s)

    assert sys == d


# -----------------------------------------------------------------------------
# Data Subcomponents
# -----------------------------------------------------------------------------


def test_data_classification() -> None:
    for classification in nc.DataClassification:
        s = classification.to_json()
        d = nc.DataClassification.from_json(s)
        assert d == classification


def test_data_label_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    data = nc.LabelDescriptor()
    data.description = "description"
    data.percentage = 95.0

    s = data.to_json()
    d = nc.LabelDescriptor.from_json(s)

    assert d == data

    # An empty instance can be serialized / deserialized successfull
    data = nc.LabelDescriptor()

    s = data.to_json()
    d = nc.LabelDescriptor.from_json(s)

    assert d == data


def test_data_field_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    fd = nc.FieldDescriptor()
    fd.name = "name"
    fd.description = "description"
    fd.type = "type"
    fd.expected_values = "expected_values"
    fd.missing_values = "missing_values"
    fd.special_values = "special_values"

    s = fd.to_json()
    d = nc.FieldDescriptor.from_json(s)

    assert d == fd

    # An empty instance can be serialized / deserialized successfull
    fd = nc.FieldDescriptor()

    s = fd.to_json()
    d = nc.FieldDescriptor.from_json(s)

    assert d == fd


def test_data_descriptor() -> None:
    # A complete instance can be serialized / deserialized successfully
    dd = nc.DataDescriptor()
    dd.description = "description"
    dd.classification = nc.DataClassification.UNCLASSIFIED
    dd.access = "access"
    dd.fields = [
        nc.FieldDescriptor(
            name="name",
            description="description",
            type="type",
            expected_values="expected_values",
            missing_values="missing_values",
            special_values="special_values",
        )
    ]
    dd.labels = [nc.LabelDescriptor(description="description", percentage=95.0)]
    dd.policies = "policies"
    dd.rights = "rights"
    dd.source = "source"
    dd.identifiable_information = "identifiable_information"

    s = dd.to_json()
    d = nc.DataDescriptor.from_json(s)

    # An empty instance can be serialized / deserialized successfull
    dd = nc.DataDescriptor()

    s = dd.to_json()
    d = nc.DataDescriptor.from_json(s)

    assert d == dd


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
