"""Items API router."""

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from .models import Item
from .schemas import ItemIn, ItemOut, MessageOut

router = Router(tags=["items"])


def _authenticated_user(request: HttpRequest) -> User:
    """Cast request.user to User (safe after JWTAuth passes)."""
    assert isinstance(request.user, User)
    return request.user


@router.get("/", response=list[ItemOut], auth=JWTAuth())
def list_items(request: HttpRequest) -> list[Item]:
    """Return all items owned by the authenticated user."""
    return list(Item.objects.filter(owner=_authenticated_user(request)))


@router.post("/", response={201: ItemOut}, auth=JWTAuth())
def create_item(request: HttpRequest, payload: ItemIn) -> Item:
    """Create a new item for the authenticated user."""
    return Item.objects.create(owner=_authenticated_user(request), **payload.dict())


@router.get("/{item_id}", response=ItemOut, auth=None)
def get_item(request: HttpRequest, item_id: int) -> Item:
    """Retrieve a single item by ID (public)."""
    return get_object_or_404(Item, id=item_id)


@router.patch("/{item_id}", response=ItemOut, auth=JWTAuth())
def update_item(request: HttpRequest, item_id: int, payload: ItemIn) -> Item:
    """Update an item owned by the authenticated user."""
    user = _authenticated_user(request)
    item = get_object_or_404(Item, id=item_id, owner=user)
    for attr, value in payload.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@router.delete("/{item_id}", response=MessageOut, auth=JWTAuth())
def delete_item(request: HttpRequest, item_id: int) -> MessageOut:
    """Delete an item owned by the authenticated user."""
    user = _authenticated_user(request)
    item = get_object_or_404(Item, id=item_id, owner=user)
    item.delete()
    return MessageOut(message="Item deleted successfully")
