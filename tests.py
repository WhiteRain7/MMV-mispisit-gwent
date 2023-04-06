import objects
import unittest
import sys
import os
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

    def test_sending_results (self):
        sys.stdout = io.StringIO('123')
        objects.Users.send_match_results_to(1, -1)
        objects.Users.send_match_results_to(2,  0)
        objects.Users.send_match_results_to(3,  1)
        objects.Users.send_match_results_to(4,  1)
        objects.Users.send_match_results_to('abc', 1)
        objects.Users.send_match_results_to('abc', 2)
        objects.Users.send_match_results_to(3,  2)
        objects.Users.send_match_results_to(3,  None)
        stdout = sys.stdout
        sys.stdout = sys.__stdout__
        stdout.seek(0)

        self.assertEqual(
            stdout.readlines(),
            [
                'example1@mail.com - results (-1) sended\n',
                'example2@mail.com - results (0) sended\n',
                'example3@mail.com - results (1) sended\n',
                'user with id 4 is not exists\n',
                'user with id abc is not exists\n',
                'invalid result to send - 2\n',
                'invalid result to send - 2\n',
                'invalid result to send - None\n'
            ]
        )

    def test_sending_history (self):
        self.assertEqual(objects.Users.send_match_history_to(1, ['abc']), ['abc'])
        self.assertEqual(objects.Users.send_match_history_to(2, ['name2 abc']), ['name2 (вы) abc'])
        self.assertEqual(objects.Users.send_match_history_to(4, ['name4']), ['name4'])
        self.assertEqual(objects.Users.send_match_history_to(4, None), None)
        self.assertEqual(objects.Users.send_match_history_to(3, None), None)

