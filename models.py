from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)

    posts = db.relationship("Post", back_populates="user", cascade="all, delete-orphan")
# groups = db.relationship("Group", secondary_table="user_groups", back_populates="users")
    user_groups = db.relationship("UserGroup", back_populates="user", cascade= "all, delete-orphan")

    groups = association_proxy("user_groups", "group", creator=lambda group_obj: UserGroup(group = group_obj))
    @validates("email_address")
    def validate_email(self, key, email_address):
        if "@" not in email_address:
            raise ValueError ("Email address must contain @")
        return email_address
    
class Post(db.Model, SerializerMixin):
    __tablename__= "posts"
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="posts")

class UserGroup(db.Model, SerializerMixin):
    __tablename__ = "user_groups"
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    user = db.relationship("User", back_populates="user_groups")
    group = db.relationship("Group", back_populates="user_groups")

class Group(db.Model, SerializerMixin):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String())

    user_groups = db.relationship("UserGroup", back_populates="group", cascade= "all, delete-orphan")

    users = association_proxy("user_groups", "user", creator= lambda user_obj: UserGroup(user= user_obj))
# users = db.relationship("User", secondary_table="user_groups", back_populates="groups")
# # Using an association table
# user_groups = db.Table("user_groups",
#                        db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
#                        db.Column("group_id", db.Integer, db.ForeignKey("groups.id"))
#                        )