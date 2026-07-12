import { NextResponse } from "next/server";

const FLASK_BACKEND = process.env.FLASK_BACKEND_URL || "http://localhost:5000";

export async function GET() {
  try {
    const response = await fetch(`${FLASK_BACKEND}/extractQuestions`);
    const data: unknown = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Internal server error";

    if (
      message.includes("ECONNREFUSED") ||
      message.includes("fetch failed")
    ) {
      return NextResponse.json(
        {
          error:
            "Cannot connect to the AI backend. Please ensure the Flask server is running on port 5000.",
        },
        { status: 503 }
      );
    }

    return NextResponse.json({ error: message }, { status: 500 });
  }
}
