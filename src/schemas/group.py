from pydantic import field_validator, Field

from .base import BaseSchema
from ..utils.validators.group import (
    validate_jid,
    validate_invite_link,
    validate_total_participants,
)


class CreateGroup(BaseSchema):
    jid: str = Field(default=..., examples=["12345678912345@g.us"])
    invite_link: str = Field(
        default=..., examples=["https://chat.whatsapp.com/asetdEdkl3190DSFnDSdjq"]
    )
    total_participants: int = Field(default=..., examples=["234"])

    @field_validator("jid")
    @classmethod
    def validate_jid(cls, value: str) -> str:
        return validate_jid(jid=value)

    @field_validator("invite_link")
    @classmethod
    def validate_invite_link(cls, value: str) -> str:
        return validate_invite_link(invite_link=value)

    @field_validator("total_participants")
    @classmethod
    def validate_total_participants(cls, value: int) -> int:
        return validate_total_participants(total_participants=value)


class UpdateTotalParticipants(BaseSchema):
    jid: str = Field(default=..., examples=["12345678912345@g.us"])
    total_participants: int = Field(default=..., examples=["234"])

    @field_validator("jid")
    @classmethod
    def validate_jid(cls, value: str) -> str:
        return validate_jid(jid=value)

    @field_validator("total_participants")
    @classmethod
    def validate_total_participants(cls, value: int) -> int:
        return validate_total_participants(total_participants=value)


class GroupResponse(BaseSchema):
    jid: str = Field(default=..., examples=["12345678912345@g.us"])
    invite_link: str = Field(
        default=..., examples=["https://chat.whatsapp.com/asetdEdkl3190DSFnDSdjq"]
    )
    total_participants: int = Field(default=..., examples=["234"])

    @field_validator("jid")
    @classmethod
    def validate_jid(cls, value: str) -> str:
        return validate_jid(jid=value)

    @field_validator("invite_link")
    @classmethod
    def validate_invite_link(cls, value: str) -> str:
        return validate_invite_link(invite_link=value)

    @field_validator("total_participants")
    @classmethod
    def validate_total_participants(cls, value: int) -> int:
        return validate_total_participants(total_participants=value)
