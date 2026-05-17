const rooms = {
    group: []
};

const unread = {
    group: 0
};

let currentRoom = "group";

const socket = new WebSocket("ws://localhost:8765");

const input = document.getElementById("message-input");
const chatContainer = document.getElementById("chat-container");

document.getElementById("group-chat").onclick = () => switchRoom("group");

socket.onopen = () => {
    socket.send(USERNAME);
};

socket.onmessage = (event) => {

    const data = JSON.parse(event.data);

    const div = document.createElement("div");

    const currentTime = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
    if (data.type === "private") {

    createPrivateRoom(data.from);

    div.classList.add("private-message");

    div.innerHTML = `
        <div class="private-label">Private Message</div>
        <div class="username">${data.from}</div>
        <div class="message-content">${data.message}</div>
        <div class="message-time">${currentTime}</div>
    `;

    rooms[data.from].push(div);

    if (currentRoom === data.from) {
        renderRoom();
    } else {
        unread[data.from] = (unread[data.from] || 0) + 1;
        updateUnreadBadge(data.from);
    }
}

else if (data.type === "private_sent") {
    div.classList.add("my-private-message");

    const text = data.message;
    const target = data.to;

    div.innerHTML = `
        <div class="private-label">Private</div>
        <div class="message-content">${text}</div>
        <div class="message-time">${currentTime}</div>
    `;

    createPrivateRoom(target);
    rooms[target].push(div);

    if (currentRoom === target) {
        renderRoom();
    }
}

    else if (data.type === "system") {

        div.classList.add("system-message-box");

       const text = data.message;

        div.innerHTML = `
            <div class="system-label">System</div>
            <div class="message-content">${text}</div>
            <div class="message-time">${currentTime}</div>
        `;
        rooms.group.push(div);

        if (currentRoom === "group") {
            renderRoom();
        }
    }


    else if (
    data.type === "join" ||
    data.type === "left"
    ) {

        div.classList.add("system-message-box");

        div.innerHTML = `
            <div class="system-label">System</div>
            <div class="message-content">
            ${data.user} ${data.type === "join" ? "joined the chat" : "left the chat"}
            </div>
            <div class="message-time">${currentTime}</div>
        `;
        rooms.group.push(div);

        if (currentRoom === "group") {
            renderRoom();
        }
    }


else if (data.type === "public") {

    const username = data.from;
    const text = data.message;

    if (username === USERNAME) {

        div.classList.add("my-message");

        div.innerHTML = `
            <div class="message-content">${text}</div>
            <div class="message-time">${currentTime}</div>
        `;
    }
    else {

        div.classList.add("other-message");

        div.innerHTML = `
            <div class="username">${username}</div>
            <div class="message-content">${text}</div>
            <div class="message-time">${currentTime}</div>
        `;
    }

    rooms.group.push(div);

    if (currentRoom === "group") {
        renderRoom();
    } else {
        unread.group++;
        updateUnreadBadge("group");
    }
    }
};



input.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {

        const msg = input.value.trim();

        if (msg !== "") {

            if(currentRoom === "group"){

                socket.send(msg);

            }else{

                socket.send(`@${currentRoom} ${msg}`);
            }

            input.value = "";
        }
    }
});

function createPrivateRoom(username) {

    if (rooms[username]) return;

    rooms[username] = [];
    unread[username] = 0;

    const div = document.createElement("div");

    div.classList.add("chat-item");

    div.innerText = username;

    div.dataset.room = username;

    div.onclick = () => switchRoom(username);

    document.getElementById("sidebar").appendChild(div);
}

function switchRoom(roomName){

    currentRoom = roomName;

    unread[roomName] = 0;
    updateUnreadBadge(roomName);

    document.querySelectorAll(".chat-item").forEach(item=>{
        item.classList.remove("active");
    });

    if(roomName === "group"){
        document.getElementById("group-chat").classList.add("active");
    }else{
        document.querySelector(`[data-room="${roomName}"]`).classList.add("active");
    }

    renderRoom();
}

function renderRoom() {
    chatContainer.innerHTML = "";

    if (!rooms[currentRoom]) return;

    rooms[currentRoom].forEach(msg => {
        chatContainer.appendChild(msg);
    });

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateUnreadBadge(room) {
    const item = 
        room === "group"
        ? document.getElementById("group-chat")
        : document.querySelector(`[data-room="${room}"]`);

    if (!item) return;

    let badge = item.querySelector(".unread-badge");

    if (unread[room] > 0) {

        if (!badge) {
            badge = document.createElement("span");
            badge.classList.add("unread-badge");
            item.appendChild(badge);
        }

        badge.innerText = unread[room];

    } else {

        if (badge) {
            badge.remove();
        }
    }
}
