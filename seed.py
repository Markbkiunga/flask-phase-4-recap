from app import app
from models import User, Post, Group, UserGroup, db
from sqlalchemy.exc import IntegrityError

with app.app_context():
    # Create Users
    print("Creating users....")
    user1 = User(username="john_doe", email_address="john@example.com")
    user2 = User(username="jane_doe", email_address="jane@example.com")
    user3 = User(username="alice_smith", email_address="alice@example.com")

    # Create Posts
    print("Creating posts....")
    post1 = Post(
        title="First Post", description="This is the first post by John", user=user1
    )
    post2 = Post(
        title="Second Post", description="This is the first post by Jane", user=user2
    )
    post3 = Post(
        title="Third Post", description="This is the second post by John", user=user1
    )

    # Create Groups
    print("Creating groups....")
    group1 = Group(name="Python Developers")
    group2 = Group(name="Data Scientists")
    group3 = Group(name="Web Developers")

    # Assign Users to Groups via UserGroup
    user1.groups.append(group1)  # John in Python Developers
    user1.groups.append(group2)  # John in Data Scientists
    user2.groups.append(group3)  # Jane in Web Developers
    user3.groups.append(group1)  # Alice in Python Developers

    try:
        # Add the users, posts, and groups to the session and commit
        db.session.add_all([user1, user2, user3])
        db.session.add_all([post1, post2, post3])
        db.session.add_all([group1, group2, group3])
        db.session.commit()
        print("Database seeded successfully!")
    except IntegrityError as e:
        print(f"Error seeding database: {e}")
        db.session.rollback()
    finally:
        db.session.close()
