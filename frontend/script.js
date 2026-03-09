// ---------------------------------------------------------------
// Multimodal AI Agent — frontend
//
// Talks to the FastAPI backend in app/api/router.py:
//   POST /health
//   POST /chat            { question }            -> ChatResponse
//   POST /chat/image       multipart(file, question) -> MultimodalChatResponse
//   POST /chat/audio       multipart(file, question) -> MultimodalChatResponse
//   POST /chat/video       multipart(file, question) -> MultimodalChatResponse
//
// The backend does not currently ship CORS middleware. If this page
// is served from a different origin/port than the API, add to
// app/main.py:
//
//   from fastapi.middleware.cors import CORSMiddleware
//   app.add_middleware(
//       CORSMiddleware,
//       allow_origins=["*"],       # tighten in production
//       allow_methods=["*"],
//       allow_headers=["*"],
//   )
// ---------------------------------------------------------------

const DEFAULT_API_BASE = "http://localhost:8000";

const state = {
  apiBase: localStorage.getItem("mma_api_base") || DEFAULT_API_BASE,
  chats: JSON.parse(localStorage.getItem("mma_chats") || "[]"), // [{id, title, messages}]
  activeChatId: null,
  pendingFile: null, // { file, kind }
  sending: false,
};

// ---------------- DOM refs ----------------

const el = {
  sidebar: document.getElementById("sidebar"),
  sidebarToggle: document.getElementById("sidebarToggle"),
  newChatBtn: document.getElementById("newChatBtn"),
  historyList: document.getElementById("historyList"),
  chatScroll: document.getElementById("chatScroll"),
  welcome: document.getElementById("welcome"),
  messages: document.getElementById("messages"),
  composerForm: document.getElementById("composerForm"),
  promptInput: document.getElementById("promptInput"),
  sendBtn: document.getElementById("sendBtn"),
  attachBtn: document.getElementById("attachBtn"),
  fileInput: document.getElementById("fileInput"),
  attachmentPreview: document.getElementById("attachmentPreview"),
  attachmentName: document.getElementById("attachmentName"),
  removeAttachment: document.getElementById("removeAttachment"),
  statusDot: document.getElementById("statusDot"),
  settingsBtn: document.getElementById("settingsBtn"),
  settingsModal: document.getElementById("settingsModal"),
  closeSettings: document.getElementById("closeSettings"),
  cancelSettings: document.getElementById("cancelSettings"),
  saveSettings: document.getElementById("saveSettings"),
  apiBaseInput: document.getElementById("apiBaseInput"),
  suggestionCards: document.querySelectorAll(".suggestion-card"),
};

// ---------------- Chat persistence ----------------

function persistChats() {
  localStorage.setItem("mma_chats", JSON.stringify(state.chats));
}

function getActiveChat() {
  return state.chats.find((c) => c.id === state.activeChatId) || null;
}

function createChat() {
  const chat = { id: crypto.randomUUID(), title: "New chat", messages: [] };
  state.chats.unshift(chat);
  state.activeChatId = chat.id;
  persistChats();
  renderHistory();
  renderMessages();
}

function selectChat(id) {
  state.activeChatId = id;
  renderHistory();
  renderMessages();
}

// ---------------- Rendering ----------------

function renderHistory() {
  el.historyList.querySelectorAll(".history-item").forEach((n) => n.remove());
  state.chats.forEach((chat) => {
    const btn = document.createElement("button");
    btn.className = "history-item" + (chat.id === state.activeChatId ? " active" : "");
    btn.textContent = chat.title || "New chat";
    btn.addEventListener("click", () => selectChat(chat.id));
    el.historyList.appendChild(btn);
  });
}

function renderMessages() {
  const chat = getActiveChat();
  el.messages.innerHTML = "";

  if (!chat || chat.messages.length === 0) {
    el.welcome.classList.remove("hidden");
    return;
  }
  el.welcome.classList.add("hidden");

  chat.messages.forEach((msg) => el.messages.appendChild(renderMessage(msg)));
  scrollToBottom();
}

