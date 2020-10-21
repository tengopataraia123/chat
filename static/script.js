
const socket = io('ws://localhost:80');

var room = 0;

function addMessage(msg,received=true){
    row = document.createElement("div");
    row.className = "row no-gutters";
    col = document.createElement("div");

    if(received){
        col.className = "col-5";
    }else{
        col.className = "col-5 offset-7";
    }

    message = document.createElement("div");
    message.className = "message";
    
    message.innerHTML = msg;

    col.appendChild(message);
    row.appendChild(col);

    document.getElementById("messages").appendChild(row);
}

function sendMessage(){
    var textarea = document.getElementById("textbox");
    var messageText = textarea.value;
    textarea.value = "";

    addMessage(messageText,false);

    socket.send({"text":messageText,"room":room});
}

function joinRoom(roomNumber){
    if(room){
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
    socket.emit("fetch-messages",room);
}