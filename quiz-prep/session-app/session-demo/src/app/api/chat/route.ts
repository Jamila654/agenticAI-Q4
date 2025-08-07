import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { session_id, text } = await request.json();

    if (!session_id || !text) {
      return new Response(
        JSON.stringify({ error: 'session_id and text are required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const FASTAPI_URL = 'https://study-buddy-theta-six.vercel.app';
    
    // Create form data as your FastAPI expects
    const formData = new FormData();
    formData.append('session_id', session_id);
    formData.append('text', text);

    const response = await fetch(`${FASTAPI_URL}/chat`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      return new Response(
        JSON.stringify({ error: `FastAPI error: ${errorText}` }),
        { status: response.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Forward the streaming response
    const stream = new ReadableStream({
      start(controller) {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        function pump(): Promise<void> {
          return reader!.read().then(({ done, value }) => {
            if (done) {
              controller.close();
              return;
            }

            const chunk = decoder.decode(value, { stream: true });
            controller.enqueue(new TextEncoder().encode(chunk));
            return pump();
          });
        }

        return pump();
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Error in chat route:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
