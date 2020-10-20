
const socket = io('ws://localhost:80');

function sendMessage(){
    var message = document.getElementById("textbox").value;
    socket.send(message);
}

socket.on("connect",()=>{
    socket.send("hello");
});