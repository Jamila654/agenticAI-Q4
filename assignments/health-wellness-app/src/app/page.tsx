// "use client"

// import type React from "react"

// import { useState, useEffect, useRef } from "react"
// import { sendMessage, checkHealth } from "@/lib/api"

// interface Message {
//   user_id: string
//   reply: string
//   timestamp: string
//   isStreaming?: boolean
// }

// export default function Chat() {
//   const [messages, setMessages] = useState<Message[]>([])
//   const [input, setInput] = useState("")
//   const [userId] = useState("user_" + Math.random().toString(36).substr(2, 9))
//   const [userName, setUserName] = useState("")
//   const [nameInput, setNameInput] = useState("")
//   const [showNameInput, setShowNameInput] = useState(true)
//   const [isLoading, setIsLoading] = useState(false)
//   const [error, setError] = useState<string | null>(null)
//   const messagesEndRef = useRef<HTMLDivElement>(null)
//   const chatContainerRef = useRef<HTMLDivElement>(null)
//   const streamingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

//   useEffect(() => {
//     checkHealth()
//       .then(() => console.log("API is healthy"))
//       .catch((err) => setError("API is unavailable"))
//   }, [])

//   // Auto-scroll to bottom when messages change
//   useEffect(() => {
//     if (messagesEndRef.current) {
//       messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
//     }
//   }, [messages])

//   // Function to simulate streaming response word by word
//   const streamResponse = (fullResponse: string, messageIndex: number) => {
//     const words = fullResponse.split(' ')
//     let currentWordIndex = 0
    
//     const streamNextWord = () => {
//       if (currentWordIndex < words.length) {
//         const currentText = words.slice(0, currentWordIndex + 1).join(' ')
        
//         setMessages(prev => 
//           prev.map((msg, index) => 
//             index === messageIndex 
//               ? { ...msg, reply: currentText, isStreaming: true }
//               : msg
//           )
//         )
        
//         currentWordIndex++
//         streamingTimeoutRef.current = setTimeout(streamNextWord, 50) // Adjust speed here (50ms per word)
//       } else {
//         // Streaming complete
//         setMessages(prev => 
//           prev.map((msg, index) => 
//             index === messageIndex 
//               ? { ...msg, isStreaming: false }
//               : msg
//           )
//         )
//       }
//     }

//     streamNextWord()
//   }

//   const handleNameSubmit = (e: React.FormEvent) => {
//     e.preventDefault()
//     const finalName = nameInput.trim() || "Guest"
//     setUserName(finalName)
//     setShowNameInput(false)
//   }

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault()
//     if (!input.trim()) return

//     setIsLoading(true)
//     setError(null)

//     // Clear any existing streaming timeout
//     if (streamingTimeoutRef.current) {
//       clearTimeout(streamingTimeoutRef.current)
//     }

//     try {
//       const response = await sendMessage({
//         user_id: userId,
//         user_name: userName,
//         message: input,
//       })

//       // Add message with empty reply initially
//       const newMessage = { ...response, reply: "", isStreaming: true }
//       setMessages(prev => [...prev, newMessage])
      
//       // Start streaming the response
//       const messageIndex = messages.length
//       streamResponse(response.reply, messageIndex)
      
//       setInput("")
//     } catch (err: any) {
//       setError(err.message || "Failed to send message")
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   // Cleanup timeout on unmount
//   useEffect(() => {
//     return () => {
//       if (streamingTimeoutRef.current) {
//         clearTimeout(streamingTimeoutRef.current)
//       }
//     }
//   }, [])

//   // Name Input Screen
//   if (showNameInput) {
//     return (
//       <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-100 p-4 flex items-center justify-center">
//         <div className="w-full max-w-md mx-auto">
//           <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8">
//             {/* Welcome Header */}
//             <div className="text-center mb-8">
//               <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-3xl mb-6 shadow-lg">
//                 <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                   <path
//                     strokeLinecap="round"
//                     strokeLinejoin="round"
//                     strokeWidth={2}
//                     d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
//                   />
//                 </svg>
//               </div>
//               <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-teal-700 bg-clip-text text-transparent mb-3">
//                 Welcome to Health & Wellness Assistant
//               </h1>
//               <p className="text-slate-600 text-lg leading-relaxed">
//                 Your intelligent AI agent is ready to assist you with any questions or tasks.
//               </p>
//             </div>

