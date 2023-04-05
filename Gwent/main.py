import sqlite3 as sql
from flask import Flask, request, render_template
from objects import Users, Game_records

import re

app = Flask(__name__)

@app.route("/", methods=['GET'])
def GET ():
    user_id = request.form.get('user_id', -1)
    output_g = Game_records.get_games_of_user_by_id(user_id)

    return render_template(
        'index.html',

        games = [
            {
                'id': game[0],
                'pl1': Users.get_user_by_id(game['player_1']).get('nickname', '?'),
                'pl2': Users.get_user_by_id(game['player_2']).get('nickname', '?'),
                'res': game[3],
                'd1': game[4],
                'd2': game[5],
                'actions': game[6]
            } for game in output_g
        ]
    )

@app.route("/admin", methods=['GET'])
def GET_ADMIN ():
    base = sql.connect('gwent_db.sqlite3')
    output_u = base.execute('SELECT id,nickname,email FROM users')
    output_g = base.execute('SELECT id,player_1,player_2,result,deck_1,deck_2,actions FROM games')
    base.close()

    return render_template(
        'admin.html',

        users = [
            {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            } for user in output_u.fetchall()
        ],

        games = [
            {
                'id': game[0],
                'pl1': game[1],
                'pl2': game[2],
                'res': game[3],
                'd1': game[4],
                'd2': game[5],
                'actions': game[6]
            } for game in output_g.fetchall()
        ]
    )

@app.route("/new_game", methods=['POST'])
def POST_NEW_GAME ():
    try:
        p1 = re.search('(?<=\()\d+(?=\)\s*$)', request.form.get('p1', '', type=str))
        p2 = re.search('(?<=\()\d+(?=\)\s*$)', request.form.get('p2', '', type=str))

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

        if result not in (0,1,2):
            return render_template(
                'notification.html',

                status = 'Запись не удалось создать - 400',
                message = f'Причина: результат матча должен быть равен 0, 1 или 2, получено {result!r}',
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
        base = sql.connect('gwent_db.sqlite3')
        base.execute('PRAGMA foreign_keys = ON')

        gid = request.form.get('gid', -1)

        if base.execute(f'SELECT 1 FROM games WHERE id={gid}').fetchone() is None:
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = 'Причина: игры с переданным id не существует',
            ), 400

        p1 = re.search('(?<=\()\d+(?=\)\s*$)', request.form.get('p1', '', type=str))
        p2 = re.search('(?<=\()\d+(?=\)\s*$)', request.form.get('p2', '', type=str))

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
        
        if (not base.execute(f"SELECT 1 FROM users WHERE id='{p1}'").fetchone() or 
            not base.execute(f"SELECT 1 FROM users WHERE id='{p2}'").fetchone()):
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = 'Причина: указанных игроков (или игрока) не существует',
            ), 400
        
        result = request.form.get('result', -1, type=int)

        if result not in (0,1,2):
            return render_template(
                'notification.html',

                status = 'Запись не удалось изменить - 400',
                message = f'Причина: результат матча должен быть равен 0, 1 или 2, получено {result!r}',
            ), 400
        
        d1 = re.sub('\s*,\s*', ',', request.form.get('d1', '', type=str))
        d2 = re.sub('\s*,\s*', ',', request.form.get('d2', '', type=str))
        actions = re.sub('\s*,\s*', ',', request.form.get('actions', '', type=str))

        base.execute(f"""
            UPDATE games SET
                player_1 = {p1},
                player_2 = {p2},
                result = {result},
                deck_1 = '{d1}',
                deck_2 = '{d2}',
                actions = '{actions}'
            WHERE id={gid}
        """)

        base.commit()
        base.close()

        return render_template(
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
        base = sql.connect('gwent_db.sqlite3')
        base.execute('PRAGMA foreign_keys = ON')

        gid = request.form.get('gid', -1)

        if base.execute(f'SELECT 1 FROM games WHERE id={gid}').fetchone() is None:
            return render_template(
                'notification.html',

                status = 'Запись не удалось удалить - 400',
                message = 'Причина: игры с переданным id не существует',
            ), 400

        base.execute(f"DELETE FROM games WHERE id={gid}")

        base.commit()
        base.close()

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