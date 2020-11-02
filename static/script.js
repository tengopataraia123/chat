const url = document.location.origin;

const socket = io(url+":80");

var room = 0;
var username = localStorage.getItem("username");

function addMessage(msg,user="",received=true){
    row = document.createElement("div");
    row.className = "row no-gutters";
    col = document.createElement("div");

    if(received){
        col.className = "col-5";
    }else{
        col.className = "col-5 offset-7";
    }
    
    username = document.createElement("div");
    username.className = "username";
    username.innerHTML = user;

    message = document.createElement("div");
    message.className = "message";

    messageText = document.createElement("div");
    messageText.className = "messageText";
    messageText.innerHTML = msg;

    message.appendChild(username);
    message.appendChild(messageText);

    col.appendChild(message);
    row.appendChild(col);

    document.getElementById("messages").appendChild(row);
    document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}

function sendMessage(){
    var textarea = document.getElementById("textbox");
    var messageText = textarea.value;
    textarea.value = "";

    addMessage(messageText,false);

    socket.send({"text":messageText,"room":room});
}

function joinRoom(roomNumber){

    document.getElementById("messages").innerHTML = "";

    if(room != roomNumber){
        socket.emit("leave-room",room)
    }
    socket.emit("join-room",roomNumber);
    room = roomNumber;
    fetchMessages(room);
}

socket.on("message",(messageText) =>{
    addMessage(messageText); 
});

socket.on("old-messages",(data) =>{
    if(data.mine){
        addMessage(data.text,false);
    }else{
        addMessage(data.text);
    }
});

function fetchMessages(data){
    var reqUrl = `/oldMessages?room=${room}`;
    fetch(reqUrl)
    .then((response)=>{
        return response.json();
    }).then(response =>{
        response.data.forEach((message) =>{
            if(message.username != response.user){
                addMessage(message.text,message.username);
            }else{
                addMessage(message.text,message.username,false);
            }
        });
    });
}

window.onload = (event) => {
    joinRoom(room);
}