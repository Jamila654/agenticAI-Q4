'use client';

import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState<{ user: string; bot?: string }[]>([]);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add only the user message
    const userMessage = { user: message };
    setChat((prev) => [...prev, userMessage]);

    try {
      const res = await fetch('https://prac-assignments-q4.vercel.app/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'test_user',
          text: message,
          metadata: null,
          tags: null,
        }),
      });
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();
      // Append only the bot response
      setChat((prev) => [...prev, { user: message, bot: data.reply }]);
    } catch (error) {
      console.error('Error:', error);
      // Append error message without duplicating user input
      setChat((prev) => [...prev, { user: message, bot: 'Error: Could not get response' }]);
    }
    setMessage('');
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chat]);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg border border-gray-200">
        <div className="bg-purple-100 p-3 rounded-t-xl flex items-center gap-2">
          <div className="w-8 h-8 bg-purple-300 rounded-full flex items-center justify-center">
            🤖
          </div>
          <h2 className="text-lg font-semibold text-gray-800">AI Chatbot</h2>
          <p className="ml-auto text-sm text-gray-500" suppressHydrationWarning={true}>
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
        <div
          ref={chatContainerRef}
          className="p-4 bg-purple-50 h-96 overflow-y-auto"
        >
          {chat.length === 0 && (
            <div className="text-center text-gray-500 py-4">
              Say hi to start the conversation!
            </div>
          )}
          {chat.map((msg, index) => (
            <div key={index} className="mb-4">
              {/* User Message */}
              {msg.user && !msg.bot && (
                <div className="flex justify-end">
                  <div className="bg-blue-100 text-gray-800 p-2 rounded-lg max-w-xs">
                    <p>{msg.user}</p>
                  </div>
                </div>
              )}
              {msg.bot && (
                <div className="flex flex-col items-start">
                  <div className="flex justify-start">
                    <div className="bg-purple-200 text-gray-800 p-2 mt-2 rounded-lg max-w-xs">
                      <p>{msg.bot}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
        <div className="p-4 bg-white rounded-b-xl border-t">
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1 p-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-300 placeholder-gray-400 text-black"
              placeholder="Write your message..."
            />
            <button
              onClick={sendMessage}
              className="bg-purple-500 text-white p-2 px-4 rounded-full hover:bg-purple-600 transition"
            >
              ➤
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            This is an AI-powered assistant. Responses are automated and may not
            always be accurate or complete. For definitive information, please
            contact support.
          </p>
        </div>
      </div>
    </div>
  );
}