"use client"
import type React from "react"
import { useState, useEffect, useRef } from "react"
import { Send, Loader2 } from "lucide-react"

interface Message {
  id: string
  text: string 
  content: string // Bot's reply content
  isUser: boolean
  isStreaming: boolean // Only for type: "bot"
  timestamp: Date
  type: "user" | "bot" // Only user and bot messages displayed
}

export default function MathPythonChatbot() {
  const [userName, setUserName] = useState<string>("")
  const [tempName, setTempName] = useState<string>("")
  const [showNameModal, setShowNameModal] = useState(true)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])

  // Initialize chat after name is set
  useEffect(() => {
    if (userName && messages.length === 0) {
      setMessages([
        {
          id: "1",
          text: "",
          content: `Hello ${userName}! 👋 I'm your AI Math & Python Teacher. I can help you with complex numbers, algorithms, coding examples, and more. What would you like to learn today?`,
          isUser: false,
          isStreaming: false,
          timestamp: new Date(),
          type: "bot",
        },
      ])
    }
  }, [userName, messages.length])

  const handleNameSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (tempName.trim()) {
      setUserName(tempName.trim())
      setShowNameModal(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      content: "",
      isUser: true,
      isStreaming: false,
      timestamp: new Date(),
      type: "user",
    }

    setMessages((prev) => [...prev, userMessage])

    const currentInput = input
    setInput("")
    setIsLoading(true)

    const botMessageId = (Date.now() + 1).toString()
    setMessages((prev) => [
      ...prev,
      {
        id: botMessageId,
        text: "",
        content: "",
        isUser: false,
        isStreaming: true,
        timestamp: new Date(),
        type: "bot",
      },
    ])

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: currentInput,
          user_id: userName,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(`API Error: ${response.status} - ${errorData.error || "Unknown error"}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value, { stream: true })
          const lines = chunk.split("\n")

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                let jsonString = line
                while (jsonString.startsWith("data: ")) {
                  jsonString = jsonString.slice(6)
                }
                if (!jsonString.trim()) continue

                const data = JSON.parse(jsonString)

                if (data.chunk) {
                  setMessages((prev) =>
                    prev.map((msg) => (msg.id === botMessageId ? { ...msg, content: msg.content + data.chunk } : msg)),
                  )
                } else if (data.message_output) {
                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === botMessageId ? { ...msg, content: data.message_output, isStreaming: false } : msg,
                    ),
                  )
                }
                // All other data types (tool_called, tool_output, agent_updated, etc.) are ignored for display
              } catch (e) {
                console.error("Error parsing JSON chunk:", e, "Chunk:", line)
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Chat error:", error)
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === botMessageId
            ? {
                ...msg,
                content: `I'm having trouble connecting right now. Please try again in a moment.`,
                isStreaming: false,
              }
            : msg,
        ),
      )
    } finally {
      setIsLoading(false)
    }
  }

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  // Name Modal
  if (showNameModal) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 w-full max-w-md border border-gray-700">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-4xl font-bold">
              π
            </div>
            <h1 className="text-3xl font-bold text-gray-100 mb-2">Welcome, Student!</h1>
            <p className="text-gray-400">Your AI Math & Python Teacher is ready.</p>
          </div>
          <form onSubmit={handleNameSubmit} className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                What's your name?
              </label>
              <input
                type="text"
                id="name"
                value={tempName}
                onChange={(e) => setTempName(e.target.value)}
                placeholder="Enter your name"
                className="w-full px-4 py-3 border text-gray-100 bg-gray-700 border-gray-600 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-green-600 text-white py-3 px-6 rounded-md font-medium hover:bg-green-700 transition-all duration-200 shadow-md hover:shadow-lg"
            >
              Start Learning
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-gray-900 font-sans">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 shadow-sm py-4 px-6">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center text-white text-xl font-bold">
              π
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-100">Math & Python AI</h1>
              <p className="text-sm text-gray-400">Your Personal Teacher</p>
            </div>
          </div>
          <div className="text-sm text-gray-400">
            Hello,{" "}
            <span className="font-medium text-green-400">{userName.charAt(0).toUpperCase() + userName.slice(1)}</span>
          </div>
        </div>
      </header>

      {/* Messages Container */}
      <main className="flex-1 overflow-y-auto max-w-4xl mx-auto w-full px-6 py-6 pb-24">
        {" "}
        {/* pb-24 to account for fixed input */}
        <div className="space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[75%] ${message.isUser ? "order-2" : "order-1"}`}>
                <div
                  className={`rounded-lg px-4 py-3 shadow-sm ${
                    message.isUser
                      ? "bg-green-600 text-white ml-4"
                      : "bg-gray-700 border border-gray-600 mr-4 text-gray-100"
                  }`}
                >
                  {message.isUser ? (
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-medium opacity-90">
                          {userName.charAt(0).toUpperCase() + userName.slice(1)}
                        </span>
                      </div>
                      <p className="leading-relaxed">{message.text}</p>
                    </div>
                  ) : (
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-medium text-green-400">Teacher AI</span>
                        {message.isStreaming && (
                          <div className="flex gap-1">
                            <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-bounce"></div>
                            <div
                              className="w-1.5 h-1.5 bg-green-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.1s" }}
                            ></div>
                            <div
                              className="w-1.5 h-1.5 bg-green-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.2s" }}
                            ></div>
                          </div>
                        )}
                      </div>
                      <p className="whitespace-pre-wrap leading-relaxed text-gray-200">{message.content}</p>
                    </div>
                  )}
                </div>
                <div className={`text-xs text-gray-500 mt-1 ${message.isUser ? "text-right mr-4" : "ml-4"}`}>
                  {formatTimestamp(message.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>
        <div ref={messagesEndRef} />
      </main>

      {/* Input Form Container (Fixed at bottom) */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700 shadow-lg p-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me about math, Python, algorithms, or anything else..."
              className="flex-1 px-4 py-3 text-gray-100 bg-gray-700 border border-gray-600 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition-all"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-white p-3 rounded-md font-medium transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
