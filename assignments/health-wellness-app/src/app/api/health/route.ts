import { NextResponse } from 'next/server';

const API_URL = 'https://agentic-ai-q4-lfx4.vercel.app';

export async function GET() {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Health check failed');
    }
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Health check error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: error.status || 500 }
    );
  }
}