const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatOutput = document.getElementById("chat-output");
const botSuccessMessageTemplate = (text) => `<span
            class="bot-message inline-flex items-center gap-x-2 rounded-full bg-green-600/20 px-2.5 py-1 text-sm font-semibold leading-5 text-green-600"
    >
    <span class="inline-block h-1.5 w-1.5 rounded-full bg-green-600"></span>
    ${text}
  </span><br>`;

const botErrorMessageTemplate = (text) => `<span
    class="bot-message inline-flex items-center gap-x-2 rounded-full bg-amber-600/20 px-2.5 py-1 text-sm font-semibold leading-5 text-amber-600"
  >
    <span class="inline-block h-1.5 w-1.5 rounded-full bg-amber-600"></span>
    ${text}
  </span><br>`;

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    chatOutput.innerHTML += `<p class="user-message">${message}</p>`;
    chatInput.value = "";
    chatOutput.scrollTop = chatOutput.scrollHeight;

    fetch('/process-request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data: message }),
    })
    var eventSource = new EventSource("/stream");
    eventSource.onmessage = function(e) {
      if (e.data === "TASK_DONE") {
        eventSource.close()
      } else {
        chatOutput.innerHTML += botSuccessMessageTemplate(e.data);
      }
    };
    // for (var i = 0; i < 30; i++) {
    //     chatOutput.innerHTML += botSuccessMessageTemplate("Jasiek jest" + i);
    //     if (i%2 == 0) {
    //         chatOutput.innerHTML += botErrorMessageTemplate("jhasfjssa vdfa fdsjf sdfkhs fskfjhshh  ajsdkasj SJADKDJKD JDSKADJA SDkKKKKKKKKKKKK error" + i);
    //     }
    //     chatOutput.scrollTop = chatOutput.scrollHeight;
    // }
    // const response = await fetch("gptchat.php", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({ message }),
    // });

    // if (response.ok) {
    //     const data = await response.json();
    //     if (data.choices && data.choices[0] && data.choices[0].text) {
    //         chatOutput.innerHTML += `<p class="bot-message">${data.choices[0].text}</p>`;
    //     } else {
    //         console.error("Error: Unexpected response format", data);
    //     }
    //     chatOutput.scrollTop = chatOutput.scrollHeight;
    // } else {
    //     console.error("Error communicating with GPTChat API");
    // }
});