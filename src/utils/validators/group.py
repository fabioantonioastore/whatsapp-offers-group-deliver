def validate_jid(jid: str) -> str:
    if not "@" in jid:
        raise ValueError("Invalid JID format")
    jid_parts = jid.split("@")
    if not (jid_parts[0].isdecimal() and jid_parts[1] == "g.us"):
        raise ValueError("Invalid JID format")
    return jid


def validate_invite_link(invite_link: str) -> str:
    if not invite_link.startswith("https://chat.whatsapp.com"):
        raise ValueError("Invalid invite link format")
    return invite_link


def validate_total_participants(total_participants: int) -> int:
    if not (0 < total_participants <= 1024):
        raise ValueError(
            "Invalid total participants value, must be greater than 0 e less or equal than 1024"
        )
    return total_participants
