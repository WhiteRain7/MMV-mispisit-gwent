import objects
import unittest
import sys
import io

class Test_Users (unittest.TestCase):
    def test_getting (self):
        self.assertDictEqual(
            objects.Users.get_user_by_id(1),
            {'id': 1, 'nickname': 'name1', 'email': 'example1@mail.com'}
        )
        self.assertDictEqual(
            objects.Users.get_user_by_id(2),
            {'id': 2, 'nickname': 'name2', 'email': 'example2@mail.com'}
        )
        self.assertDictEqual(
            objects.Users.get_user_by_id(3),
            {'id': 3, 'nickname': 'name3', 'email': 'example3@mail.com'}
        )
        self.assertIsNone(objects.Users.get_user_by_id(-1))
        self.assertIsNone(objects.Users.get_user_by_id('123'))
        self.assertIsNone(objects.Users.get_user_by_id(None))

    def test_getting_all (self):
        self.assertCountEqual(
            objects.Users.get_all_users(),
            [
                {'id': 1, 'nickname': 'name1', 'email': 'example1@mail.com'},
                {'id': 2, 'nickname': 'name2', 'email': 'example2@mail.com'},
                {'id': 3, 'nickname': 'name3', 'email': 'example3@mail.com'}
            ]
        )

    def test_sending_match_results (self):
        sys.stdout = io.StringIO()
        self.assertEqual()
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    objects.DATABASE_NAME = 'test_db.sqlite3'

    unittest.main()
