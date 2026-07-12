export interface QuizQuestion {
  question: string;
  options: string[];
  answer: string;
}

export interface QuizData {
  questions: QuizQuestion[];
}

export interface ExtractResponse {
  message: string;
  quiz: string;
}

export interface ExtractError {
  error: string;
}

export type QuizPhase =
  | "landing"
  | "uploading"
  | "processing"
  | "quiz"
  | "results";

export interface UserAnswer {
  questionIndex: number;
  selectedOption: string;
  isCorrect: boolean;
}

export interface QuizResult {
  totalQuestions: number;
  correctAnswers: number;
  score: number;
  maxScore: number;
  percentage: number;
  answers: UserAnswer[];
  timeTaken: number;
}

export interface ProcessingStage {
  id: string;
  label: string;
  description: string;
  icon: string;
  status: "pending" | "active" | "complete";
}
