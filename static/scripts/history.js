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