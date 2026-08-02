from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RecoveredPacket:
    id: str
    category: str
    icon: str
    title: str
    content: str
    comment: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RecoveredPacket":
        required = {"id", "category", "icon", "title", "content", "comment"}
        missing = required.difference(value)
        if missing:
            raise ValueError(
                "Pachet incomplet. Câmpuri lipsă: "
                + ", ".join(sorted(missing))
            )

        return cls(
            id=str(value["id"]),
            category=str(value["category"]),
            icon=str(value["icon"]),
            title=str(value["title"]),
            content=str(value["content"]),
            comment=str(value["comment"]),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "category": self.category,
            "icon": self.icon,
            "title": self.title,
            "content": self.content,
            "comment": self.comment,
        }
