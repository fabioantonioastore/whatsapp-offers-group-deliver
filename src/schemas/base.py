from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_serialization_defaults_required=True,
        extra="forbid",
    )
