function settings() {
    window.location.replace('/settings')
}

document.getElementById('amazon').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Famazon.com");
});
document.getElementById('github').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Fgithub.com");
});
document.getElementById('pinterest').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Fpinterest.com");
});
document.getElementById('stackoverflow').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Fstackoverflow.com");
});
document.getElementById('wikipedia').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Fen.wikipedia.org");
});
document.getElementById('reddit').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Freddit.com");
});
document.getElementById('apple').addEventListener("click", function(){ 
    window.location.replace("/open?data=https%3A%2F%2Fapple.com");
});