function save() {
    window.location.replace('/home')
  }

  function logout() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/l/logout", false ); 
    xmlHttp.send( null );
    window.location.replace('/home')
  }