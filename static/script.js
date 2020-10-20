
const socket = io('ws://localhost:80');

function sendMessage(){
    var messageText = document.getElementById("textbox").value;
/*
    <div class="row no-gutters">
        <div class="col-5">
            <div class="message">
                hello
            </div>
        </div>
    </div>
*/

    row = document.createElement("div");
    row.className = "row no-gutters";
    col = document.createElement("div");
    col.className = "col-5 offset-7";
    message = document.createElement("div");
    message.className = "message";
    
    message.innerHTML = messageText;

    col.appendChild(message);
    row.appendChild(col);

    document.getElementsByClassName("messages").appendChild(row);

    //console.log(row);

    socket.send(message);
}

function joinRoom(roomNumber){
    socket.emit("join",roomNumber);
}

socket.on("connect",()=>{
    socket.send("hello");
});