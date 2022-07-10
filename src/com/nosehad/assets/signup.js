function clear_bnd() {
    document.getElementById('banned').innerHTML = ''
  } 

  document.getElementById('create').addEventListener('click', function () {
    if(document.getElementById("passwd1").value != document.getElementById("passwd2").value) {
      document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">Passwords don't match.</span>";
    }
    else if(document.getElementById("email").value.includes('/')) { // i have to do this here, otherwise it could result in html errors
      document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">Email is invalid.</span>";
    }
    else if(!document.getElementById('accept').checked) {
      document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">You have to agree to our terms and conditions.</span>";
    }
    else if(!(document.getElementById('email').value.includes('/') || document.getElementById('passwd1').value.includes('/') || document.getElementById('passwd2').value.includes('/'))) {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open( "GET", "/l/create=" + document.getElementById("email").value + "&&" + document.getElementById("passwd1").value, false ); 
      xmlHttp.send( null );
      if(xmlHttp.responseText == 'failure') {
        document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">User with this email already exists.</span>";
      }
      else if(xmlHttp.responseText == 'alr') {
        document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-success\" style=\"padding-top: 1%; text-align: left;\">You are already logged in to an account.</span>";
      }
      else if(xmlHttp.responseText == 'email') {
        document.getElementById('res').innerHTML = "<span class=\"tag is-danger is-light\" style=\"padding-top: 1%; text-align: left;\">Email is invalid.</span>";
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
    }
  })