//             {/* Name Input Form */}
//             <form onSubmit={handleNameSubmit} className="space-y-6">
//               <div>
//                 <label htmlFor="name" className="block text-sm font-semibold text-slate-700 mb-3">
//                   What should we call you?
//                 </label>
//                 <input
//                   type="text"
//                   id="name"
//                   value={nameInput}
//                   onChange={(e) => setNameInput(e.target.value)}
//                   placeholder="Enter your name (optional)"
//                   className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-slate-800 placeholder-slate-400 transition-all duration-200"
//                   autoFocus
//                 />
//                 <p className="text-xs text-slate-500 mt-2">Leave blank to continue as Guest</p>
//               </div>

//               <div className="space-y-3">
//                 <button
//                   type="submit"
//                   className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-3 px-6 rounded-2xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
//                 >
//                   {nameInput.trim() ? `Continue as ${nameInput.trim()}` : "Continue as Guest"}
//                 </button>

//                 <div className="text-center">
//                   <button
//                     type="button"
//                     onClick={() => {
//                       setUserName("Guest")
//                       setShowNameInput(false)
//                     }}
//                     className="text-slate-500 hover:text-slate-700 text-sm font-medium transition-colors duration-200"
//                   >
//                     Skip and continue as Guest
//                   </button>
//                 </div>
//               </div>
//             </form>
//           </div>
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-100 p-4 flex items-center justify-center">
//       <div className="w-full max-w-5xl mx-auto h-[90vh] flex flex-col">
//         <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden h-full flex flex-col">

//           {/* Header */}
//           <div className="bg-gradient-to-r from-emerald-500 to-teal-600 px-6 py-4 flex-shrink-0">
//             <div className="flex items-center justify-between">
//               <div className="flex items-center space-x-3">
//                 <div className="relative">
//                   <div className="w-3 h-3 bg-green-300 rounded-full"></div>
//                   <div className="absolute inset-0 w-3 h-3 bg-green-300 rounded-full animate-ping"></div>
//                 </div>
//                 <span className="text-white font-medium">Connected as {userName}</span>
//                 <button
//                   onClick={() => setShowNameInput(true)}
//                   className="text-emerald-100 hover:text-white text-sm underline transition-colors duration-200"
//                 >
//                   Change name
//                 </button>
//               </div>
//               <div className="flex items-center space-x-4">
//                 <div className="text-emerald-100 text-sm">{messages.length} messages</div>
//                 <button
//                   onClick={() => setMessages([])}
//                   className="text-emerald-100 hover:text-white text-sm bg-white/10 hover:bg-white/20 px-3 py-1 rounded-full transition-all duration-200"
//                 >
//                   Clear chat
//                 </button>
//               </div>
//             </div>
//           </div>

//           {/* Messages Container */}
//           <div 
//             ref={chatContainerRef}
//             className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-slate-50/50 to-white/50 scroll-smooth"
//           >
//             {error && (
//               <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-lg animate-slide-in">
//                 <div className="flex items-center">
//                   <svg className="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
//                     <path
//                       fillRule="evenodd"
//                       d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
//                       clipRule="evenodd"
//                     />
//                   </svg>
//                   <p className="text-red-700 font-medium">{error}</p>
//                 </div>
//               </div>
//             )}

//             {messages.length === 0 && !error && (
//               <div className="text-center py-12">
//                 <div className="w-20 h-20 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
//                   <svg className="w-10 h-10 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                     <path
//                       strokeLinecap="round"
//                       strokeLinejoin="round"
//                       strokeWidth={2}
//                       d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
//                     />
//                   </svg>
//                 </div>
//                 <h3 className="text-xl font-semibold text-slate-700 mb-2">Hello {userName}! 👋</h3>
//                 <p className="text-slate-500 mb-4">Ask me anything - I'm your AI agent ready to help!</p>
//                 <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-md mx-auto">
//                   <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-emerald-100">
//                     <p className="text-sm text-slate-600">💡 Try asking about health tips</p>
//                   </div>
//                   <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-teal-100">
//                     <p className="text-sm text-slate-600">🧘 Or wellness advice</p>
//                   </div>
//                 </div>
//               </div>
//             )}

