function clear_bnd() {
    document.getElementById('banned').innerHTML = ''
} 

document.getElementById('go').addEventListener('click', function () {
  if(!(document.getElementById('email').value.includes('/') || document.getElementById('passwd').value.includes('/'))) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/l/do=" + document.getElementById("email").value + "&&" + document.getElementById("passwd").value, false ); 
    xmlHttp.send( null );
    if(xmlHttp.responseText == 'failure') {
      document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">Email or Password are wrong.</span>";
      return;
    }
    else if(xmlHttp.responseText == 'alr') {
      document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-success\" style=\"padding-top: 1%; text-align: left;\">You are already logged in to an account.</span>";
      return;
    }
    else if(xmlHttp.responseText == 'banned') {
      document.getElementById('banned').innerHTML = '        <article class="message is-danger">\
<div class="message-header">\
<p>Security Ban.</p>\
<button class="delete" aria-label="delete" onclick="clear_bnd()"></button>\
</div>\
<div class="message-body">\
Our Bot protection has permanently banned your ip from this platform.<br>\
Please contact contact@nosehad.com if you believe, this is an error.\
</div>\
</article>';
    }
    else if (xmlHttp.responseText == 'done') {
      window.location.replace("/home");
    }
  } else {
    document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">Email or Password are wrong.</span>";
  }
})