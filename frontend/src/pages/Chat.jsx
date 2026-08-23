import { useEffect, useRef, useState } from "react";
import { getChatHistory, sendChatMessage } from "../services/api";
import { Spinner, EmptyState, ErrorBanner } from "../components/Feedback";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [historyError, setHistoryError] = useState(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoadingHistory(true);
      setHistoryError(null);
      try {
        const history = await getChatHistory();
        if (!cancelled) setMessages(history || []);
      } catch (err) {
        if (!cancelled) setHistoryError(err?.message || "Could not load chat history.");
      } finally {
        if (!cancelled) setLoadingHistory(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  async function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;

    setSendError(null);
    setSending(true);

    // Optimistically show the user's message.
    const optimisticUserMessage = {
      id: `local-${Date.now()}`,
      role: "user",
      content: text,
    };
    setMessages((prev) => [...prev, optimisticUserMessage]);
    setInput("");

    try {
      const { response } = await sendChatMessage(text);
      setMessages((prev) => [
        ...prev,
        { id: `local-reply-${Date.now()}`, role: "assistant", content: response },
      ]);
    } catch (err) {
      setSendError(err?.message || "Could not send your message. Please try again.");
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="page page-chat">
      <header className="page-header">
        <h1>AI Chat</h1>
        <p className="page-subtitle">Ask the health assistant a question.</p>
      </header>

      <div className="chat-window">
        <div className="chat-messages">
          <ErrorBanner message={historyError} />
          {loadingHistory ? (
            <Spinner label="Loading conversation..." />
          ) : messages.length === 0 ? (
            <EmptyState message="No messages yet. Say hello to get started." />
          ) : (
            messages.map((msg) => (
              <div key={msg.id} className={`chat-bubble chat-bubble-${msg.role}`}>
                <div className="chat-bubble-role">{msg.role === "user" ? "You" : "Assistant"}</div>
                <div className="chat-bubble-content">{msg.content}</div>
              </div>
            ))
          )}
          {sending && (
            <div className="chat-bubble chat-bubble-assistant">
              <div className="chat-bubble-role">Assistant</div>
              <div className="chat-bubble-content">
                <Spinner label="Thinking..." />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <ErrorBanner message={sendError} />

        <form className="chat-input-row" onSubmit={handleSend}>
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={sending}
          />
          <button className="btn btn-primary" type="submit" disabled={sending || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