//             {messages.map((msg, index) => (
//               <div key={index} className="group animate-slide-in">
//                 <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:bg-white/80 transition-all duration-200">
//                   <div className="flex items-start justify-between mb-3">
//                     <div className="flex items-center space-x-3">
//                       <div className="w-8 h-8 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full flex items-center justify-center shadow-sm">
//                         <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                           <path
//                             strokeLinecap="round"
//                             strokeLinejoin="round"
//                             strokeWidth={2}
//                             d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
//                           />
//                         </svg>
//                       </div>
//                       <div>
//                         <span className="font-medium text-slate-700">AI Assistant</span>
//                         <p className="text-xs text-slate-500">Health & Wellness Expert</p>
//                       </div>
//                       {msg.isStreaming && (
//                         <div className="flex items-center space-x-1 ml-2">
//                           <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce"></div>
//                           <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce animate-delay-100" ></div>
//                           <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce animate-delay-200"></div>
//                         </div>
//                       )}
//                     </div>
//                     <time className="text-xs text-slate-400 bg-slate-50 px-3 py-1 rounded-full">
//                       {new Date(msg.timestamp).toLocaleTimeString()}
//                     </time>
//                   </div>
//                   <div className="text-slate-800 leading-relaxed whitespace-pre-wrap">
//                     {msg.reply}
//                     {msg.isStreaming && <span className="inline-block w-2 h-5 bg-emerald-500 ml-1 animate-pulse"></span>}
//                   </div>
//                 </div>
//               </div>
//             ))}

//             {isLoading && (
//               <div className="flex items-center space-x-3 p-4 animate-slide-in">
//                 <div className="flex space-x-1">
//                   <div className="w-3 h-3 bg-emerald-400 rounded-full animate-bounce"></div>
//                   <div className="w-3 h-3 bg-emerald-400 rounded-full animate-bounce animate-delay-100"></div>
//                   <div className="w-3 h-3 bg-emerald-400 rounded-full animate-bounce animate-delay-200"></div>
//                 </div>
//                 <span className="text-slate-500 text-sm">AI Assistant is thinking...</span>
//               </div>
//             )}
            
//             {/* Scroll anchor */}
//             <div ref={messagesEndRef} />
//           </div>

//           {/* Input Area */}
//           <div className="p-6 bg-white/90 backdrop-blur-sm border-t border-slate-100 flex-shrink-0">
//             <form onSubmit={handleSubmit} className="flex items-end space-x-4">
//               <div className="flex-1 relative">
//                 <textarea
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   placeholder={`Hi ${userName}, what can I help you with?`}
//                   className="w-full h-auto px-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none text-slate-800 placeholder-slate-400 transition-all duration-200 min-h-[48px] max-h-32"
//                   rows={1}
//                   disabled={isLoading}
//                   // style={{
//                   //   height: 'auto',
//                   //   minHeight: '48px'
//                   // }}
//                   onInput={(e) => {
//                     const target = e.target as HTMLTextAreaElement
//                     target.style.height = 'auto'
//                     target.style.height = target.scrollHeight + 'px'
//                   }}
//                   onKeyDown={(e) => {
//                     if (e.key === "Enter" && !e.shiftKey) {
//                       e.preventDefault()
//                       handleSubmit(e)
//                     }
//                   }}
//                 />
//               </div>
//               <button
//                 type="submit"
//                 disabled={isLoading || !input.trim()}
//                 className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 disabled:from-slate-300 disabled:to-slate-400 text-white p-3 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none group flex-shrink-0"
//               >
//                 {isLoading ? (
//                   <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
//                     <circle
//                       className="opacity-25"
//                       cx="12"
//                       cy="12"
//                       r="10"
//                       stroke="currentColor"
//                       strokeWidth="4"
//                     ></circle>
//                     <path
//                       className="opacity-75"
//                       fill="currentColor"
//                       d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
//                     ></path>
//                   </svg>
//                 ) : (
//                   <svg
//                     className="w-5 h-5 group-hover:translate-x-0.5 transition-transform duration-200"
//                     fill="none"
//                     stroke="currentColor"
//                     viewBox="0 0 24 24"
//                   >
//                     <path
//                       strokeLinecap="round"
//                       strokeLinejoin="round"
//                       strokeWidth={2}
//                       d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
//                     />
//                   </svg>
//                 )}
//               </button>
//             </form>
//             <p className="text-xs text-slate-400 mt-2 text-center">Press Enter to send • Shift + Enter for new line</p>
//           </div>
//         </div>
//       </div>
//     </div>
//   )
// }

"use client"

import type React from "react"
import { useState, useEffect, useRef } from "react"
import { sendMessage, checkHealth } from "@/lib/api"

interface Message {
  id: string
  user_id: string
  reply: string
  timestamp: string
  isStreaming?: boolean
  user_message?: string
  status: "sending" | "sent" | "delivered" | "error"
  processingTime?: number
}

interface AgentActivity {
  id: string
  timestamp: string
  type: "thinking" | "processing" | "tool_use" | "handoff" | "response_generation"
  message: string
  details?: any
  duration?: number
}

