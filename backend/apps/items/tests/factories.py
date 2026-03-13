"""Factory Boy factories for tests."""

import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

from apps.items.models import Item


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    @classmethod
    def _create(cls, model_class: type, *args: object, **kwargs: object) -> User:
        """Use create_user so the password is properly hashed and saved."""
        kwargs.setdefault("password", "password123")
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)  # type: ignore[return-value]


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    title = factory.Sequence(lambda n: f"Item {n}")
    description = "A test item description"
    completed = False
    owner = factory.SubFactory(UserFactory)
