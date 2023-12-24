const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatOutput = document.getElementById("chat-output");
const funcTemplate = (text) => `<span
class="inline-flex mt-1.5 items-center gap-x-2 rounded-full bg-green-600/20 px-2.5 py-1 text-sm font-semibold leading-5 text-green-600">
<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="16" height="16" viewBox="0 0 48 48">
<linearGradient id="HoiJCu43QtshzIrYCxOfCa_VFaz7MkjAiu0_gr1" x1="21.241" x2="3.541" y1="39.241" y2="21.541" gradientUnits="userSpaceOnUse"><stop offset=".108" stop-color="#0d7044"></stop><stop offset=".433" stop-color="#11945a"></stop></linearGradient><path fill="url(#HoiJCu43QtshzIrYCxOfCa_VFaz7MkjAiu0_gr1)" d="M16.599,41.42L1.58,26.401c-0.774-0.774-0.774-2.028,0-2.802l4.019-4.019	c0.774-0.774,2.028-0.774,2.802,0L23.42,34.599c0.774,0.774,0.774,2.028,0,2.802l-4.019,4.019	C18.627,42.193,17.373,42.193,16.599,41.42z"></path><linearGradient id="HoiJCu43QtshzIrYCxOfCb_VFaz7MkjAiu0_gr2" x1="-15.77" x2="26.403" y1="43.228" y2="43.228" gradientTransform="rotate(134.999 21.287 38.873)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2ac782"></stop><stop offset="1" stop-color="#21b876"></stop></linearGradient><path fill="url(#HoiJCu43QtshzIrYCxOfCb_VFaz7MkjAiu0_gr2)" d="M12.58,34.599L39.599,7.58c0.774-0.774,2.028-0.774,2.802,0l4.019,4.019	c0.774,0.774,0.774,2.028,0,2.802L19.401,41.42c-0.774,0.774-2.028,0.774-2.802,0l-4.019-4.019	C11.807,36.627,11.807,35.373,12.58,34.599z"></path>
</svg>
${text}
</span><br>`;

const botTemplate = (text) => `<span
class="inline-flex mt-1.5 items-center gap-x-2 rounded-full bg-purple-600/20 px-2.5 py-1 text-sm font-semibold leading-5 text-purple-400">
<span class="inline-block h-2 w-2 rounded-full bg-purple-400"></span>
${text}
</span><br>`;

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  console.log(message)
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
  }).then(res => {
    console.log(res)
    var eventSource = new EventSource("/stream");
    eventSource.addEventListener('func', (event) => {
      chatOutput.innerHTML += funcTemplate(event.data);
      chatOutput.scrollTop = chatOutput.scrollHeight;
    });
    eventSource.addEventListener('bot', (event) => {
      chatOutput.innerHTML += botTemplate(event.data);
      chatOutput.scrollTop = chatOutput.scrollHeight;
    });
    eventSource.addEventListener('close', (event) => {
      eventSource.close();
    });
  })

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