function renderMessage(msg) {
  const wrap = document.createElement("div");
  wrap.className = `msg ${msg.role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = msg.role === "user" ? "U" : "AI";

  const body = document.createElement("div");
  body.className = "msg-body";

  const roleLabel = document.createElement("div");
  roleLabel.className = "msg-role";
  roleLabel.textContent = msg.role === "user" ? "You" : "Agent";
  body.appendChild(roleLabel);

  if (msg.attachmentName) {
    const chip = document.createElement("div");
    chip.className = "msg-attachment";
    chip.textContent = `📎 ${msg.attachmentName}`;
    body.appendChild(chip);
  }

  if (msg.pending) {
    const typing = document.createElement("div");
    typing.className = "typing";
    typing.innerHTML = "<span></span><span></span><span></span>";
    body.appendChild(typing);
  } else if (msg.error) {
    const errBox = document.createElement("div");
    errBox.className = "msg-error";
    errBox.textContent = msg.content;
    body.appendChild(errBox);
  } else {
    const content = document.createElement("div");
    content.className = "msg-content";
    content.textContent = msg.content;
    body.appendChild(content);

    if (msg.role === "assistant" && (msg.sources?.length || typeof msg.confidence === "number")) {
      const meta = document.createElement("div");
      meta.className = "msg-meta";

      if (typeof msg.confidence === "number") {
        const bar = document.createElement("div");
        bar.className = "confidence-bar";
        const pct = Math.round(msg.confidence * 100);
        bar.innerHTML = `
          <span>Confidence ${pct}%</span>
          <span class="confidence-track"><span class="confidence-fill" style="width:${pct}%"></span></span>
        `;
        meta.appendChild(bar);
      }

      if (msg.sources?.length) {
        const sources = document.createElement("div");
        sources.className = "sources";
        msg.sources.forEach((s) => {
          const chip = document.createElement("span");
          chip.className = "source-chip";
          const parts = [s.document];
          if (s.page != null) parts.push(`p.${s.page}`);
          if (s.section) parts.push(s.section);
          chip.textContent = parts.join(" · ");
          sources.appendChild(chip);
        });
        meta.appendChild(sources);
      }

      body.appendChild(meta);
    }
  }

  wrap.appendChild(avatar);
  wrap.appendChild(body);
  return wrap;
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    el.chatScroll.scrollTop = el.chatScroll.scrollHeight;
  });
}

// ---------------- Sending messages ----------------

function pickEndpointForFile(file) {
  if (file.type.startsWith("image/")) return { path: "/chat/image", kind: "image" };
  if (file.type.startsWith("audio/")) return { path: "/chat/audio", kind: "audio" };
  if (file.type.startsWith("video/")) return { path: "/chat/video", kind: "video" };
  return null;
}

async function sendMessage() {
  const question = el.promptInput.value.trim();
  const file = state.pendingFile;

  if (!question && !file) return;
  if (state.sending) return;

  let chat = getActiveChat();
  if (!chat) {
    chat = { id: crypto.randomUUID(), title: "New chat", messages: [] };
    state.chats.unshift(chat);
    state.activeChatId = chat.id;
  }

  if (chat.messages.length === 0) {
    chat.title = question ? question.slice(0, 40) : `${file.name}`;
  }

  const userMsg = {
    role: "user",
    content: question || `(no question — analyze the attached ${file.kind})`,
    attachmentName: file ? file.file.name : null,
  };
  chat.messages.push(userMsg);

  const pendingMsg = { role: "assistant", pending: true, content: "" };
  chat.messages.push(pendingMsg);

  persistChats();
  renderHistory();
  renderMessages();

  el.promptInput.value = "";
  autoResize();
  clearAttachment();
  state.sending = true;
  updateSendState();

  try {
    const data = file
      ? await callMultimodalEndpoint(file, question)
      : await callChatEndpoint(question);

    pendingMsg.pending = false;
    pendingMsg.content = data.answer;
    pendingMsg.sources = data.sources || [];
    pendingMsg.confidence = data.confidence;
    setStatus(true);
  } catch (err) {
    pendingMsg.pending = false;
    pendingMsg.error = true;
    pendingMsg.content = describeError(err);
    setStatus(false);
  }

  persistChats();
  renderMessages();
  state.sending = false;
  updateSendState();
}

async function callChatEndpoint(question) {
  const res = await fetch(`${state.apiBase}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handleResponse(res);
}

