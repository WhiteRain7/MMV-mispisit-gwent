import sqlite3 as sql

class Users:
    def get_user_by_id (user_id : int) -> dict[str] | None:
        '''
            Returns user data as dict from database by specified user_id.
        '''
        try:
            base = sql.connect('gwent_db.sqlite3')
            base.execute('PRAGMA foreign_keys = ON')

            fields = ('nickname', 'email')

            data = base.execute(f"""
                SELECT {','.join(fields)}
                FROM users
                WHERE id={user_id}
            """).fetchone()

            base.close()

            return None if data is None else {field: data[i] for i, field in enumerate(fields)}

        except: return None

    def send_match_results_to (user_id : int, result : int):
        '''
            Sends to user_id if he wins or lose (or draw).
        '''

    def send_match_history_to (user_id : int, history : list[str]):
        '''
            Sends to user_id by email specified match history.
        '''

class Game_records:
    def create_game (**game_data) -> int | None:
        '''
            Creates new game record and writes it to DB. Returns game_id on success.
        '''
        try:
            base = sql.connect('gwent_db.sqlite3')
            base.execute('PRAGMA foreign_keys = ON')

            base.execute(f"""
                INSERT INTO games (
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

            id = base.execute('SELECT id FROM games ORDER BY _rowid_ DESC').fetchone()[0]

            base.commit()
            base.close()

            return id

        except: return None

    def get_game_by_id (game_id : int) -> dict | None:
        '''
            Returns game data as dict from database by specified game_id.
        '''
        return None

    def delete_game_by_id (game_id : int) -> bool:
        '''
            Removes game record of given id and returns True on success and False otherwise.
        '''
        return False

    def determine_winner_of (game_id : int, send_to_users : bool = True) -> int:
        '''
            Determines game results and writes it to DB. 
            Returns 0 on draw, 1 if first player have won, 2 if second player have won, -1 on error.
            If send_to_users is True - calls Users.send_match_results_to for both players to send results to them.
        '''
        return -1

    def get_winner_id_of (game_id : int) -> int:
        '''
            Returns id of player who won the match with given game_id. On draw returns -1.
        '''
        return -1

    def get_loser_id_of (game_id : int) -> int:
        '''
            Returns id of player who lose the match with given game_id. On draw returns -1.
        '''
        return -1
    
    def get_match_history_of (game_id : int) -> list[str]:
        '''
            Returns match history as list of messages of what players done step by step.
        '''
        return []
    
    def get_games_of_user_by_id (user_id : int) -> list[dict]:
        '''
            Returns list of games data where given user participated.
        '''
        try:
            base = sql.connect('gwent_db.sqlite3')
            base.execute('PRAGMA foreign_keys = ON')

            fields = ['player_1', 'player_2', 'result', 'deck_1', 'deck_2', 'actions']

            if user_id == -1:         
                data = base.execute(f"""
                    SELECT {','.join(fields)}
                    FROM games
                    ORDER BY _rowid_
                """).fetchall()

            else:
                data = base.execute(f"""
                    SELECT {','.join(fields)}
                    FROM games
                    WHERE player_1 = {user_id} OR player_2 = {user_id}
                    ORDER BY _rowid_
                """).fetchall()

            base.close()

            return [{field: row[i] for i, field in enumerate(fields)} for row in data]

        except: return []
