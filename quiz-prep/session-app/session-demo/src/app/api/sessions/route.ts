import { NextRequest } from 'next/server';

const FASTAPI_URL = process.env.FASTAPI_URL || 'https://study-buddy-theta-six.vercel.app';

export async function GET() {
  try {
    const response = await fetch(`${FASTAPI_URL}/sessions`);
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    return Response.json({ error: 'Failed to fetch sessions' }, { status: 500 });
  }
}

export async function POST() {
  try {
    const response = await fetch(`${FASTAPI_URL}/new_session`, {
      method: 'POST',
    });
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    return Response.json({ error: 'Failed to create session' }, { status: 500 });
  }
}