async function callMultimodalEndpoint(file, question) {
  const endpoint = pickEndpointForFile(file.file);
  if (!endpoint) throw new Error("Unsupported file type. Use an image, audio, or video file.");

  const formData = new FormData();
  formData.append("file", file.file);
  if (question) formData.append("question", question);

  const res = await fetch(`${state.apiBase}${endpoint.path}`, {
    method: "POST",
    body: formData,
  });
  return handleResponse(res);
}

async function handleResponse(res) {
  if (!res.ok) {
    let detail = `Request failed with status ${res.status}`;
    try {
      const body = await res.json();
      if (body.detail) detail = body.detail;
    } catch (_) {}
    throw new Error(detail);
  }
  return res.json();
}

function describeError(err) {
  if (err instanceof TypeError) {
    return `Couldn't reach the backend at ${state.apiBase}. Check that the server is running and CORS is enabled, then verify the API base URL in Settings.`;
  }
  return err.message || "Something went wrong.";
}

// ---------------- Attachment handling ----------------

function setAttachment(file) {
  const endpoint = pickEndpointForFile(file);
  if (!endpoint) {
    alert("Unsupported file type. Please attach an image, audio, or video file.");
    return;
  }
  state.pendingFile = { file, kind: endpoint.kind };
  el.attachmentName.textContent = file.name;
  el.attachmentPreview.classList.remove("hidden");
  updateSendState();
}

function clearAttachment() {
  state.pendingFile = null;
  el.fileInput.value = "";
  el.attachmentPreview.classList.add("hidden");
  updateSendState();
}

// ---------------- UI helpers ----------------

function updateSendState() {
  const hasContent = el.promptInput.value.trim().length > 0 || !!state.pendingFile;
  el.sendBtn.disabled = !hasContent || state.sending;
}

function autoResize() {
  el.promptInput.style.height = "auto";
  el.promptInput.style.height = Math.min(el.promptInput.scrollHeight, 200) + "px";
}

function setStatus(online) {
  el.statusDot.classList.remove("online", "offline");
  el.statusDot.classList.add(online ? "online" : "offline");
}

async function checkHealth() {
  try {
    const res = await fetch(`${state.apiBase}/health`);
    setStatus(res.ok);
  } catch (_) {
    setStatus(false);
  }
}

// ---------------- Event wiring ----------------

el.composerForm.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

el.promptInput.addEventListener("input", () => {
  autoResize();
  updateSendState();
});

el.promptInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

el.newChatBtn.addEventListener("click", createChat);

el.sidebarToggle.addEventListener("click", () => {
  el.sidebar.classList.toggle("collapsed");
});

el.attachBtn.addEventListener("click", () => el.fileInput.click());

el.fileInput.addEventListener("change", () => {
  if (el.fileInput.files[0]) setAttachment(el.fileInput.files[0]);
});

el.removeAttachment.addEventListener("click", clearAttachment);

el.suggestionCards.forEach((card) => {
  card.addEventListener("click", () => {
    el.promptInput.value = card.dataset.prompt;
    autoResize();
    updateSendState();
    el.promptInput.focus();
  });
});

// Settings modal

el.settingsBtn.addEventListener("click", () => {
  el.apiBaseInput.value = state.apiBase;
  el.settingsModal.classList.remove("hidden");
});

el.closeSettings.addEventListener("click", closeSettingsModal);
el.cancelSettings.addEventListener("click", closeSettingsModal);
el.settingsModal.addEventListener("click", (e) => {
  if (e.target === el.settingsModal) closeSettingsModal();
});

function closeSettingsModal() {
  el.settingsModal.classList.add("hidden");
}

el.saveSettings.addEventListener("click", () => {
  const value = el.apiBaseInput.value.trim().replace(/\/$/, "");
  if (value) {
    state.apiBase = value;
    localStorage.setItem("mma_api_base", value);
    checkHealth();
  }
  closeSettingsModal();
});

// ---------------- Init ----------------

function init() {
  if (state.chats.length > 0) {
    state.activeChatId = state.chats[0].id;
  } else {
    createChat();
  }
  renderHistory();
  renderMessages();
  updateSendState();
  checkHealth();
  setInterval(checkHealth, 30000);
}

init();
