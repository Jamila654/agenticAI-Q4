// interface ChatRequest {
//   user_id: string;
//   user_name: string;
//   message: string;
// }

// interface ChatResponse {
//   user_id: string;
//   reply: string;
//   timestamp: string;
// }

// export async function sendMessage(data: ChatRequest): Promise<ChatResponse> {
//   const response = await fetch('/api/chat', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data),
//   });

//   if (!response.ok) {
//     const error = await response.json();
//     throw new Error(error.error || 'Failed to send message');
//   }

//   return response.json();
// }

// export async function checkHealth() {
//   const response = await fetch('/api/health');
//   if (!response.ok) {
//     throw new Error('Health check failed');
//   }
//   return response.json();
// }

interface ChatRequest {
  user_id: string
  user_name: string
  message: string
}

interface ChatResponse {
  user_id: string
  reply: string
  timestamp: string
}

export async function sendMessage(data: ChatRequest): Promise<ChatResponse> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || "Failed to send message")
  }

  return response.json()
}

export async function checkHealth() {
  const response = await fetch("/api/health")
  if (!response.ok) {
    throw new Error("Health check failed")
  }
  return response.json()
}
