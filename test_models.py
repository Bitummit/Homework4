from pytest import fixture
from models import Session, SessionType, get_posts, create_user, get_users


@fixture
def session_instance() -> SessionType:
    session: SessionType = Session()
    return session


def test_get_posts(session_instance):
    posts = get_posts(session_instance)
    assert len(posts) == 2


def test_create_user(session_instance):
    login = "Mark"
    password = "Mark1"
    user = create_user(session_instance, login, password)
    users = get_users(session_instance)
    assert user in users