interface SystemLog {
  id: string
  timestamp: string
  type: "info" | "error" | "success" | "warning"
  message: string
  details?: any
}

interface ChatSession {
  id: string
  name: string
  messages: Message[]
  created: string
  lastActive: string
  messageCount: number
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [userId] = useState(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("chat_user_id")
      if (stored) return stored
    }
    return "user_" + Math.random().toString(36).substr(2, 9)
  })
  const [userName, setUserName] = useState("")
  const [nameInput, setNameInput] = useState("")
  const [showNameInput, setShowNameInput] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [agentActivities, setAgentActivities] = useState<AgentActivity[]>([])
  const [systemLogs, setSystemLogs] = useState<SystemLog[]>([])
  const [showActivityPanel, setShowActivityPanel] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [showSidebar, setShowSidebar] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [currentSessionId, setCurrentSessionId] = useState<string>("")
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [isTyping, setIsTyping] = useState(false)
  const [copiedMessageId, setCopiedMessageId] = useState<string | null>(null)

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const streamingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  // Add agent activity
  const addAgentActivity = (type: AgentActivity["type"], message: string, details?: any) => {
    const activity: AgentActivity = {
      id: Date.now().toString() + Math.random(),
      timestamp: new Date().toISOString(),
      type,
      message,
      details,
    }
    setAgentActivities((prev) => [activity, ...prev].slice(0, 50))
  }

  // Add system log
  const addSystemLog = (type: SystemLog["type"], message: string, details?: any) => {
    const logEntry: SystemLog = {
      id: Date.now().toString() + Math.random(),
      timestamp: new Date().toISOString(),
      type,
      message,
      details,
    }
    setSystemLogs((prev) => [logEntry, ...prev].slice(0, 50))
  }

  // Enhanced copy functionality
  const copyMessage = async (message: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(message)
      setCopiedMessageId(messageId)
      addSystemLog("success", "Message copied to clipboard")
      setTimeout(() => setCopiedMessageId(null), 2000)
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement("textarea")
      textArea.value = message
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      try {
        document.execCommand("copy")
        setCopiedMessageId(messageId)
        addSystemLog("success", "Message copied to clipboard")
        setTimeout(() => setCopiedMessageId(null), 2000)
      } catch (fallbackErr) {
        addSystemLog("error", "Failed to copy message")
      }
      document.body.removeChild(textArea)
    }
  }

  // Load data from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUserName = localStorage.getItem("chat_user_name")
      const storedSessions = localStorage.getItem("chat_sessions")
      const storedCurrentSession = localStorage.getItem("chat_current_session")

      localStorage.setItem("chat_user_id", userId)

      if (storedUserName) {
        setUserName(storedUserName)
        setShowNameInput(false)
      }

      if (storedSessions) {
        try {
          const parsedSessions = JSON.parse(storedSessions)
          setSessions(parsedSessions)

          if (storedCurrentSession && parsedSessions.length > 0) {
            const currentSession = parsedSessions.find((s: ChatSession) => s.id === storedCurrentSession)
            if (currentSession) {
              setCurrentSessionId(currentSession.id)
              setMessages(currentSession.messages)
              addSystemLog("info", `Session restored: ${currentSession.name}`)
            }
          }
        } catch (err) {
          addSystemLog("error", "Failed to load sessions", err)
        }
      }

      addSystemLog("info", "Application initialized")
    }
  }, [userId])

  // Save to localStorage
  useEffect(() => {
    if (typeof window !== "undefined" && userName) {
      localStorage.setItem("chat_user_name", userName)
    }
  }, [userName])

  useEffect(() => {
    if (typeof window !== "undefined" && sessions.length > 0) {
      localStorage.setItem("chat_sessions", JSON.stringify(sessions))
    }
  }, [sessions])

  useEffect(() => {
    if (typeof window !== "undefined" && currentSessionId) {
      localStorage.setItem("chat_current_session", currentSessionId)
    }
  }, [currentSessionId])

  // Update current session
  useEffect(() => {
    if (currentSessionId && messages.length > 0) {
      setSessions((prev) =>
        prev.map((session) =>
          session.id === currentSessionId
            ? { ...session, messages, lastActive: new Date().toISOString(), messageCount: messages.length }
            : session,
        ),
      )
    }
  }, [messages, currentSessionId])

  useEffect(() => {
    checkHealth()
      .then(() => addSystemLog("success", "API connection established"))
      .catch((err) => {
        setError("API unavailable")
        addSystemLog("error", "API connection failed", err)
      })
  }, [])

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])

  const streamResponse = (fullResponse: string, messageIndex: number) => {
    const words = fullResponse.split(" ")
    let currentWordIndex = 0
    const startTime = Date.now()

    addAgentActivity("response_generation", `Generating response (${words.length} words)`)

    const streamNextWord = () => {
      if (currentWordIndex < words.length) {
        const currentText = words.slice(0, currentWordIndex + 1).join(" ")

        setMessages((prev) =>
          prev.map((msg, index) =>
            index === messageIndex
              ? { ...msg, reply: currentText, isStreaming: true, status: "delivered" as const }
              : msg,
          ),
        )

        currentWordIndex++
        streamingTimeoutRef.current = setTimeout(streamNextWord, 50)
      } else {
        const processingTime = Date.now() - startTime
        setMessages((prev) =>
          prev.map((msg, index) =>
            index === messageIndex ? { ...msg, isStreaming: false, processingTime, status: "delivered" as const } : msg,
          ),
        )
        addAgentActivity("processing", `Response completed in ${processingTime}ms`, { processingTime })
      }
    }
    streamNextWord()
  }

  const createNewSession = () => {
    const newSession: ChatSession = {
      id: Date.now().toString(),
      name: `Chat ${sessions.length + 1}`,
      messages: [],
      created: new Date().toISOString(),
      lastActive: new Date().toISOString(),
      messageCount: 0,
    }

    setSessions((prev) => [newSession, ...prev])
    setCurrentSessionId(newSession.id)
    setMessages([])
    addSystemLog("info", `New session created: ${newSession.name}`)
  }

  const switchSession = (sessionId: string) => {
    const session = sessions.find((s) => s.id === sessionId)
    if (session) {
      setCurrentSessionId(sessionId)
      setMessages(session.messages)
      setShowSidebar(false)
      addSystemLog("info", `Switched to: ${session.name}`)
    }
  }

  const deleteSession = (sessionId: string) => {
    setSessions((prev) => prev.filter((s) => s.id !== sessionId))
    if (currentSessionId === sessionId) {
      const remainingSessions = sessions.filter((s) => s.id !== sessionId)
      if (remainingSessions.length > 0) {
        switchSession(remainingSessions[0].id)
      } else {
        createNewSession()
      }
    }
    addSystemLog("warning", "Session deleted")
  }

  const exportChat = () => {
    const currentSession = sessions.find((s) => s.id === currentSessionId)
    if (currentSession) {
      const exportData = {
        session: currentSession,
        agentActivities: agentActivities.slice(0, 20),
        systemLogs: systemLogs.slice(0, 20),
        exportedAt: new Date().toISOString(),
        userName,
      }

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `chat-${currentSession.name}-${new Date().toISOString().split("T")[0]}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)

      addSystemLog("success", "Chat exported successfully")
    }
  }

  const handleNameSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const finalName = nameInput.trim() || "Guest"
    setUserName(finalName)
    setShowNameInput(false)

    if (sessions.length === 0) {
      createNewSession()
    }

    addSystemLog("info", `User authenticated: ${finalName}`)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = input.trim()
    const messageId = Date.now().toString()
    setIsLoading(true)
    setIsTyping(true)
    setError(null)

    if (streamingTimeoutRef.current) {
      clearTimeout(streamingTimeoutRef.current)
    }

    // Add user message immediately
    const userMsg: Message = {
      id: messageId,
      user_id: userId,
      reply: "",
      timestamp: new Date().toISOString(),
      user_message: userMessage,
      status: "sending",
    }

    setMessages((prev) => [...prev, userMsg])
    setInput("")

    addAgentActivity("thinking", "Processing user request...")
    addSystemLog("info", `Message sent: "${userMessage.substring(0, 30)}..."`)

    try {
      // Simulate agent activities
      setTimeout(() => addAgentActivity("tool_use", "Analyzing message context"), 200)
      setTimeout(() => addAgentActivity("processing", "Generating contextual response"), 500)

      const response = await sendMessage({
        user_id: userId,
        user_name: userName,
        message: userMessage,
      })

      // Update message with response
      const updatedMessage: Message = {
        ...userMsg,
        ...response,
        reply: "",
        isStreaming: true,
        status: "sent",
      }

      setMessages((prev) => prev.map((msg) => (msg.id === messageId ? updatedMessage : msg)))

      const messageIndex = messages.length
      streamResponse(response.reply, messageIndex)

      addSystemLog("success", "Response received")
    } catch (err: any) {
      const errorMessage = err.message || "Failed to send message"
      setError(errorMessage)
      setMessages((prev) => prev.map((msg) => (msg.id === messageId ? { ...msg, status: "error" as const } : msg)))
      addSystemLog("error", "Message failed", err)
      addAgentActivity("processing", "Error occurred during processing")
    } finally {
      setIsLoading(false)
      setIsTyping(false)
    }
  }

  const filteredMessages = messages.filter(
    (msg) =>
      searchQuery === "" ||
      msg.reply.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (msg.user_message && msg.user_message.toLowerCase().includes(searchQuery.toLowerCase())),
  )

  const getStatusIcon = (status: Message["status"]) => {
    switch (status) {
      case "sending":
        return <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" />
      case "sent":
        return <div className="w-2 h-2 bg-blue-400 rounded-full" />
      case "delivered":
        return <div className="w-2 h-2 bg-green-400 rounded-full" />
      case "error":
        return <div className="w-2 h-2 bg-red-400 rounded-full" />
      default:
        return null
    }
  }

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)

    if (minutes < 1) return "Just now"
    if (minutes < 60) return `${minutes}m ago`
    if (minutes < 1440) return `${Math.floor(minutes / 60)}h ago`
    return date.toLocaleDateString()
  }

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
                Professional AI Assistant
              </h1>
              <p className="text-slate-600 text-lg leading-relaxed">
                Your intelligent health & wellness expert with advanced capabilities.
              </p>
            </div>

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
                      if (sessions.length === 0) {
                        createNewSession()
                      }
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
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-100 flex">
      {/* Sidebar */}
      {showSidebar && (
        <div className="fixed inset-0 z-50 lg:relative lg:inset-auto">
          <div className="absolute inset-0 bg-black/20 lg:hidden" onClick={() => setShowSidebar(false)} />
          <div className="relative w-80 h-full bg-white/90 backdrop-blur-xl border-r border-white/20 shadow-xl">
            <div className="p-4 border-b border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-slate-800">Sessions</h2>
                <button
                  title="Close Sidebar"
                  onClick={() => setShowSidebar(false)}
                  className="lg:hidden p-2 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <button
                onClick={createNewSession}
                className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-2 px-4 rounded-xl font-medium transition-all duration-200"
              >
                + New Session
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-2">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  className={`group p-3 rounded-xl cursor-pointer transition-all duration-200 ${
                    currentSessionId === session.id
                      ? "bg-emerald-100 border border-emerald-200"
                      : "hover:bg-slate-100 border border-transparent"
                  }`}
                  onClick={() => switchSession(session.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-slate-800 truncate">{session.name}</p>
                      <p className="text-xs text-slate-500">
                        {session.messageCount} messages • {formatTime(session.lastActive)}
                      </p>
                    </div>
                    <button
                      title="Delete Session"
                      onClick={(e) => {
                        e.stopPropagation()
                        deleteSession(session.id)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 rounded transition-all duration-200"
                    >
                      <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 p-4 flex items-center justify-center">
        <div className="w-full max-w-6xl mx-auto h-[90vh] flex flex-col">
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden h-full flex flex-col">
            {/* Header */}
            <div className="bg-gradient-to-r from-emerald-500 to-teal-600 px-6 py-4 flex-shrink-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <button
                    title="Toggle Sidebar"
                    onClick={() => setShowSidebar(true)}
                    className="text-white hover:bg-white/10 p-2 rounded-lg transition-colors duration-200"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                  <div className="flex items-center space-x-2">
                    <div className="relative">
                      <div className="w-3 h-3 bg-green-300 rounded-full"></div>
                      <div className="absolute inset-0 w-3 h-3 bg-green-300 rounded-full animate-ping"></div>
                    </div>
                    <span className="text-white font-medium">{userName}</span>
                    {isTyping && <span className="text-emerald-100 text-sm">• AI is thinking...</span>}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="text-emerald-100 text-sm">{messages.length} msgs</div>
                  <button
                    title="Toggle Activity Panel"
                    onClick={() => setShowActivityPanel(!showActivityPanel)}
                    className={`text-emerald-100 hover:text-white text-sm px-3 py-1 rounded-full transition-all duration-200 ${
                      showActivityPanel ? "bg-white/20" : "bg-white/10 hover:bg-white/20"
                    }`}
                  >
                    Activity
                  </button>
                  <button
                  title="Export Chat"
                    onClick={exportChat}
                    className="text-emerald-100 hover:text-white p-2 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-200"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                  </button>
                  <button
                  title="Settings"
                    onClick={() => setShowSettings(!showSettings)}
                    className="text-emerald-100 hover:text-white p-2 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-200"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Search Bar */}
              {messages.length > 0 && (
                <div className="mt-3">
                  <div className="relative">
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search messages..."
                      className="w-full px-4 py-2 pl-10 bg-white/10 border border-white/20 rounded-xl text-white placeholder-emerald-100 focus:outline-none focus:ring-2 focus:ring-white/30 transition-all duration-200"
                    />
                    <svg
                      className="absolute left-3 top-2.5 w-4 h-4 text-emerald-100"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                      />
                    </svg>
                  </div>
                </div>
              )}
            </div>

            <div className="flex-1 flex overflow-hidden">
              {/* Messages Container */}
              <div className="flex-1 flex flex-col">
                <div
                  ref={chatContainerRef}
                  className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-slate-50/50 to-white/50 scroll-smooth"
                >
                  {error && (
                    <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-lg animate-slide-in">
                      <div className="flex items-center justify-between">
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
                        <button
                        title="Dismiss error"
                          onClick={() => setError(null)}
                          className="text-red-400 hover:text-red-600 transition-colors"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M6 18L18 6M6 6l12 12"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  )}

                  {filteredMessages.length === 0 && !error && searchQuery === "" && (
                    <div className="text-center py-12">
                      <div className="w-20 h-20 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg
                          className="w-10 h-10 text-emerald-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                          />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-slate-700 mb-2">Hello {userName}! 👋</h3>
                      <p className="text-slate-500 mb-4">Your professional AI assistant is ready to help!</p>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-lg mx-auto">
                        <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-emerald-100">
                          <p className="text-sm text-slate-600">💡 Health insights</p>
                        </div>
                        <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-teal-100">
                          <p className="text-sm text-slate-600">🧘 Wellness advice</p>
                        </div>
                        <div className="bg-white/60 backdrop-blur-sm rounded-xl p-3 border border-green-100">
                          <p className="text-sm text-slate-600">📊 Data analysis</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {searchQuery && filteredMessages.length === 0 && (
                    <div className="text-center py-8">
                      <p className="text-slate-500">No messages found for "{searchQuery}"</p>
                    </div>
                  )}

                  {filteredMessages.map((msg, index) => (
                    <div key={msg.id} className="group animate-slide-in">
                      {msg.user_message && (
                        <div className="mb-3 flex justify-end">
                          <div className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-2xl px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                            <p className="text-sm">{msg.user_message}</p>
                            <div className="flex items-center justify-between mt-2">
                              <span className="text-xs text-emerald-100">{formatTime(msg.timestamp)}</span>
                              <div className="flex items-center space-x-1">
                                {getStatusIcon(msg.status)}
                                {msg.processingTime && (
                                  <span className="text-xs text-emerald-100">{msg.processingTime}ms</span>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
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
                              <p className="text-xs text-slate-500">Professional Health Expert</p>
                            </div>
                            {msg.isStreaming && (
                              <div className="flex items-center space-x-1 ml-2">
                                <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce"></div>
                                <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce animate-delay-100"></div>
                                <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce animate-delay-200"></div>
                              </div>
                            )}
                          </div>
                          <div className="flex items-center space-x-2">
                            <time className="text-xs text-slate-400 bg-slate-50 px-3 py-1 rounded-full">
                              {formatTime(msg.timestamp)}
                            </time>
                            <div className="opacity-0 group-hover:opacity-100 flex items-center space-x-1 transition-opacity duration-200">
                              <button
                                onClick={() => copyMessage(msg.reply, msg.id)}
                                className={`p-1 rounded transition-colors ${
                                  copiedMessageId === msg.id
                                    ? "bg-green-100 text-green-600"
                                    : "hover:bg-slate-100 text-slate-400"
                                }`}
                                title={copiedMessageId === msg.id ? "Copied!" : "Copy message"}
                              >
                                {copiedMessageId === msg.id ? (
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                      strokeWidth={2}
                                      d="M5 13l4 4L19 7"
                                    />
                                  </svg>
                                ) : (
                                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                      strokeWidth={2}
                                      d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                                    />
                                  </svg>
                                )}
                              </button>
                            </div>
                          </div>
                        </div>
                        <div className="text-slate-800 leading-relaxed whitespace-pre-wrap">
                          {msg.reply}
                          {msg.isStreaming && (
                            <span className="inline-block w-2 h-5 bg-emerald-500 ml-1 animate-pulse"></span>
                          )}
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
                      <span className="text-slate-500 text-sm">Processing your request...</span>
                    </div>
                  )}

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
                        onInput={(e) => {
                          const target = e.target as HTMLTextAreaElement
                          target.style.height = "auto"
                          target.style.height = target.scrollHeight + "px"
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
                  <p className="text-xs text-slate-400 mt-2 text-center">
                    Press Enter to send • Shift + Enter for new line
                  </p>
                </div>
              </div>

              {/* Activity Panel */}
              {showActivityPanel && (
                <div className="w-80 border-l border-slate-200 bg-slate-50/50 flex flex-col">
                  <div className="p-4 border-b border-slate-200 bg-white/80">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-slate-800">Agent Activity</h3>
                      <button
                        onClick={() => {
                          setAgentActivities([])
                          setSystemLogs([])
                        }}
                        className="text-slate-500 hover:text-slate-700 text-sm"
                      >
                        Clear
                      </button>
                    </div>
                    <div className="flex space-x-2">
                      <div className="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded">
                        {agentActivities.length} activities
                      </div>
                      <div className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                        {systemLogs.length} logs
                      </div>
                    </div>
                  </div>
                  <div className="flex-1 overflow-y-auto p-4 space-y-3">
                    {/* Agent Activities */}
                    {agentActivities.map((activity) => (
                      <div
                        key={activity.id}
                        className={`p-3 rounded-lg text-xs border ${
                          activity.type === "thinking"
                            ? "bg-purple-50 text-purple-700 border-purple-200"
                            : activity.type === "processing"
                              ? "bg-blue-50 text-blue-700 border-blue-200"
                              : activity.type === "tool_use"
                                ? "bg-orange-50 text-orange-700 border-orange-200"
                                : activity.type === "handoff"
                                  ? "bg-indigo-50 text-indigo-700 border-indigo-200"
                                  : "bg-green-50 text-green-700 border-green-200"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-medium capitalize flex items-center">
                            {activity.type === "thinking" && "🤔"}
                            {activity.type === "processing" && "⚙️"}
                            {activity.type === "tool_use" && "🔧"}
                            {activity.type === "handoff" && "🔄"}
                            {activity.type === "response_generation" && "✨"}
                            <span className="ml-1">{activity.type.replace("_", " ")}</span>
                          </span>
                          <span className="text-xs opacity-70">{formatTime(activity.timestamp)}</span>
                        </div>
                        <p>{activity.message}</p>
                        {activity.duration && (
                          <div className="mt-1 text-xs opacity-70">Duration: {activity.duration}ms</div>
                        )}
                      </div>
                    ))}

                    {/* System Logs */}
                    {systemLogs.map((log) => (
                      <div
                        key={log.id}
                        className={`p-3 rounded-lg text-xs border ${
                          log.type === "error"
                            ? "bg-red-50 text-red-700 border-red-200"
                            : log.type === "warning"
                              ? "bg-yellow-50 text-yellow-700 border-yellow-200"
                              : log.type === "success"
                                ? "bg-green-50 text-green-700 border-green-200"
                                : "bg-slate-50 text-slate-700 border-slate-200"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-medium capitalize flex items-center">
                            {log.type === "error" && "❌"}
                            {log.type === "warning" && "⚠️"}
                            {log.type === "success" && "✅"}
                            {log.type === "info" && "ℹ️"}
                            <span className="ml-1">{log.type}</span>
                          </span>
                          <span className="text-xs opacity-70">{formatTime(log.timestamp)}</span>
                        </div>
                        <p>{log.message}</p>
                      </div>
                    ))}

                    {agentActivities.length === 0 && systemLogs.length === 0 && (
                      <p className="text-slate-500 text-center py-8">No activity yet</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/20">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-800">Settings</h2>
              <button
              title="Close settings"
                onClick={() => setShowSettings(false)}
                className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-slate-700 mb-2">Data Management</h3>
                <div className="space-y-2">
                  <button
                    onClick={() => {
                      localStorage.clear()
                      window.location.reload()
                    }}
                    className="w-full text-left p-3 hover:bg-red-50 rounded-lg transition-colors text-red-600"
                  >
                    Clear All Data
                  </button>
                  <button
                    onClick={exportChat}
                    className="w-full text-left p-3 hover:bg-slate-50 rounded-lg transition-colors"
                  >
                    Export Current Session
                  </button>
                </div>
              </div>

              <div>
                <h3 className="font-medium text-slate-700 mb-2">Statistics</h3>
                <div className="bg-slate-50 rounded-lg p-3 space-y-1 text-sm">
                  <p>Sessions: {sessions.length}</p>
                  <p>Messages: {messages.length}</p>
                  <p>Activities: {agentActivities.length}</p>
                  <p>System Logs: {systemLogs.length}</p>
                  <p>User ID: {userId.substring(0, 8)}...</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
