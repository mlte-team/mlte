from pydantic import BaseModel


class Value:
    pass


class Integer(Value):
    pass


class ValueModel(BaseModel):
    identifier: str
    """"""

    evidence_metadata: str
    """"""

    body: Union[IntegerModel, FloatModel]
    """"""


class IntegerModel(ValueModel):
    pass


class OpaqueModel:
    dict[str, Any]
