
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlmodel import Session, SQLModel

from app.core.config import settings
from app.core.database import get_session
from app.main import app


@pytest.fixture(scope="session")
def test_engine() -> Engine:
    if settings.test_database_url is None:
        raise RuntimeError("TEST_DATABASE_URL is not configured")

    engine = create_engine(
        settings.test_database_url,
        echo=False,
    )

    # Prepare a clean database schema for the test session.
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine: Engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session):
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
