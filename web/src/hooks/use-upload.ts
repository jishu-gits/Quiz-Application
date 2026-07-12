"use client";

import { useState, useCallback } from "react";
import { uploadPDF, fetchQuestions } from "@/lib/api";
import { useQuizStore } from "@/stores/quiz-store";
import { pdfFileSchema } from "@/lib/validations";

export function useUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { setPhase, setQuestions, setSelectedFile } = useQuizStore();

  const upload = useCallback(
    async (file: File) => {
      setError(null);

      const validation = pdfFileSchema.safeParse(file);
      if (!validation.success) {
        setError(validation.error.issues[0]?.message || "Invalid file");
        return;
      }

      setSelectedFile(file);
      setIsUploading(true);
      setPhase("uploading");

      try {
        setPhase("processing");
        await uploadPDF(file);

        const quizData = await fetchQuestions();
        setQuestions(quizData.questions);
        setPhase("quiz");
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "An unexpected error occurred";
        setError(message);
        setPhase("landing");
      } finally {
        setIsUploading(false);
      }
    },
    [setPhase, setQuestions, setSelectedFile]
  );

  return { upload, isUploading, error, clearError: () => setError(null) };
}
