import { NextResponse } from 'next/server';

const API_URL = 'https://agentic-ai-q4-lfx4.vercel.app';

export async function POST(request: Request) {
  try {
    const { user_id, user_name, message } = await request.json();

    if (!user_id || !user_name || !message) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    const response = await fetch(`${API_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id, user_name, message }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: error.status || 500 }
    );
  }
}