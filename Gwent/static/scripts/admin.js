let new_game_id = 1

function add_new_game () {
    form = document.getElementById('new_game_form')

    tr = document.createElement('tr')
    tr.setAttribute('onclick', `document.getElementById('game_N${ new_game_id }_cb').click()`)
    tr.innerHTML = `
        <td>N${new_game_id}</td>
        <td>${form.querySelector('input[name="p1"]').value.match(/(\d+)[?=\)]$/)[1]}</td>
        <td>${form.querySelector('input[name="p2"]').value.match(/(\d+)[?=\)]$/)[1]}</td>
        <td>${form.querySelector('select').value}</td>
        <td>${form.querySelector('input[name="d1"]').value}</td>
        <td>${form.querySelector('input[name="d2"]').value}</td>
        <td>${form.querySelector('input[name="actions"]').value}</td>
        <td><input id='game_N${ new_game_id }_cb' type="radio" name="game_radio" onclick="document.getElementById('game_N${ new_game_id }_cb').click(); game_control(false)"></td>
    `
    new_game_id += 1
    document.querySelector('#game_table tbody').appendChild(tr)
    notify('Форма отправлена', `Новая запись о матче (N${new_game_id-1})`)
    hide_all()
}

function change_game () {
    form = document.getElementById('edit_game_form')

    id = form.querySelector('input[name="gid"]').value
    tr = document.querySelector(`tr#game_${ id }_tr`)
    if (tr) {
        tr.innerHTML = `
            <td>${id}</td>
            <td>${form.querySelector('input[name="p1"]').value.match(/(\d+)[?=\)]$/)[1]}</td>
            <td>${form.querySelector('input[name="p2"]').value.match(/(\d+)[?=\)]$/)[1]}</td>
            <td>${form.querySelector('select').value}</td>
            <td>${form.querySelector('input[name="d1"]').value}</td>
            <td>${form.querySelector('input[name="d2"]').value}</td>
            <td>${form.querySelector('input[name="actions"]').value}</td>
            <td><input id='game_${ id }_cb' type="radio" name="game_radio" onclick="document.getElementById('game_${ id }_cb').click(); game_control(false)"></td>
        `
    }
    notify('Форма отправлена', `Изменена запись о матче (${id})`)
    hide_all()
}

function delete_game () {
    form = document.getElementById('delete_game_form')
    tr = document.querySelector(`tr#game_${ form.querySelector('input[name="gid"]').value }_tr`)
    tr.remove()
    notify('Форма отправлена', `Удалена запись о матче (${id})`)
    hide_all()
}

function game_form_create () {
    document.querySelector('#new_game_form input[type="reset"]').click()

    hide_all()
    document.getElementById('dark_bg').classList.remove('hidden')
    document.getElementById('new_game_panel').classList.remove('hidden')
}

function game_form_change () {
    document.querySelector('#edit_game_form input[type="reset"]').click()

    id = document.querySelector('input[type="radio"][name="game_radio"]:checked').value

    data = document.getElementById(`game_${id}_tr`)
    form = document.getElementById('edit_game_form')

    form.querySelector('input[name="gid"]'     ).value = id
    form.querySelector('input[name="p1"]'      ).value = data.children[0].innerText
    form.querySelector('input[name="p2"]'      ).value = data.children[1].innerText
    form.querySelector('select[name="result"]' ).value = data.children[2].innerText
    form.querySelector('input[name="d1"]'      ).value = data.children[3].innerText
    form.querySelector('input[name="d2"]'      ).value = data.children[4].innerText
    form.querySelector('input[name="actions"]' ).value = data.children[5].innerText

    hide_all()
    document.getElementById('dark_bg').classList.remove('hidden')
    document.getElementById('edit_game_panel').classList.remove('hidden')
}

function game_form_delete () {
    document.querySelector('#delete_game_form input[type="reset"]').click()

    id = document.querySelector('input[type="radio"][name="game_radio"]:checked').value

    data = document.getElementById(`game_${id}_tr`)
    form = document.getElementById('delete_game_form')

    form.querySelector('input[name="gid"]'     ).value = id
    form.querySelector('input[name="p1"]'      ).value = data.children[0].innerText
    form.querySelector('input[name="p2"]'      ).value = data.children[1].innerText
    form.querySelector('select[name="result"]' ).value = data.children[2].innerText
    form.querySelector('input[name="d1"]'      ).value = data.children[3].innerText
    form.querySelector('input[name="d2"]'      ).value = data.children[4].innerText
    form.querySelector('input[name="actions"]' ).value = data.children[5].innerText

    hide_all()
    document.getElementById('dark_bg').classList.remove('hidden')
    document.getElementById('delete_game_panel').classList.remove('hidden')
}

function game_control (enabled = true) {
    if (enabled) {
        document.getElementById('GC_change').removeAttribute('disabled')
        document.getElementById('GC_delete').removeAttribute('disabled')
    }
    else {
        document.getElementById('GC_change').setAttribute('disabled', 'disabled')
        document.getElementById('GC_delete').setAttribute('disabled', 'disabled')
    }
}

function hide_all () {
    document.getElementById('dark_bg').classList.add('hidden')
    document.getElementById('new_game_panel').classList.add('hidden')
    document.getElementById('edit_game_panel').classList.add('hidden')
    document.getElementById('delete_game_panel').classList.add('hidden')
}

let not_id = 1
function notify (text, header = 'Предупреждение', nav = 'хорошо') {
    not = document.createElement('div')
    not.setAttribute('id', 'not-' + not_id)
    not.innerHTML = `
        <div class='not-header'><h1>${header}</h1></div>
        <div class='not-body'><p>${text.replaceAll('\n', '</p><p>')}</p></div>
        <div class='not-nav'><input type='button' value='${nav}' class='click_button' onclick='document.getElementById("not-${not_id}").remove()'></div>
    `
    not_id++
    document.getElementById('notifications').appendChild(not)
}