import type { ExtractResponse, QuizData } from "@/types/quiz";
import { quizDataSchema } from "@/lib/validations";

const API_BASE = "/api";

export async function uploadPDF(file: File): Promise<ExtractResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/extract`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      error: `Server error: ${response.status}`,
    }));
    throw new Error(
      (errorData as { error: string }).error || "Failed to process PDF"
    );
  }

  return response.json() as Promise<ExtractResponse>;
}

export async function fetchQuestions(): Promise<QuizData> {
  const response = await fetch(`${API_BASE}/questions`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      error: `Server error: ${response.status}`,
    }));
    throw new Error(
      (errorData as { error: string }).error || "Failed to fetch questions"
    );
  }

  const data: unknown = await response.json();
  const parsed = quizDataSchema.safeParse(data);

  if (!parsed.success) {
    throw new Error("Invalid quiz data format received from server");
  }

  return parsed.data;
}
