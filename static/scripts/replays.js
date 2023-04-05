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

function game_control (enabled = true) {
    if (enabled) {
        document.getElementById('GC_view').removeAttribute('disabled')
    }
    else {
        document.getElementById('GC_view').setAttribute('disabled', 'disabled')
    }
}

function go_to_match () {
    radio = document.querySelector('#game_table tr input[type="radio"]:checked')
    if (radio) document.location.search = 'history_of=' + radio.value
}