import { create } from "zustand";
import type { QuizPhase, QuizQuestion, UserAnswer, QuizResult } from "@/types/quiz";

interface QuizStore {
  // Phase
  phase: QuizPhase;
  setPhase: (phase: QuizPhase) => void;

  // File
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;

  // Questions
  questions: QuizQuestion[];
  setQuestions: (questions: QuizQuestion[]) => void;

  // Quiz state
  currentIndex: number;
  answers: UserAnswer[];
  startTime: number;

  // Actions
  selectOption: (option: string) => void;
  nextQuestion: () => void;
  submitQuiz: () => QuizResult;
  resetQuiz: () => void;
  resetAll: () => void;
}

export const useQuizStore = create<QuizStore>((set, get) => ({
  phase: "landing",
  setPhase: (phase) => set({ phase }),

  selectedFile: null,
  setSelectedFile: (file) => set({ selectedFile: file }),

  questions: [],
  setQuestions: (questions) =>
    set({
      questions,
      currentIndex: 0,
      answers: [],
      startTime: Date.now(),
    }),

  currentIndex: 0,
  answers: [],
  startTime: 0,

  selectOption: (option) => {
    const { currentIndex, questions, answers } = get();
    const question = questions[currentIndex];
    if (!question) return;

    const isCorrect = option === question.answer;
    const existingIndex = answers.findIndex(
      (a) => a.questionIndex === currentIndex
    );
    const newAnswer: UserAnswer = {
      questionIndex: currentIndex,
      selectedOption: option,
      isCorrect,
    };

    if (existingIndex >= 0) {
      const newAnswers = [...answers];
      newAnswers[existingIndex] = newAnswer;
      set({ answers: newAnswers });
    } else {
      set({ answers: [...answers, newAnswer] });
    }
  },

  nextQuestion: () => {
    const { currentIndex, questions } = get();
    if (currentIndex < questions.length - 1) {
      set({ currentIndex: currentIndex + 1 });
    }
  },

  submitQuiz: () => {
    const { questions, answers, startTime } = get();
    const correctAnswers = answers.filter((a) => a.isCorrect).length;
    const result: QuizResult = {
      totalQuestions: questions.length,
      correctAnswers,
      score: correctAnswers * 10,
      maxScore: questions.length * 10,
      percentage: Math.round((correctAnswers / questions.length) * 100),
      answers,
      timeTaken: Math.round((Date.now() - startTime) / 1000),
    };
    set({ phase: "results" });
    return result;
  },

  resetQuiz: () =>
    set((state) => ({
      currentIndex: 0,
      answers: [],
      startTime: Date.now(),
      phase: "quiz",
      questions: state.questions,
    })),

  resetAll: () =>
    set({
      phase: "landing",
      selectedFile: null,
      questions: [],
      currentIndex: 0,
      answers: [],
      startTime: 0,
    }),
}));
