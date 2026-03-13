"""Unit tests for the items API."""

import pytest
from django.contrib.auth.models import User
from django.test import Client

from apps.items.models import Item

from .factories import ItemFactory, UserFactory


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def user() -> User:
    return UserFactory()  # type: ignore[return-value]


@pytest.fixture
def auth_headers(user: User, client: Client) -> dict[str, str]:
    """Obtain a JWT access token and return Authorization header."""
    response = client.post(
        "/api/auth/pair",
        data={"username": user.username, "password": "password123"},
        content_type="application/json",
    )
    assert response.status_code == 200, response.content
    token: str = response.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.mark.django_db
class TestListItems:
    def test_returns_only_own_items(
        self, client: Client, user: User, auth_headers: dict[str, str]
    ) -> None:
        ItemFactory.create_batch(3, owner=user)
        ItemFactory.create_batch(2)  # another user's items

        response = client.get("/api/items/", **auth_headers)

        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_requires_auth(self, client: Client) -> None:
        response = client.get("/api/items/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestCreateItem:
    def test_creates_item(
        self, client: Client, user: User, auth_headers: dict[str, str]
    ) -> None:
        payload = {"title": "New Item", "description": "Some description"}

        response = client.post(
            "/api/items/",
            data=payload,
            content_type="application/json",
            **auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Item"
        assert data["owner_id"] == user.pk
        assert Item.objects.filter(owner=user).count() == 1

    def test_requires_auth(self, client: Client) -> None:
        response = client.post(
            "/api/items/", data={"title": "x"}, content_type="application/json"
        )
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetItem:
    def test_retrieves_item(self, client: Client, user: User) -> None:
        item = ItemFactory(owner=user)

        response = client.get(f"/api/items/{item.pk}")

        assert response.status_code == 200
        assert response.json()["id"] == item.pk
        assert response.json()["title"] == item.title

    def test_returns_404_for_missing(self, client: Client) -> None:
        response = client.get("/api/items/99999")
        assert response.status_code == 404


@pytest.mark.django_db
class TestDeleteItem:
    def test_deletes_own_item(
        self, client: Client, user: User, auth_headers: dict[str, str]
    ) -> None:
        item = ItemFactory(owner=user)

        response = client.delete(f"/api/items/{item.pk}", **auth_headers)

        assert response.status_code == 200
        assert not Item.objects.filter(pk=item.pk).exists()

    def test_cannot_delete_others_item(
        self, client: Client, auth_headers: dict[str, str]
    ) -> None:
        other_item = ItemFactory()  # different owner

        response = client.delete(f"/api/items/{other_item.pk}", **auth_headers)

        assert response.status_code == 404
