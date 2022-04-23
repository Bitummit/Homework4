from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    scoped_session,
    relationship,
    Session as SessionType
)
from datetime import datetime


class Base:
    id = Column(Integer, primary_key=True)


DB_URL = "sqlite:///blog.db"
DB_ECHO = True

engine = create_engine(url=DB_URL, echo=DB_ECHO)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base = declarative_base(bind=engine, cls=Base)


class User(Base):
    __tablename__ = "users"
    login = Column(String(32), unique=True)
    password = Column(String(32))
    username = Column(String(20), nullable=True)
    age = Column(Integer, nullable=True)

    posts = relationship("Post")
    comments = relationship("Comment")

    def __str__(self):
        return (f"User("
                f"id={self.id},"
                f" {self.login},"
                f" password={self.password},"
                f" username={self.username},"
                f" age={self.age})")

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"
    post_title = Column(String(128))
    post_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey(User.id))

    comments = relationship("Comment")

    def __str__(self):
        return (f"Post("
                f"id={self.id},"
                f" title={self.post_title},"
                f" text={self.post_text},"
                f" user_id={self.user_id})")

    def __repr__(self):
        return str(self)


class Comment(Base):
    __tablename__ = "comments"
    comment_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey(User.id))
    post_id = Column(Integer, ForeignKey(Post.id))

    def __str__(self):
        return (f"Comment("
                f"id={self.id},"
                f" text={self.comment_text},"
                f" user_id={self.user_id},"
                f" post_id={self.post_id})")

    def __repr__(self):
        return str(self)


def get_users(session: SessionType) -> list[User]:
    users = session.query(User).all()
    print(users)
    return users


def get_posts(session: SessionType) -> list[Post]:
    posts = session.query(Post).all()
    print(posts)
    return posts


def get_comments(session: SessionType) -> list[Comment]:
    comments = session.query(Comment).all()
    print(comments)
    return comments


def create_user(session: SessionType, login:str, password:str) -> User:
    user = User(login=login, password=password)
    session.add(user)
    session.commit()
    return user


def create_post(session: SessionType, title: str, text: str, user: User) -> Post:
    post = Post(post_title=title, post_text=text, user_id=user.id)
    session.add(post)
    session.commit()
    return post


def create_comment(session: SessionType, text: str, user: User, post: Post) -> Comment:
    comment = Comment(comment_text=text, user_id=user.id, post_id=post.id)
    session.add(comment)
    session.commit()
    return comment


def get_user_by_id(session: SessionType, id: int) -> User:
    user = session.query(User).filter_by(id=id).first()
    return user


def get_post_by_id(session: SessionType, id: int) -> Post:
    post = session.query(Post).filter_by(id=id).first()
    return post


def get_admin_users_only(session: SessionType) -> list[User]:
    admins = session.query(User).filter(User.login.like(f"%admin%")).all()
    return admins


def main():
    Base.metadata.create_all()
    session: SessionType = Session()

    user = get_user_by_id(session, 1)
    post = get_post_by_id(session, 1)


    # create_user(session, "Ignat", "1234")
    # create_post(session, "Videos", "some text", user)
    # create_comment(session, "some comment", user, post)


    get_users(session)
    get_comments(session)
    get_posts(session)

    print(get_admin_users_only(session))

    session.close()


if __name__ == '__main__':
    main()