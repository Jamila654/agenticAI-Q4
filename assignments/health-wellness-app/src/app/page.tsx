"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { sendMessage, checkHealth } from "@/lib/api"

interface Message {
  user_id: string
  reply: string
  timestamp: string
  isStreaming?: boolean
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [userId] = useState("user_" + Math.random().toString(36).substr(2, 9))
  const [userName, setUserName] = useState("")
  const [nameInput, setNameInput] = useState("")
  const [showNameInput, setShowNameInput] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const streamingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    checkHealth()
      .then(() => console.log("API is healthy"))
      .catch((err) => setError("API is unavailable"))
  }, [])

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])

  // Function to simulate streaming response word by word
  const streamResponse = (fullResponse: string, messageIndex: number) => {
    const words = fullResponse.split(' ')
    let currentWordIndex = 0
    
    const streamNextWord = () => {
      if (currentWordIndex < words.length) {
        const currentText = words.slice(0, currentWordIndex + 1).join(' ')
        
        setMessages(prev => 
          prev.map((msg, index) => 
            index === messageIndex 
              ? { ...msg, reply: currentText, isStreaming: true }
              : msg
          )
        )
        
        currentWordIndex++
        streamingTimeoutRef.current = setTimeout(streamNextWord, 50) // Adjust speed here (50ms per word)
      } else {
        // Streaming complete
        setMessages(prev => 
          prev.map((msg, index) => 
            index === messageIndex 
              ? { ...msg, isStreaming: false }
              : msg
          )
        )
      }
    }

    streamNextWord()
  }

  const handleNameSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const finalName = nameInput.trim() || "Guest"
    setUserName(finalName)
    setShowNameInput(false)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    setIsLoading(true)
    setError(null)

    // Clear any existing streaming timeout
    if (streamingTimeoutRef.current) {
      clearTimeout(streamingTimeoutRef.current)
    }

    try {
      const response = await sendMessage({
        user_id: userId,
        user_name: userName,
        message: input,
      })

      // Add message with empty reply initially
      const newMessage = { ...response, reply: "", isStreaming: true }
      setMessages(prev => [...prev, newMessage])
      
      // Start streaming the response
      const messageIndex = messages.length
      streamResponse(response.reply, messageIndex)
      
      setInput("")
    } catch (err: any) {
      setError(err.message || "Failed to send message")
    } finally {
      setIsLoading(false)
    }
  }

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (streamingTimeoutRef.current) {
        clearTimeout(streamingTimeoutRef.current)
      }
    }
  }, [])

  // Name Input Screen
  if (showNameInput) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-100 p-4 flex items-center justify-center">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8">
            {/* Welcome Header */}
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-3xl mb-6 shadow-lg">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
              </div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-teal-700 bg-clip-text text-transparent mb-3">
                Welcome to Health & Wellness Assistant
              </h1>
              <p className="text-slate-600 text-lg leading-relaxed">
                Your intelligent AI agent is ready to assist you with any questions or tasks.
              </p>
            </div>

            {/* Name Input Form */}
            <form onSubmit={handleNameSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-semibold text-slate-700 mb-3">
                  What should we call you?
                </label>
                <input
                  type="text"
                  id="name"
                  value={nameInput}
                  onChange={(e) => setNameInput(e.target.value)}
                  placeholder="Enter your name (optional)"
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-slate-800 placeholder-slate-400 transition-all duration-200"
                  autoFocus
                />
                <p className="text-xs text-slate-500 mt-2">Leave blank to continue as Guest</p>
              </div>

              <div className="space-y-3">
                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-3 px-6 rounded-2xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                  {nameInput.trim() ? `Continue as ${nameInput.trim()}` : "Continue as Guest"}
                </button>

                <div className="text-center">
                  <button
                    type="button"
                    onClick={() => {
                      setUserName("Guest")
                      setShowNameInput(false)
                    }}
                    className="text-slate-500 hover:text-slate-700 text-sm font-medium transition-colors duration-200"
                  >
                    Skip and continue as Guest
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-100 p-4 flex items-center justify-center">
      <div className="w-full max-w-5xl mx-auto h-[90vh] flex flex-col">
        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden h-full flex flex-col">

          {/* Header */}
          <div className="bg-gradient-to-r from-emerald-500 to-teal-600 px-6 py-4 flex-shrink-0">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-3 h-3 bg-green-300 rounded-full"></div>
                  <div className="absolute inset-0 w-3 h-3 bg-green-300 rounded-full animate-ping"></div>
                </div>
                <span className="text-white font-medium">Connected as {userName}</span>
                <button
                  onClick={() => setShowNameInput(true)}
                  className="text-emerald-100 hover:text-white text-sm underline transition-colors duration-200"
                >
                  Change name
                </button>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-emerald-100 text-sm">{messages.length} messages</div>
                <button
                  onClick={() => setMessages([])}
                  className="text-emerald-100 hover:text-white text-sm bg-white/10 hover:bg-white/20 px-3 py-1 rounded-full transition-all duration-200"
                >
                  Clear chat
                </button>
              </div>
            </div>
          </div>

          {/* Messages Container */}
          <div 
            ref={chatContainerRef}
            className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-slate-50/50 to-white/50 scroll-smooth"
          >
            {error && (
              <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-lg animate-slide-in">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </div>
            )}

            {messages.length === 0 && !error && (
              <div className="text-center py-12">
                <div className="w-20 h-20 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-slate-700 mb-2">Hello {userName}! 👋</h3>
                <p className="text-slate-500 mb-4">Ask me anything - I'm your AI agent ready to help!</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-md mx-auto">
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-emerald-100">
                    <p className="text-sm text-slate-600">💡 Try asking about health tips</p>
                  </div>
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-teal-100">
                    <p className="text-sm text-slate-600">🧘 Or wellness advice</p>
                  </div>
                </div>
              </div>
            )}

            {messages.map((msg, index) => (
              <div key={index} className="group animate-slide-in">
                <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:bg-white/80 transition-all duration-200">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full flex items-center justify-center shadow-sm">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                          />
                        </svg>
                      </div>
                      <div>
                        <span className="font-medium text-slate-700">AI Assistant</span>
                        <p className="text-xs text-slate-500">Health & Wellness Expert</p>
                      </div>
                      {msg.isStreaming && (
                        <div className="flex items-center space-x-1 ml-2">
                          <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce"></div>
                          <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce animate-delay-100" ></div>
                          <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce animate-delay-200"></div>
                        </div>
                      )}
                    </div>
                    <time className="text-xs text-slate-400 bg-slate-50 px-3 py-1 rounded-full">
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </time>
                  </div>
                  <div className="text-slate-800 leading-relaxed whitespace-pre-wrap">
                    {msg.reply}
                    {msg.isStreaming && <span className="inline-block w-2 h-5 bg-emerald-500 ml-1 animate-pulse"></span>}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex items-center space-x-3 p-4 animate-slide-in">
                <div className="flex space-x-1">
                  <div className="w-3 h-3 bg-emerald-400 rounded-full animate-bounce"></div>
                  <div className="w-3 h-3 bg-emerald-400 rounded-full animate-bounce animate-delay-100"></div>
                  <div className="w-3 h-3 bg-emerald-400 rounded-full animate-bounce animate-delay-200"></div>
                </div>
                <span className="text-slate-500 text-sm">AI Assistant is thinking...</span>
              </div>
            )}
            
            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-6 bg-white/90 backdrop-blur-sm border-t border-slate-100 flex-shrink-0">
            <form onSubmit={handleSubmit} className="flex items-end space-x-4">
              <div className="flex-1 relative">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={`Hi ${userName}, what can I help you with?`}
                  className="w-full h-auto px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none text-slate-800 placeholder-slate-400 transition-all duration-200 min-h-[48px] max-h-32"
                  rows={1}
                  disabled={isLoading}
                  // style={{
                  //   height: 'auto',
                  //   minHeight: '48px'
                  // }}
                  onInput={(e) => {
                    const target = e.target as HTMLTextAreaElement
                    target.style.height = 'auto'
                    target.style.height = target.scrollHeight + 'px'
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleSubmit(e)
                    }
                  }}
                />
              </div>
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 disabled:from-slate-300 disabled:to-slate-400 text-white p-3 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none group flex-shrink-0"
              >
                {isLoading ? (
                  <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  <svg
                    className="w-5 h-5 group-hover:translate-x-0.5 transition-transform duration-200"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                    />
                  </svg>
                )}
              </button>
            </form>
            <p className="text-xs text-slate-400 mt-2 text-center">Press Enter to send • Shift + Enter for new line</p>
          </div>
        </div>
      </div>
    </div>
  )
}