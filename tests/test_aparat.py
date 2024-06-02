import unittest
from aparat import Aparat, IncorrectPasswordError, UsernameNotFoundError, LoginRequiredError

class TestAparat(unittest.TestCase):
    def setUp(self):
        self.aparat = Aparat()

    def test_login_success(self):
        self.assertTrue(self.aparat.login("username", "password"))

    def test_login_incorrect_password(self):
        with self.assertRaises(IncorrectPasswordError):
            self.aparat.login("username", "incorrect_password")

    def test_login_username_not_found(self):
        with self.assertRaises(UsernameNotFoundError):
            self.aparat.login("non_existing_username", "password")

    def test_get_me_logged_in(self):
        self.aparat.login("username", "password")
        self.assertIsNotNone(self.aparat.get_me())

    def test_get_me_not_logged_in(self):
        with self.assertRaises(LoginRequiredError):
            self.aparat.get_me()

if __name__ == '__main__':
    unittest.main()
