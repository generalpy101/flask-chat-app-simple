let socketio = io();
const messages = document.querySelector(".messages");
const messageBox = document.querySelector("#message");

const createMessage = (username, msg) => {
  const content = `
        <div class='my-2 border-black p-2'>
            <span>
                <strong> ${username} </strong>: ${msg}
            </span>
            <span class='text-gray-600'>
                ${new Date().toLocaleString()}
            </span>
        </div>
    `;
  messages.innerHTML += content;
};

socketio.on("message", (data) => {
  console.log("message received");
  createMessage(data.username, data.message);
});

const sendMessage = () => {
  if (messageBox.value == "") return;
  socketio.emit("message", {
    data: messageBox.value,
  });
  messageBox.value = "";
};
