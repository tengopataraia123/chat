
const socket = io('ws://localhost:80');

function sendMessage(){
    
/*
    <div class="row no-gutters">
        <div class="col-5">
            <div class="message">
                hello
            </div>
        </div>
    </div>
*/

    var textarea = document.getElementById("textbox");
    var messageText = textarea.value;
    textarea.value = "";

    row = document.createElement("div");
    row.className = "row no-gutters";
    col = document.createElement("div");
    col.className = "col-5 offset-7";
    message = document.createElement("div");
    message.className = "message";
    
    message.innerHTML = messageText;

    col.appendChild(message);
    row.appendChild(col);

    document.getElementById("messages").appendChild(row);

    //console.log(temp);

    socket.send(messageText);
}

function joinRoom(roomNumber){
    socket.emit("join",roomNumber);
}

socket.on("message",(messageText) =>{
    row = document.createElement("div");
    row.className = "row no-gutters";
    col = document.createElement("div");
    col.className = "col-5";
    message = document.createElement("div");
    message.className = "message";
    
    message.innerHTML = messageText;

    col.appendChild(message);
    row.appendChild(col);

    console.log(messageText);

    document.getElementById("messages").appendChild(row);
});