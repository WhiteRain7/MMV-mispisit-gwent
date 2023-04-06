import sqlite3 as sql
from random import randint

DATABASE_NAME = 'gwent_db.sqlite3'

class Users:
    BASE = 'users'
    FIELDS = ('id', 'nickname', 'email')

    @staticmethod
    def get_user_by_id (user_id : int) -> dict[str] | None:
        '''
            Returns user data as dict from database by specified user_id.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')

            data = base.execute(f"""
                SELECT {','.join(Users.FIELDS)}
                FROM users
                WHERE id={user_id}
            """).fetchone()

            base.close()

            return None if data is None else {field: data[i] for i, field in enumerate(Users.FIELDS)}

        except: return None
    
    @staticmethod
    def get_all_users () -> list[dict]:
        '''
            Returns list of users
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')
      
            data = base.execute(f"""
                SELECT {','.join(Users.FIELDS)}
                FROM users
                ORDER BY _rowid_
            """).fetchall()

            base.close()

            return [{field: row[i] for i, field in enumerate(Users.FIELDS)} for row in data]

        except: return []

    @staticmethod
    def send_match_results_to (user_id : int, result : int):
        '''
            Sends to user_id if he wins (1) or lose (-1) (or draw (0)).
        '''
        data = Users.get_user_by_id(user_id)
        print(data['email'], '-', f'results ({result}) sended')

    @staticmethod
    def send_match_history_to (user_id : int, history : list[str]) -> list[str]:
        '''
            Returns modified history.
        '''
        try:
            data = Users.get_user_by_id(user_id)

            if data:
                for i in range(len(history)):
                    history[i] = history[i].replace(data['nickname'], data['nickname'] + ' (вы)')

            return history
        except: return history

