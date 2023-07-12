from fastapi.testclient import TestClient
from faker import Faker
from dataclasses import dataclass, field
from src.routers import app
import pytest


@dataclass(init=True, frozen=True)
class State:
    new_ids: list[str] = field(init=False, default_factory=list)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def fake() -> Faker:
    return Faker()


@pytest.fixture
def state() -> State:
    return State()
