from flask import Flask, request, render_template
from objects import Users, Game_records

import re

app = Flask(__name__)

@app.route("/", methods=['GET'])
def GET ():
    game_id = request.args.get('history_of', None)
    user_id = request.args.get('user_id', -1, type=int)

    if game_id is not None:
        game_id = int(game_id)
        history = Game_records.get_match_history_of(game_id)
        game = Game_records.get_game_by_id(game_id)

        history = Users.send_match_history_to(user_id, history)

        return render_template(
            'history.html',

            history = enumerate(history, start=1),
            game = {
                'id': game.get('id'),
                'pl1': Users.get_user_by_id(game.get('player_1', '')).get('nickname', '?'),
                'pl2': Users.get_user_by_id(game.get('player_2', '')).get('nickname', '?'),
                'res':
                    'ничья' if game.get('result') == 0 else
                    'победа игрока 1' if game.get('result') == 1 else
                    'победа игрока 2' if game.get('result') == 2 else
                    '?',
                'd1': game.get('deck_1'),
                'd2': game.get('deck_2'),
                'actions': game.get('actions')
            }
        )
    
    output_u = Users.get_all_users()
    output_g = Game_records.get_games_of_user_by_id(user_id)

    return render_template(
        'index.html',

        current_user = user_id,

        users = [
            {
                'id': user.get('id'),
                'name': user.get('nickname'),
                'email': user.get('email')
            } for user in output_u
        ],

        games = [
            {
                'id': game.get('id'),
                'pl1': Users.get_user_by_id(game.get('player_1', '')).get('nickname', '?'),
                'pl2': Users.get_user_by_id(game.get('player_2', '')).get('nickname', '?'),
                'res': 
                    'ничья' if game.get('result') == 0 else
                    'победа игрока 1' if game.get('result') == 1 else
                    'победа игрока 2' if game.get('result') == 2 else
                    '?',
                'd1': game.get('deck_1'),
                'd2': game.get('deck_2'),
                'actions': game.get('actions')
            } for game in output_g
        ]
    )

@app.route("/admin", methods=['GET'])
def GET_ADMIN ():
    output_u = Users.get_all_users()
    output_g = Game_records.get_games_of_user_by_id(-1)

    return render_template(
        'admin.html',

        users = [
            {
                'id': user.get('id'),
                'name': user.get('nickname'),
                'email': user.get('email')
            } for user in output_u
        ],

        games = [
            {
                'id': game['id'],
                'pl1': game['player_1'],
                'pl2': game['player_2'],
                'res': game['result'],
                'd1': game['deck_1'],
                'd2': game['deck_2'],
                'actions': game['actions']
            } for game in output_g
        ]
    )

@app.route("/new_game", methods=['POST'])
def POST_NEW_GAME ():
    try:
        p1 = re.search('^\d+$|(?<=\()\d+(?=\)\s*$)', request.form.get('p1', '', type=str))
        p2 = re.search('^\d+$|(?<=\()\d+(?=\)\s*$)', request.form.get('p2', '', type=str))

        if (p1 is None or 
            p2 is None or
            not (p1:= p1.group()).isdigit() or
            not (p2:= p2.group()).isdigit() or
            (p1:= int(p1)) == (p2:= int(p2))
            ):
            return render_template(
                'notification.html',

                status = 'Запись не удалось создать - 400',
                message = 'Причина: поля с игроками заполнены не правильно, повторяются или не заполнены вообще',
            ), 400
        
        if (Users.get_user_by_id(p1) is None or 
            Users.get_user_by_id(p2) is None):
            return render_template(
                'notification.html',

                status = 'Запись не удалось создать - 400',
                message = 'Причина: указанных игроков (или игрока) не существует',
            ), 400
        
        result = request.form.get('result', -1, type=int)

        if result not in (-1, 0,1,2):
            return render_template(
                'notification.html',

                status = 'Запись не удалось создать - 400',
                message = f'Причина: результат матча должен быть равен 0, 1, 2 или отсутствовать, получено {result!r}',
            ), 400
        
        d1 = re.sub('\s*,\s*', ',', request.form.get('d1', '', type=str))
        d2 = re.sub('\s*,\s*', ',', request.form.get('d2', '', type=str))
        actions = re.sub('\s*,\s*', ',', request.form.get('actions', '', type=str))

        success = Game_records.create_game(
            p1 = p1,
            p2 = p2,
            result = result,
            d1 = d1,
            d2 = d2,
            actions = actions,
        )

        if success: return render_template(
            'notification.html',

            status = 'Запись создана успешно',
            message = '-',
        ), 201

        else: raise Exception('game create fail')
    
    except Exception as e:
        print(e)
        return render_template(
            'notification.html',

            status = 'Запись не удалось создать - 500',
            message = 'Причина: внутренняя ошибка сервера при добавлении новой записи матча',
        ), 500


@app.route("/edit_game", methods=['POST'])
def POST_CHANGED_GAME ():
    try:
        gid = request.form.get('gid', -1)

        if Game_records.get_game_by_id(gid) is None:
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = 'Причина: игры с переданным id не существует',
            ), 400

        p1 = re.search('^\d+$|(?<=\()\d+(?=\)\s*$)', request.form.get('p1', '', type=str))
        p2 = re.search('^\d+$|(?<=\()\d+(?=\)\s*$)', request.form.get('p2', '', type=str))

        if (p1 is None or 
            p2 is None or
            not (p1:= p1.group()).isdigit() or
            not (p2:= p2.group()).isdigit() or
            (p1:= int(p1)) == (p2:= int(p2))
            ):
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = 'Причина: поля с игроками заполнены не правильно, повторяются или не заполнены вообще',
            ), 400
        
        if (Users.get_user_by_id(p1) is None or 
            Users.get_user_by_id(p2) is None):
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = 'Причина: указанных игроков (или игрока) не существует',
            ), 400
        
        result = request.form.get('result', -1, type=int)

        if result not in (-1, 0,1,2):
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = f'Причина: результат матча должен быть равен 0, 1, 2 или отсутствовать, получено {result!r}',
            ), 400
        
        d1 = re.sub('\s*,\s*', ',', request.form.get('d1', '', type=str))
        d2 = re.sub('\s*,\s*', ',', request.form.get('d2', '', type=str))
        actions = re.sub('\s*,\s*', ',', request.form.get('actions', '', type=str))

        success = Game_records.create_game(
            id = gid,
            p1 = p1,
            p2 = p2,
            result = result,
            d1 = d1,
            d2 = d2,
            actions = actions,
        )

        if success: return render_template(
            'notification.html',

            status = 'Запись изменена успешно',
            message = '-',
        ), 201
    
    except Exception as e:
        print(e)
        return render_template(
            'notification.html',

            status = 'Запись не удалось изменить - 500',
            message = 'Причина: внутренняя ошибка сервера при изменении записи матча',
        ), 500


@app.route("/delete_game", methods=['POST'])
def POST_DELETE_GAME ():
    try:
        assert Game_records.delete_game_by_id(request.form.get('gid', -1, type=int)), "game haven't been deleted"

        return render_template(
            'notification.html',

            status = 'Запись удалена успешно',
            message = '-',
        ), 201
    
    except Exception as e:
        print(e)
        return render_template(
            'notification.html',

            status = 'Запись не удалось удалить - 500',
            message = 'Причина: внутренняя ошибка сервера при удалении записи матча',
        ), 500