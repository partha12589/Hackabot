import { useState, useEffect, useRef } from 'react';
import './App.css';

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
    const errorData = await res.json();
    return Promise.reject({ status: res.status, data: errorData });
  }
  return res.body;
}

async function getSampleQueries() {
  const res = await fetch(`${API_URL}/sample-queries`);
  const data = await res.json();
  return data.queries || [];
}

// Spinner Component
function Spinner() {
  return (
    <div className="flex space-x-2">
      <div className="w-3 h-3 bg-green-400 rounded-full animate-bounce shadow-lg"></div>
      <div className="w-3 h-3 bg-green-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '150ms' }}></div>
      <div className="w-3 h-3 bg-green-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '300ms' }}></div>
    </div>
  );
}

// Typing indicator
function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 text-green-400 animate-pulse">
      <Spinner />
      <span className="text-sm font-medium">FinanceGPT is thinking...</span>
    </div>
  );
}

// ChatMessages Component
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
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-600 to-green-800 flex items-center justify-center text-white font-bold shadow-lg">
                💼
              </div>
            </div>
          )}
          
          <div className={`max-w-[75%] rounded-2xl p-5 transform transition-all duration-500 hover:scale-105 ${
            role === 'user' 
              ? 'finance-message-user shadow-2xl animate-shimmer' 
              : 'finance-message-assistant hover:border-green-500 shadow-2xl'
          }`}>
            {loading && !content ? (
              <TypingIndicator />
            ) : (
              <div className="whitespace-pre-wrap leading-relaxed animate-fadeIn text-base">{content}</div>
            )}
            {error && (
              <div className="mt-3 text-red-400 text-sm flex items-center gap-2 bg-red-900 bg-opacity-30 p-3 rounded-lg border-2 border-red-800">
                <span className="text-lg">❌</span>
                <span className="font-medium">{content || "Error: Please ask a finance-related question"}</span>
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

// ChatInput Component
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
          <div className={`absolute inset-0 bg-gradient-to-r from-green-600 to-green-800 rounded-2xl blur-xl transition-opacity duration-500 ${isFocused ? 'opacity-40' : 'opacity-0'}`}></div>
          <textarea
            ref={textareaRef}
            rows="1"
            value={newMessage}
            onChange={e => setNewMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Ask about investments, loans, taxes... 💰"
            style={{ maxHeight: '200px' }}
            className={`relative w-full resize-none bg-gray-800 border-2 text-gray-100 text-base placeholder-gray-400 rounded-2xl px-5 py-4 focus:outline-none transition-all duration-500 ${
              isFocused 
                ? 'border-green-500 ring-4 ring-green-500 ring-opacity-30 shadow-2xl scale-105' 
                : 'border-gray-700 hover:border-gray-600'
            }`}
            disabled={isLoading}
          />
        </div>
        <button
          onClick={submitNewMessage}
          disabled={isLoading || !newMessage.trim()}
          className="finance-button relative px-8 py-4 text-white text-base font-bold rounded-2xl disabled:from-gray-700 disabled:to-gray-800 disabled:cursor-not-allowed transition-all duration-500 shadow-2xl hover:scale-110 active:scale-95 disabled:scale-100 group overflow-hidden min-w-32"
        >
          <span className={`relative z-10 flex items-center justify-center gap-2 ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-300`}>
            <span>Send</span>
            <span className="text-xl">📊</span>
          </span>
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <Spinner />
            </div>
          )}
        </button>
      </div>
      
      <div className="text-center mt-4 text-gray-500 text-xs animate-fadeIn">
        ⚠️ <strong>Disclaimer:</strong> This is an AI assistant for educational purposes. Always consult a certified financial advisor.
      </div>
    </div>
  );
}

// Sample Query Chip Component
function SampleQueryChip({ query, onClick }) {
  return (
    <button
      onClick={() => onClick(query)}
      className="finance-card bg-gray-800 hover:bg-gray-700 text-gray-200 px-4 py-3 rounded-xl border-2 transition-all duration-300 hover:scale-105 text-sm font-medium shadow-lg hover:shadow-xl"
    >
      {query}
    </button>
  );
}

