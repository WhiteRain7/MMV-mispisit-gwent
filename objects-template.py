class Users:
    @staticmethod
    def get_user_by_id (user_id : int) -> dict[str] | None:
        '''
            Returns user data as dict from database by specified user_id.
        '''
        return None
    
    @staticmethod
    def get_all_users () -> list[dict]:
        '''
            Returns list of users
        '''
        return []

    @staticmethod
    def send_match_results_to (user_id : int, result : int):
        '''
            Sends to user_id if he wins (1) or lose (-1) (or draw (0)).
        '''
        return

    @staticmethod
    def send_match_history_to (user_id : int, history : list[str]) -> list[str]:
        '''
            Returns modified history.
        '''
        return history

class Game_records:
    @staticmethod
    def create_game (**game_data) -> int | None:
        '''
            Creates new game record and writes it to DB. Returns game_id on success.
            If id given, updates old record with given params.
        '''
        return None

    @staticmethod
    def get_game_by_id (game_id : int) -> dict | None:
        '''
            Returns game data as dict from database by specified game_id.
        '''
        return None

    @staticmethod
    def delete_game_by_id (game_id : int) -> bool:
        '''
            Removes game record of given id and returns True on success and False otherwise.
        '''
        return False

    @staticmethod
    def determine_winner_of (game_id : int, send_to_users : bool = True) -> int:
        '''
            Determines game results and writes it to DB. 
            Returns 0 on draw, 1 if first player have won, 2 if second player have won, -1 on error.
            If send_to_users is True - calls Users.send_match_results_to for both players to send results to them.
        '''
        return -1

    @staticmethod
    def get_winner_id_of (game_id : int) -> int:
        '''
            Returns id of player who won the match with given game_id. On draw returns -1.
        '''
        return -1

    @staticmethod
    def get_loser_id_of (game_id : int) -> int:
        '''
            Returns id of player who lose the match with given game_id. On draw returns -1.
        '''
        return -1
    
    @staticmethod
    def get_match_history_of (game_id : int) -> list[str]:
        '''
            Returns match history as list of messages of what players done step by step.
        '''
        return ['История матча временно недоступна']
    
    @staticmethod
    def get_games_of_user_by_id (user_id : int) -> list[dict]:
        '''
            Returns list of games data where given user participated.
            If -1 given, returns all games.
        '''
        return []
