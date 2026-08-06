import  { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send } from 'lucide-react';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'model',
      text: "Hello! Welcome to Apex Tech Solutions. Are you looking to build a digital solution for your business, or are you a student looking for tech training?"
    }
  ]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    // alert("The button works! Code is running."); // <--- ADD THIS LINE TEMPORARILY
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    const updatedMessages = [...messages, { role: 'user', text: userMessage }];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      const formattedHistory = updatedMessages.map(msg => ({
        role: msg.role === 'model' ? 'model': 'user',
        text:msg.text
      }));
// Post to Express backend server route
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
             'Content-Type': 'application/json' ,
            //  'Accept': 'application/json'
        },
        body: JSON.stringify({ messageHistory: formattedHistory }),
      });

      const data = await response.json();

      if (data.text) {
        setMessages(prev => [...prev, { role: 'model', text: data.text }]);
      } else if(data.error) {
        setMessages(prev => [...prev, { role: 'model', text: `Backend Server Error: ${data.error}` }]);
      } else{
        setMessages(prev => [...prev, { role: 'model', text: "Error: Received empty response from server." }]);
      }
    } catch (error) {
      console.error("Network fetch pipeline failed:", error);
      setMessages(prev => [...prev, { role: 'model', text: "Cannot connect to server. Is your backend server running?" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-50 font-sans text-gray-800">
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg flex items-center justify-center cursor-pointer transition-transform transform hover:scale-105"
        >
          <MessageSquare className="h-6 w-6" />
        </button>
      )}

      {isOpen && (
        <div className="bg-white w-80 sm:w-96 h-[460px] rounded-2xl border border-gray-300 shadow-2xl flex flex-col overflow-hidden">
          <div className="bg-blue-600 text-white p-4 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-sm">ApexBot AI</h3>
              <p className="text-[10px] text-blue-200">Services & Internship Assistant</p>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-blue-700 p-1 rounded-full cursor-pointer">
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="flex-1 bg-gray-50 p-4 overflow-y-auto space-y-3">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div 
                  className={`max-w-[85%] rounded-2xl px-3 py-2 text-xs leading-relaxed shadow-xs whitespace-pre-line ${
                    msg.role === 'user' 
                      ? 'bg-blue-600 text-white rounded-br-none' 
                      : 'bg-white border border-gray-200 rounded-bl-none'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 text-gray-400 text-[11px] rounded-xl px-3 py-2 animate-pulse">
                  Bot is typing a response...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSendMessage} className="border-t border-gray-200 p-2 flex gap-2 bg-white">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 border border-gray-300 rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-blue-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-xl flex items-center justify-center disabled:bg-gray-200 disabled:text-gray-400 cursor-pointer transition-all"
            >
              <Send className="h-3.5 w-3.5" />
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
