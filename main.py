"""Main file"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Form

DATABASE_URL = "postgresql://postgres:2846Max&@localhost:5432/Labs"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
app = FastAPI()

class User(Base):
    """User class"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship('Post', back_populates='owner')

class Post(Base):
    """Posts class"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='posts')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

user1 = User(id=0, username="Igor", email="igor@mail.mail", password="password")
user2 = User(id=1, username="Igor2", email="igor2@mail.mail", password="password")
user3 = User(id=2, username="Igor3", email="igor3@mail.mail", password="password")
session.add_all([user1, user2, user3])
session.commit()

post1 = Post(title="Igor post", content="Igor post.", user_id=user1.id)
post2 = Post(title="Igor2 post", content="Igor2 post.", user_id=user2.id)
post3 = Post(title="Igor3 post", content="Igor3 post.", user_id=user3.id)
session.add_all([post1, post2, post3])
session.commit()

users = session.query(User).all()
for user in users:
    print(user.username, user.email, user.password)

posts = session.query(Post).all()
for post in posts:
    print(post.title, post.content, post.user_id)

user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
for post in user_posts:
    print(post.title, post.content, post.user_id)

user_to_update = session.query(User).filter(User.id == 0).first()
user_to_update.email = "notigor@mail.mail"
session.commit()

post_to_update = session.query(Post).filter(Post.id == 1).first()
post_to_update.content = "No post anymore"
session.commit()

post_to_delete = session.query(Post).filter(Post.id == 2).first()
session.delete(post_to_delete)
session.commit()

user_to_delete = session.query(User).filter(User.id == 1).first()
session.delete(user_to_delete)
session.commit()

@app.post("/user create")
def user_create(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """User create"""
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()

@app.post("/post create")
def post_create(title: str = Form(...), content: str = Form(...), user_id: str = Form(...)):
    """Post create"""
    post = Post(title=title, content=content, user_id=user_id)
    session.add(post)
    session.commit()

@app.get("/users")
def users_show():
    """Show all users"""
    users = session.query(User).all()
    return users

@app.get("/posts")
def posts_show():
    """Show all posts"""
    posts = session.query(Post).all()
    return posts

@app.put("/user/update/{id}")
def user_update(i: int, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """Edit user"""
    user_edit = session.query(User).filter(User.id == i).first()
    user_edit.username = username
    user_edit.email = email
    user_edit.password = password
    session.commit()

@app.put("/post/update/{id}")
def post_update(i: int, title: str = Form(...), content: str = Form(...), user_id: str = Form(...)):
    """Edit posts"""
    post_edit = session.query(Post).filter(Post.id == i).first()
    post_edit.title = title
    post_edit.content = content
    post_edit.user_id = user_id
    session.commit()

@app.delete("/user/delete/{id}")
def user_delete(i: int):
    """User delete"""
    user_d = session.query(User).filter(User.id == i).first()
    session.delete(user_d)
    session.commit()

@app.delete("/post/delete/{id}")
def post_delete(i: int):
    """User delete"""
    post_d = session.query(Post).filter(Post.id == i).first()
    session.delete(post_d)
    session.commit()
