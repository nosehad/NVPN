var tsl = true;  
function create() {

    document.getElementById('create').innerHTML = '<div class="wrap">\
        <h2>Get your aLink: </h2>\
        <button id="confirm" type="submit" class="cbutton" onclick="pull()" style="width: 75px;border-top-right-radius: 0px;border-bottom-right-radius: 0px;">Get</button>\
        <input  class="cinput" onclick="swap()" id="prot" style="width: 64px;" disabled="disabled" type="text" placeholder="https://">\
        <input  class="cinput" style="border-top-right-radius: 10px; border-bottom-right-radius: 10px; color: #9b9a9d" type="text" placeholder="example.com" id="target">\
    </div>'
}

function pull() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/l/get=" + (tsl ? 'https:&2F&2F' : 'http:&2F&2F') + document.getElementById('target').value.replaceAll('?', '&3F').replaceAll('/', '&2F'), false ); 
    xmlHttp.send( null );
    document.getElementById('create').innerHTML = '<div class="wrap">\
        <h2>Success!</h2>\
        <p>Your aLink: <strong><a style="color: #4290f5;" href="' + xmlHttp.responseText + '">' + xmlHttp.responseText + '</a></strong></p>\
        <button class="bbutton" onclick="window.location.replace(\'/alink\')" style="border-bottom-left-radius: 10px;border-top-left-radius: 10px;">Go Back</button>\
    </div>'
}

function swap() {
    tsl = ! tsl;
    document.getElementById('prot').setAttribute('placeholder', tsl ? 'https://' : 'http://');
}

function back() {
    window.location.replace('/home')
}