// Welcome Card Component
function WelcomeCard({ icon, title, description, delay }) {
  return (
    <div 
      className="finance-card relative bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6 rounded-2xl shadow-xl border-2 transition-all duration-700 hover:scale-110 cursor-pointer group overflow-hidden animate-slideInFromBottom"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-green-600 to-green-800 opacity-0 group-hover:opacity-10 transition-all duration-700"></div>
      
      <div className="relative z-10">
        <div className="font-bold finance-accent mb-3 transition-colors duration-500 flex items-center gap-3 text-lg">
          <span className="text-3xl group-hover:scale-125 transition-all duration-500 inline-block">{icon}</span>
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
  const [sampleQueries, setSampleQueries] = useState([]);

  const isLoading = messages.length && messages[messages.length - 1].loading;

  useEffect(() => {
    getSampleQueries().then(queries => {
      setSampleQueries(queries.slice(0, 4));
    }).catch(console.error);
  }, []);

  function handleSampleClick(query) {
    setNewMessage(query);
  }

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
      let errorMessage = "An error occurred";
      
      if (err.data?.detail?.message) {
        errorMessage = err.data.detail.message;
      } else if (err.data?.detail) {
        errorMessage = err.data.detail;
      }
      
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: errorMessage,
          loading: false,
          error: true
        };
        return updated;
      });
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-950 overflow-hidden">
      {/* Header */}
      <div className="finance-header relative text-white p-8 shadow-2xl border-b-4 border-green-700 backdrop-blur-sm animate-fadeIn overflow-hidden">
        <div className="absolute inset-0 animate-gradient opacity-20"></div>
        
        <div className="relative z-10 max-w-4xl mx-auto">
          <h1 className="text-5xl font-black flex items-center gap-4 hover:scale-105 transition-transform duration-500">
            <span className="text-6xl animate-float drop-shadow-lg">💼</span>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-green-200 to-white">
              FinanceGPT
            </span>
          </h1>
          <p className="text-green-200 mt-3 text-xl font-semibold">
            Your AI Financial Assistant powered by Ollama Phi3 ✨
          </p>
        </div>
      </div>

      {/* Welcome Message */}
      {messages.length === 0 && (
        <div className="flex-1 flex items-center justify-center p-8 bg-gray-950 overflow-y-auto">
          <div className="text-center max-w-3xl">
            <div className="text-8xl mb-6 animate-float hover:scale-125 transition-transform duration-500 cursor-pointer">
              💰
            </div>
            <h2 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-300 to-green-400 mb-6 animate-slideInFromBottom">
              Welcome to FinanceGPT
            </h2>
            <p className="text-gray-300 text-xl mb-8 leading-relaxed font-medium">
              I specialize in financial advice and can help you with investments, loans, taxes, budgeting, and more!
            </p>

            {/* Sample Queries */}
            {sampleQueries.length > 0 && (
              <div className="mb-12">
                <p className="text-gray-400 mb-4 text-lg">💡 Try asking:</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {sampleQueries.map((query, idx) => (
                    <SampleQueryChip 
                      key={idx} 
                      query={query} 
                      onClick={handleSampleClick}
                    />
                  ))}
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
              <WelcomeCard 
                icon="📊"
                title="Investment Strategies"
                description="Get guidance on stocks, mutual funds, bonds, and ETFs"
                delay={300}
              />
              <WelcomeCard 
                icon="💳"
                title="Banking & Loans"
                description="Learn about EMI, interest rates, mortgages, and credit"
                delay={400}
              />
              <WelcomeCard 
                icon="🧾"
                title="Tax Planning"
                description="Understand tax savings, deductions, and filing strategies"
                delay={500}
              />
              <WelcomeCard 
                icon="🎯"
                title="Retirement Planning"
                description="Plan your future with pension, PF, and retirement accounts"
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