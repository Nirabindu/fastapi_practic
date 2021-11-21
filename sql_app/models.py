from sql_app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True, unique=True)
    phone = Column(Integer, unique=True, nullable=False)
    password = Column(String(250))
    date = Column(Date)
    blog = relationship("Blog", back_populates="user",cascade="all, delete")


class Blog(Base):
    __tablename__ = "blog"
    blog_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    date = Column(Date)
    id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="blog")
