from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from .base import Base
from ..utils.validators.group import (
    validate_total_participants,
    validate_invite_link,
    validate_jid,
)


class Group(Base):
    __tablename__ = "groups"

    jid: Mapped[str] = mapped_column(primary_key=True)
    invite_link: Mapped[str] = mapped_column(unique=True)
    total_participants: Mapped[int] = mapped_column()

    __table_args__ = (
        CheckConstraint(
            "total_participants > 0 AND total_participants <= 1024",
            name="check_total_group_participants",
        ),
    )

    @validates("jid")
    def validate_jid(self, key: str, value: str) -> str:
        return validate_jid(jid=value)

    @validates("invite_link")
    def validate_invite_link(self, key: str, value: str) -> str:
        return validate_invite_link(invite_link=value)

    @validates("total_participants")
    def validate_total_participants(self, key: str, value: int) -> int:
        return validate_total_participants(total_participants=value)
