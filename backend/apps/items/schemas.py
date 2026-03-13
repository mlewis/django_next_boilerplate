"""Pydantic schemas for the items API."""

from ninja import Schema


class ItemIn(Schema):
    title: str
    description: str = ""
    completed: bool = False


class ItemOut(Schema):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int
    created_at: str
    updated_at: str

    @staticmethod
    def resolve_created_at(obj: object) -> str:
        from datetime import datetime

        dt: datetime = getattr(obj, "created_at")
        return dt.isoformat()

    @staticmethod
    def resolve_updated_at(obj: object) -> str:
        from datetime import datetime

        dt: datetime = getattr(obj, "updated_at")
        return dt.isoformat()


class MessageOut(Schema):
    message: str