class Game_records:
    BASE = 'games'
    FIELDS = ('id', 'player_1', 'player_2', 'result', 'deck_1', 'deck_2', 'actions')

    @staticmethod
    def create_game (**game_data) -> int | None:
        '''
            Creates new game record and writes it to DB. Returns game_id on success.
            If id given, updates old record with given params.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')

            determine_winner = False
            if game_data.get('result', None) is None or game_data.get('result', None) == -1:
                determine_winner = True
                game_data['result'] = 0

            if game_data.get('id', None) is None:
                base.execute(f"""
                    INSERT INTO {Game_records.BASE} (
                        player_1,
                        player_2,
                        result,
                        deck_1,
                        deck_2,
                        actions
                    ) VALUES (
                        {game_data['p1']},
                        {game_data['p2']},
                        {game_data['result']},
                        '{game_data['d1']}',
                        '{game_data['d2']}',
                        '{game_data['actions']}'
                    )
                """)
                id = base.execute(f'SELECT id FROM {Game_records.BASE} ORDER BY _rowid_ DESC').fetchone()[0]

            else:
                p1 = game_data.get('p1', None)
                p2 = game_data.get('p2', None)
                res = game_data.get('result', None)
                d1 = game_data.get('d1', None)
                d2 = game_data.get('d2', None)
                actions = game_data.get('actions', None)

                base.execute(f"""
                    UPDATE {Game_records.BASE} SET
                        player_1={repr(p1) if p1 else 'player_1'},
                        player_2={repr(p2) if p2 else 'player_2'},
                        result={repr(res) if res else 'result'},
                        deck_1={repr(d1) if d1 else 'deck_1'},
                        deck_2={repr(d2) if d2 else 'deck_1'},
                        actions={repr(actions) if actions else 'actions'}
                    WHERE id={game_data['id']}
                """)
                id = game_data['id']

            if determine_winner:
                base.execute(f"""
                    UPDATE {Game_records.BASE}
                    SET result={Game_records.determine_winner_of(id, send_to_users=False)}
                    WHERE id={id}
                """)

            base.commit()
            base.close()

            return id

        except: return None

    @staticmethod
    def get_game_by_id (game_id : int) -> dict | None:
        '''
            Returns game data as dict from database by specified game_id.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')

            data = base.execute(f"""
                SELECT {','.join(Game_records.FIELDS)}
                FROM {Game_records.BASE}
                WHERE id={game_id}
            """).fetchone()

            base.close()

            return None if data is None else {field: data[i] for i, field in enumerate(Game_records.FIELDS)}

        except: return None

    @staticmethod
    def delete_game_by_id (game_id : int) -> bool:
        '''
            Removes game record of given id and returns True on success and False otherwise.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')

            base.execute(f"""
                DELETE FROM {Game_records.BASE}
                WHERE id={game_id}
            """)

            base.commit()
            base.close()
            return True
        except: return False

    @staticmethod
    def determine_winner_of (game_id : int, send_to_users : bool = True) -> int:
        '''
            Determines game results and writes it to DB. 
            Returns 0 on draw, 1 if first player have won, 2 if second player have won, -1 on error.
            If send_to_users is True - calls Users.send_match_results_to for both players to send results to them.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')
            game = Game_records.get_game_by_id(game_id)
            base.close()

            if game is None: return -1

            actions = game.get('actions', '').split(',')

            sum_power_1 = sum(int(power) for power in actions[0::2])
            sum_power_2 = sum(int(power) for power in actions[1::2])

            if sum_power_1 > sum_power_2: # player 1 wins
                if send_to_users:
                    Users.send_match_results_to(game.get('player_1'),  1)
                    Users.send_match_results_to(game.get('player_2'), -1)
                return 1

            elif sum_power_1 < sum_power_2: # player 2 wins
                if send_to_users:
                    Users.send_match_results_to(game.get('player_1'), -1)
                    Users.send_match_results_to(game.get('player_2'),  1)
                return 2

            else: # draw
                if send_to_users:
                    Users.send_match_results_to(game.get('player_1'), 0)
                    Users.send_match_results_to(game.get('player_2'), 0)
                return 0

        except: return -1

    @staticmethod
    def get_winner_id_of (game_id : int) -> int:
        '''
            Returns id of player who won the match with given game_id. On draw returns -1.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')
            game = Game_records.get_game_by_id(game_id)
            base.close()

            result = game.get('result', -1)

            if   result == 1: return game.get('player_1', -1)
            elif result == 2: return game.get('player_2', -1)
            else: return -1
        except: return -1

    @staticmethod
    def get_loser_id_of (game_id : int) -> int:
        '''
            Returns id of player who lose the match with given game_id. On draw returns -1.
        '''
        try:
            winner = Game_records.get_winner_id_of(game_id)
            if   winner == 1: return 2
            elif winner == 2: return 1
            else: return -1
        except: return -1
    
    @staticmethod
    def get_match_history_of (game_id : int) -> list[str]:
        '''
            Returns match history as list of messages of what players done step by step.
        '''
        try:
            history = []
            game = Game_records.get_game_by_id(game_id)

            pl1 = Users.get_user_by_id(game.get('player_1')).get('nickname')
            pl2 = Users.get_user_by_id(game.get('player_2')).get('nickname')
            is_pl1 = True
            power_1 = 0
            power_2 = 0

            history.append(f"Колода игрока {pl1} состоит из карт с силами {game.get('deck_1', '').replace(',', ', ')}")
            history.append(f"Колода игрока {pl2} состоит из карт с силами {game.get('deck_2', '').replace(',', ', ')}")
            history.append('Начало игры')
            for action in game.get('actions', '').split(','):
                if is_pl1: power_1 += int(action)
                else:      power_2 += int(action)
                history.append(f"{pl1 if is_pl1 else pl2} разыгрывает карту с силой {action} (суммарно {power_1 if is_pl1 else power_2})")
                is_pl1 = not is_pl1

            if   power_1 > power_2: result = 1
            elif power_1 < power_2: result = 2
            else:                   result = 0

            if result == game.get('result'):
                history.append('Конец игры')
                history.append(f'Итого: {power_1} : {power_2}')
                if   result == 1: history.append(f'Побеждает {pl1}')
                elif result == 2: history.append(f'Побеждает {pl2}')
                else:             history.append('Ничья')

            else:
                if game.get('result') == 1:
                    diff = power_2 - power_1 + randint(1, 7)
                    power_1 += diff
                    history.append(f"{pl1} использует способность с силой {diff} (суммарно {power_1})")
                    history.append('Конец игры')
                    history.append(f'Итого: {power_1} : {power_2}')
                    history.append(f'Побеждает {pl1}')

                elif game.get('result') == 2:
                    diff = power_1 - power_2 + randint(1, 7)
                    power_2 += diff
                    history.append(f"{pl2} использует способность с силой {diff} (суммарно {power_2})")
                    history.append('Конец игры')
                    history.append(f'Итого: {power_1} : {power_2}')
                    history.append(f'Побеждает {pl2}')

                else:
                    diff = power_1 - power_2
                    power_2 += diff
                    history.append(f"{pl2} использует способность с силой {diff} (суммарно {power_2})")
                    history.append('Конец игры')
                    history.append(f'Итого: {power_1} : {power_2}')
                    history.append(f'Ничья')

            return history

        except: return ['История матча временно недоступна']
    
    @staticmethod
    def get_games_of_user_by_id (user_id : int) -> list[dict]:
        '''
            Returns list of games data where given user participated.
        '''
        try:
            base = sql.connect(DATABASE_NAME)
            base.execute('PRAGMA foreign_keys = ON')

            if user_id == -1:         
                data = base.execute(f"""
                    SELECT {','.join(Game_records.FIELDS)}
                    FROM {Game_records.BASE}
                    ORDER BY _rowid_
                """).fetchall()

            else:
                data = base.execute(f"""
                    SELECT {','.join(Game_records.FIELDS)}
                    FROM {Game_records.BASE}
                    WHERE player_1 = {user_id} OR player_2 = {user_id}
                    ORDER BY _rowid_
                """).fetchall()

            base.close()

            return [{field: row[i] for i, field in enumerate(Game_records.FIELDS)} for row in data]

        except: return []
