import type { NextRequest } from "next/server"

// Allow streaming responses up to 30 seconds
export const maxDuration = 30

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const requestBody = {
      name: body.user_id || "anonymous_user", // Correctly read user_id
      text: body.text || "",
      reply: body.reply || null,
    }
    console.log("Sending to FastAPI:", requestBody)

    const fastapiResponse = await fetch("https://mathsorpythonteacher.vercel.app/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },
      body: JSON.stringify(requestBody),
    })

    console.log("FastAPI response status:", fastapiResponse.status)

    if (!fastapiResponse.ok) {
      const errorText = await fastapiResponse.text()
      console.error("FastAPI error response:", errorText)
      throw new Error(`HTTP error! status: ${fastapiResponse.status}, body: ${errorText}`)
    }

    const reader = fastapiResponse.body?.getReader()
    const decoder = new TextDecoder()
    const encoder = new TextEncoder()
    let buffer = "" // Buffer to handle incomplete lines

    const customReadable = new ReadableStream({
      async start(controller) {
        if (!reader) {
          controller.close()
          return
        }

        try {
          while (true) {
            const { done, value } = await reader.read()
            if (done) break

            buffer += decoder.decode(value, { stream: true })
            const lines = buffer.split("\n")
            buffer = lines.pop() || "" // Keep the last (potentially incomplete) line in buffer

            for (const line of lines) {
              // Only forward lines that start with "data: "
              // This assumes your FastAPI backend sends valid SSE data lines for chunks and message_output.
              if (line.startsWith("data: ")) {
                controller.enqueue(encoder.encode(line + "\n\n")) // SSE requires two newlines
              }
              // Any other lines (e.g., plain text logs from FastAPI) are now ignored.
            }
          }
        } catch (error) {
          console.error("Stream processing error:", error)
          controller.error(error)
        } finally {
          // Process any remaining buffer content if it's a valid SSE line
          if (buffer.startsWith("data: ") && buffer.trim().length > 0) {
            controller.enqueue(encoder.encode(buffer + "\n\n"))
          }
          controller.close()
        }
      },
    })

    return new Response(customReadable, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
        "Access-Control-Allow-Origin": "*", // Consider restricting this in production
      },
    })
  } catch (error) {
    console.error("Proxy error:", error)
    return new Response(
      JSON.stringify({
        error: "Failed to fetch from FastAPI",
        details: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    )
  }
}
