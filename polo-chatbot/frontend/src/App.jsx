import { useState, useEffect, useRef } from 'react';

// Utility function to parse SSE stream
async function* parseSSEStream(stream) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        yield line.slice(6);
      }
    }
  }
}

// API functions
const API_URL = 'http://localhost:8000';

async function createChat() {
  const res = await fetch(`${API_URL}/chats`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await res.json();
  if (!res.ok) {
    return Promise.reject({ status: res.status, data });
  }
  return data;
}

async function sendChatMessage(chatId, message) {
  const res = await fetch(`${API_URL}/chats/${chatId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  if (!res.ok) {
    return Promise.reject({ status: res.status, data: await res.json() });
  }
  return res.body;
}

// Spinner Component with enhanced animation
function Spinner() {
  return (
    <div className="flex space-x-2">
      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce shadow-lg shadow-purple-500"></div>
      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce shadow-lg shadow-purple-500" style={{ animationDelay: '150ms' }}></div>
      <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce shadow-lg shadow-purple-500" style={{ animationDelay: '300ms' }}></div>
    </div>
  );
}

// Typing indicator for assistant
function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 text-purple-400 animate-pulse">
      <Spinner />
      <span className="text-sm font-medium">Polo is typing...</span>
    </div>
  );
}

// ChatMessages Component with enhanced animations
function ChatMessages({ messages, isLoading }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-950">
      {messages.map(({ role, content, loading, error }, idx) => (
        <div 
          key={idx} 
          className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'} animate-slideInFromBottom`}
          style={{ animationDelay: `${idx * 80}ms` }}
        >
          {role === 'assistant' && (
            <div className="mr-3 mt-1 animate-fadeIn flex-shrink-0">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center text-white font-bold shadow-lg animate-pulse-slow">
                🎯
              </div>
            </div>
          )}
          
          <div className={`max-w-[75%] rounded-2xl p-5 transform transition-all duration-500 hover:scale-105 ${
            role === 'user' 
              ? 'bg-gradient-to-br from-purple-600 via-purple-700 to-purple-800 text-white shadow-2xl shadow-purple-900 animate-shimmer' 
              : 'bg-gradient-to-br from-gray-800 to-gray-900 text-gray-100 border-2 border-gray-700 hover:border-purple-500 shadow-2xl hover:shadow-purple-900'
          }`}>
            {loading && !content ? (
              <TypingIndicator />
            ) : (
              <div className="whitespace-pre-wrap leading-relaxed animate-fadeIn text-base">{content}</div>
            )}
            {error && (
              <div className="mt-3 text-red-400 text-sm flex items-center gap-2 animate-shake bg-red-900 bg-opacity-30 p-3 rounded-lg border-2 border-red-800">
                <span className="text-lg animate-pulse">⚠️</span>
                <span className="font-medium">Error generating response</span>
              </div>
            )}
          </div>

          {role === 'user' && (
            <div className="ml-3 mt-1 animate-fadeIn flex-shrink-0">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold shadow-lg">
                👤
              </div>
            </div>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

// ChatInput Component with enhanced animations
function ChatInput({ newMessage, isLoading, setNewMessage, submitNewMessage }) {
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef(null);

  function handleKeyDown(e) {
    if (e.keyCode === 13 && !e.shiftKey && !isLoading) {
      e.preventDefault();
      submitNewMessage();
    }
  }

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [newMessage]);

  return (
    <div className="border-t-2 border-gray-800 p-6 bg-gradient-to-b from-gray-900 to-gray-950 backdrop-blur-lg shadow-2xl">
      <div className="flex gap-4 max-w-4xl mx-auto items-end">
        <div className="flex-1 relative group">
          <div className={`absolute inset-0 bg-gradient-to-r from-purple-600 to-purple-800 rounded-2xl blur-xl transition-opacity duration-500 ${isFocused ? 'opacity-40' : 'opacity-0'}`}></div>
          <textarea
            ref={textareaRef}
            rows="1"
            value={newMessage}
            onChange={e => setNewMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Ask Polo anything... ✨"
            style={{ maxHeight: '200px' }}
            className={`relative w-full resize-none bg-gray-800 border-2 text-gray-100 text-base placeholder-gray-400 rounded-2xl px-5 py-4 focus:outline-none transition-all duration-500 ${
              isFocused 
                ? 'border-purple-500 ring-4 ring-purple-500 ring-opacity-30 shadow-2xl shadow-purple-900 scale-105' 
                : 'border-gray-700 hover:border-gray-600 hover:shadow-lg'
            }`}
            disabled={isLoading}
          />
        </div>
        <button
          onClick={submitNewMessage}
          disabled={isLoading || !newMessage.trim()}
          className="relative px-8 py-4 bg-gradient-to-r from-purple-600 via-purple-700 to-purple-800 text-white text-base font-bold rounded-2xl hover:from-purple-700 hover:via-purple-800 hover:to-purple-900 disabled:from-gray-700 disabled:to-gray-800 disabled:cursor-not-allowed transition-all duration-500 shadow-2xl hover:shadow-purple-900 hover:scale-110 active:scale-95 disabled:scale-100 group overflow-hidden min-w-32"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 opacity-0 group-hover:opacity-20 transition-opacity duration-500 animate-gradient"></div>
          <span className={`relative z-10 flex items-center justify-center gap-2 ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-300`}>
            <span>Send</span>
            <span className="group-hover:translate-x-1 transition-transform duration-300 text-xl">🚀</span>
          </span>
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <Spinner />
            </div>
          )}
        </button>
      </div>
      
      <div className="text-center mt-4 text-gray-500 text-xs animate-fadeIn">
        Press <kbd className="px-2 py-1 bg-gray-800 rounded border border-gray-700 text-gray-400 font-mono">Enter</kbd> to send, <kbd className="px-2 py-1 bg-gray-800 rounded border border-gray-700 text-gray-400 font-mono">Shift + Enter</kbd> for new line
      </div>
    </div>
  );
}

// Welcome Card Component with enhanced hover effects
function WelcomeCard({ icon, title, description, delay }) {
  return (
    <div 
      className="relative bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6 rounded-2xl shadow-xl border-2 border-gray-700 hover:border-purple-500 transition-all duration-700 hover:scale-110 hover:shadow-2xl hover:shadow-purple-900 cursor-pointer group overflow-hidden animate-slideInFromBottom"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600 from-0% to-purple-800 to-100% opacity-0 group-hover:opacity-10 transition-all duration-700"></div>
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
        <div className="absolute top-0 right-0 w-20 h-20 bg-purple-600 bg-opacity-30 rounded-full blur-2xl animate-pulse-slow"></div>
        <div className="absolute bottom-0 left-0 w-20 h-20 bg-purple-800 bg-opacity-30 rounded-full blur-2xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
      </div>
      
      <div className="relative z-10">
        <div className="font-bold text-purple-400 mb-3 group-hover:text-purple-300 transition-colors duration-500 flex items-center gap-3 text-lg">
          <span className="text-3xl group-hover:scale-125 group-hover:rotate-12 transition-all duration-500 inline-block">{icon}</span>
          <span className="group-hover:translate-x-1 transition-transform duration-500">{title}</span>
        </div>
        <div className="text-gray-400 text-base group-hover:text-gray-200 transition-colors duration-500 leading-relaxed">
          {description}
        </div>
      </div>
    </div>
  );
}

// Main Chatbot Component
function Chatbot() {
  const [chatId, setChatId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages(prev => [
      ...prev,
      { role: 'user', content: trimmedMessage },
      { role: 'assistant', content: '', loading: true }
    ]);
    setNewMessage('');

    let chatIdOrNew = chatId;
    try {
      if (!chatId) {
        const { id } = await createChat();
        setChatId(id);
        chatIdOrNew = id;
      }

      const stream = await sendChatMessage(chatIdOrNew, trimmedMessage);
      for await (const textChunk of parseSSEStream(stream)) {
        setMessages(prev => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: updated[updated.length - 1].content + textChunk
          };
          return updated;
        });
      }
      
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          loading: false
        };
        return updated;
      });
    } catch (err) {
      console.error(err);
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          loading: false,
          error: true
        };
        return updated;
      });
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-950 overflow-hidden">
      <style>{`
        @keyframes slideInFromBottom {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes shimmer {
          0% { background-position: -100% 0; }
          100% { background-position: 200% 0; }
        }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        @keyframes pulse-slow {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        @keyframes gradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
        .animate-slideInFromBottom {
          animation: slideInFromBottom 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out;
        }
        .animate-shimmer {
          background-size: 200% 100%;
          animation: shimmer 3s ease-in-out infinite;
        }
        .animate-shake {
          animation: shake 0.5s ease-in-out;
        }
        .animate-pulse-slow {
          animation: pulse-slow 3s ease-in-out infinite;
        }
        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }
        .animate-float {
          animation: float 3s ease-in-out infinite;
        }
      `}</style>

      {/* Header with enhanced gradient and glow */}
      <div className="relative bg-gradient-to-r from-purple-900 via-purple-800 to-purple-900 text-white p-8 shadow-2xl border-b-4 border-purple-700 backdrop-blur-sm animate-fadeIn overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 opacity-20 animate-gradient"></div>
        <div className="absolute top-0 left-1/4 w-40 h-40 bg-purple-500 opacity-30 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-0 right-1/4 w-40 h-40 bg-purple-700 opacity-30 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1.5s' }}></div>
        
        <div className="relative z-10 max-w-4xl mx-auto">
          <h1 className="text-5xl font-black flex items-center gap-4 hover:scale-105 transition-transform duration-500">
            <span className="text-6xl animate-float drop-shadow-lg">🎯</span>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-purple-200 to-white bg-[length:200%_100%] animate-shimmer">
              Polo
            </span>
          </h1>
          <p className="text-purple-200 mt-3 text-xl font-semibold animate-slideInFromBottom" style={{ animationDelay: '200ms' }}>
            Your AI Assistant powered by Ollama Phi3 ✨
          </p>
        </div>
      </div>

      {/* Welcome Message with enhanced staggered animations */}
      {messages.length === 0 && (
        <div className="flex-1 flex items-center justify-center p-8 bg-gray-950 overflow-y-auto">
          <div className="text-center max-w-3xl">
            <div className="text-8xl mb-6 animate-float hover:scale-125 transition-transform duration-500 cursor-pointer drop-shadow-2xl">
              👋
            </div>
            <h2 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-purple-300 to-purple-400 mb-6 animate-slideInFromBottom" style={{ animationDelay: '100ms' }}>
              Hello! I'm Polo
            </h2>
            <p className="text-gray-300 text-xl mb-12 leading-relaxed animate-slideInFromBottom font-medium" style={{ animationDelay: '200ms' }}>
              Your intelligent AI assistant. Ask me anything - from answering questions to helping with tasks!
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
              <WelcomeCard 
                icon="💡"
                title="Ask Questions"
                description="Get intelligent answers on any topic you're curious about"
                delay={300}
              />
              <WelcomeCard 
                icon="🔍"
                title="Get Information"
                description="Discover and learn about anything instantly"
                delay={400}
              />
              <WelcomeCard 
                icon="✍️"
                title="Create Content"
                description="Write, brainstorm, and bring your ideas to life"
                delay={500}
              />
              <WelcomeCard 
                icon="🤝"
                title="Problem Solving"
                description="Get expert help with any challenges you face"
                delay={600}
              />
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      {messages.length > 0 && (
        <ChatMessages messages={messages} isLoading={isLoading} />
      )}

      {/* Input */}
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;