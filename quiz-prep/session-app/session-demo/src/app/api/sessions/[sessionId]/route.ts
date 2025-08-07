import { NextRequest } from 'next/server';

const FASTAPI_URL = process.env.FASTAPI_URL || 'https://study-buddy-theta-six.vercel.app';

export async function DELETE(
  request: NextRequest,
  { params }: { params: { sessionId: string } }
) {
  try {
    const { sessionId } = params;
    
    const formData = new FormData();
    formData.append('session_id', sessionId);

    const response = await fetch(`${FASTAPI_URL}/clear_session`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      return Response.json(
        { error: `Failed to clear session: ${errorText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error clearing session:', error);
    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
