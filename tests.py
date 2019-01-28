import unittest

from app import app
from app import db
from app.models import User

class UserModelCase(unittest.TestCase):
    def set_up(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tear_down(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        user = User(username="test")
        user.set_password("password")
        self.assertFalse(user.check_password("notpassword"))
        self.assertTrue(user.check_password("password"))

    def test_avatar(self):
        user = User(username="test", email="test@test.com")
        self.assertEqual(user.avatar(128), ("https://gravatar.com/avatar/"
                                            "b642b4217b34b1e8d3bd915fc65c4452"
                                            "?d=robohash&s=128"))

    def test_follow(self):
        user1 = User(username="test", email="test@test.com")
        user2 = User(username="test2", email="test2@test.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.following.all(), [])
        self.assertEqual(user1.followers.all(), [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.following.count(), 1)
        self.assertEqual(user1.following.first().username, "test2")
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, "test")

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.following.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

        db.session.delete(user1)
        db.session.delete(user2)
        db.session.commit()


if __name__ == "__main__":
    unittest.main(verbosity=2)