class Test_Game_Records (unittest.TestCase):
    def test_create_game (self):
        self.assertEqual(objects.Game_records.create_game(
            p1 = 1,
            p2 = 2
        ), 1)
        self.assertEqual(objects.Game_records.create_game(
            p1 = 2,
            p2 = 3,
            d1 = '1,3,5',
            d2 = '2,4,6',
            actions = '1,2,3,4,5,6'
        ), 2)
        self.assertEqual(objects.Game_records.create_game(
            p1 = 3,
            p2 = 1,
            result = 1,
            d1 = '25,25',
            d2 = '50',
            actions = '25,50,25'
        ), 3)
        self.assertEqual(objects.Game_records.create_game(
        ), None)
        self.assertEqual(objects.Game_records.create_game(
            p1 = '123',
            p2 = 4,
        ), None)
        self.assertEqual(objects.Game_records.create_game(
            p1 = 1,
            p2 = 2,
            result=10
        ), None)
        self.assertEqual(objects.Game_records.create_game(
            p1 = 1,
            p2 = 2,
            result=None,
            d1 = '1',
            d2 = '2',
            actions = '1,2'
        ), 4)
        self.assertEqual(objects.Game_records.create_game(
            id=4,
            result=-1,
            d1 = '4,8,6',
            d2 = '5,7,1',
            actions = '8,7,4,1,6,5'
        ), 4)

    def test_getting_games (self):
        sys.stdout = io.StringIO()
        self.assertDictEqual(
            objects.Game_records.get_game_by_id(1),
            {
                'id': 1,
                'player_1': 1,
                'player_2': 2,
                'result': 0,
                'deck_1': '',
                'deck_2': '',
                'actions': ''
            }
        )
        self.assertDictEqual(
            objects.Game_records.get_game_by_id(2),
            {
                'id': 2,
                'player_1': 2,
                'player_2': 3,
                'result': 2,
                'deck_1': '1,3,5',
                'deck_2': '2,4,6',
                'actions': '1,2,3,4,5,6'
            }
        )
        self.assertDictEqual(
            objects.Game_records.get_game_by_id(3),
            {
                'id': 3,
                'player_1': 3,
                'player_2': 1,
                'result': 1,
                'deck_1': '25,25',
                'deck_2': '50',
                'actions': '25,50,25'
            }
        )
        self.assertDictEqual(
            objects.Game_records.get_game_by_id(4),
            {
                'id': 4,
                'player_1': 1,
                'player_2': 2,
                'result': 1,
                'deck_1': '4,8,6',
                'deck_2': '5,7,1',
                'actions': '8,7,4,1,6,5'
            }
        )
        self.assertIsNone(objects.Game_records.get_game_by_id(5))
        self.assertIsNone(objects.Game_records.get_game_by_id(-1))
        self.assertIsNone(objects.Game_records.get_game_by_id(None))
        self.assertIsNone(objects.Game_records.get_game_by_id('abc'))
        sys.stdout = sys.__stdout__

    def test_delelting_games (self):
        objects.Game_records.create_game(p1=1, p2=2)

        self.assertTrue(objects.Game_records.delete_game_by_id(5))
        self.assertFalse(objects.Game_records.delete_game_by_id(5))
        self.assertFalse(objects.Game_records.delete_game_by_id(-1))
        self.assertFalse(objects.Game_records.delete_game_by_id('abc'))
        self.assertFalse(objects.Game_records.delete_game_by_id(None))

    def test_determing_winners (self):
        sys.stdout = io.StringIO()
        self.assertEqual(objects.Game_records.determine_winner_of(1), 0)
        self.assertEqual(objects.Game_records.determine_winner_of(2), 2)
        self.assertEqual(objects.Game_records.determine_winner_of(3), 0)
        self.assertEqual(objects.Game_records.determine_winner_of(4), 1)
        self.assertEqual(objects.Game_records.determine_winner_of(5), -1)
        self.assertEqual(objects.Game_records.determine_winner_of(-1), -1)
        sys.stdout = sys.__stdout__

    def test_getting_winner (self):
        self.assertEqual(objects.Game_records.get_winner_id_of(1), -1)
        self.assertEqual(objects.Game_records.get_winner_id_of(2), 3)
        self.assertEqual(objects.Game_records.get_winner_id_of(3), 3)
        self.assertEqual(objects.Game_records.get_winner_id_of(4), 1)
        self.assertEqual(objects.Game_records.get_winner_id_of(5), -1)
        self.assertEqual(objects.Game_records.get_winner_id_of(-1), -1)

    def test_getting_loser (self):
        self.assertEqual(objects.Game_records.get_loser_id_of(1), -1)
        self.assertEqual(objects.Game_records.get_loser_id_of(2), 2)
        self.assertEqual(objects.Game_records.get_loser_id_of(3), 1)
        self.assertEqual(objects.Game_records.get_loser_id_of(4), 2)
        self.assertEqual(objects.Game_records.get_loser_id_of(5), -1)
        self.assertEqual(objects.Game_records.get_loser_id_of(-1), -1)

    def test_getting_history (self):
        self.assertListEqual(
            objects.Game_records.get_match_history_of(1),
            [
                'Колода игрока name1 состоит из карт с силами ',
                'Колода игрока name2 состоит из карт с силами ',
                'Начало игры',
                'Конец игры',
                'Итого: 0 : 0',
                'Ничья'
            ]
        )
        self.assertListEqual(
            objects.Game_records.get_match_history_of(2),
            [
                'Колода игрока name2 состоит из карт с силами 1, 3, 5',
                'Колода игрока name3 состоит из карт с силами 2, 4, 6',
                'Начало игры',
                'name2 разыгрывает карту с силой 1 (суммарно 1)',
                'name3 разыгрывает карту с силой 2 (суммарно 2)',
                'name2 разыгрывает карту с силой 3 (суммарно 4)',
                'name3 разыгрывает карту с силой 4 (суммарно 6)',
                'name2 разыгрывает карту с силой 5 (суммарно 9)',
                'name3 разыгрывает карту с силой 6 (суммарно 12)',
                'Конец игры',
                'Итого: 9 : 12',
                'Побеждает name3'
            ]
        )
        self.assertListEqual(
            objects.Game_records.get_match_history_of(10),
            ['История матча временно недоступна']
        )

    def test_getting_multiple_games (self):
        games = [
            {
                'id': 1,
                'player_1': 1,
                'player_2': 2,
                'result': 0,
                'deck_1': '',
                'deck_2': '',
                'actions': ''
            },{
                'id': 2,
                'player_1': 2,
                'player_2': 3,
                'result': 2,
                'deck_1': '1,3,5',
                'deck_2': '2,4,6',
                'actions': '1,2,3,4,5,6'
            },{
                'id': 3,
                'player_1': 3,
                'player_2': 1,
                'result': 1,
                'deck_1': '25,25',
                'deck_2': '50',
                'actions': '25,50,25'
            },{
                'id': 4,
                'player_1': 1,
                'player_2': 2,
                'result': 1,
                'deck_1': '4,8,6',
                'deck_2': '5,7,1',
                'actions': '8,7,4,1,6,5'
            }
        ]

        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id(1),
            [games[0], games[2], games[3]]
        )
        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id(2),
            [games[0], games[1], games[3]]
        )
        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id(3),
            [games[1], games[2]]
        )
        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id(-1),
            games
        )
        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id(10),
            []
        )
        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id('abc'),
            []
        )
        self.assertListEqual(
            objects.Game_records.get_games_of_user_by_id(None),
            []
        )

if __name__ == '__main__':
    with open ('test_db-copy.sqlite3', 'rb') as fin:
        with open ('test_db.sqlite3', 'wb') as fout:
            fout.write(fin.read())

    objects.DATABASE_NAME = 'test_db.sqlite3'

    unittest.main()

    os.remove('test_db.sqlite3')
