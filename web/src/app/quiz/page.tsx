"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useQuizStore } from "@/stores/quiz-store";
import { useUpload } from "@/hooks/use-upload";
import { UploadZone } from "@/components/quiz/upload-zone";
import { ProcessingScreen } from "@/components/quiz/processing-screen";
import { QuizCard } from "@/components/quiz/quiz-card";
import { ResultsScreen } from "@/components/quiz/results-screen";
import { AnimatedGradient } from "@/components/shared/animated-gradient";
import type { QuizResult } from "@/types/quiz";

export default function QuizPage() {
  const { phase, resetQuiz, resetAll } = useQuizStore();
  const { upload, isUploading, error, clearError } = useUpload();
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);

  const handleComplete = useCallback((result: QuizResult) => {
    setQuizResult(result);
  }, []);

  const handleRestart = useCallback(() => {
    setQuizResult(null);
    resetQuiz();
  }, [resetQuiz]);

  const handleNewUpload = useCallback(() => {
    setQuizResult(null);
    resetAll();
  }, [resetAll]);

  const renderPhase = () => {
    if (phase === "results" && quizResult) {
      return (
        <ResultsScreen
          result={quizResult}
          onRestart={handleRestart}
          onNewUpload={handleNewUpload}
        />
      );
    }

    if (phase === "quiz") {
      return <QuizCard onComplete={handleComplete} />;
    }

    if (phase === "processing") {
      return <ProcessingScreen isComplete={phase !== "processing"} />;
    }

    // Default: upload phase (landing, uploading)
    return (
      <div className="space-y-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-4"
        >
          <h1 className="text-3xl sm:text-4xl font-bold gradient-text-white">
            Upload Your PDF
          </h1>
          <p className="text-white/40 max-w-md mx-auto">
            Drop any PDF document and our AI will generate an interactive quiz
            from its contents.
          </p>
        </motion.div>
        <UploadZone
          onUpload={upload}
          isUploading={isUploading}
          error={error}
          onClearError={clearError}
        />
      </div>
    );
  };

  return (
    <main className="relative min-h-screen flex items-center justify-center">
      <AnimatedGradient />

      <div className="relative z-10 w-full section-container py-20">
        {/* Back navigation */}
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-12"
        >
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-white/30 hover:text-white/60 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </motion.div>

        <AnimatePresence mode="wait">
          <motion.div
            key={phase + (quizResult ? "-result" : "")}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            {renderPhase()}
          </motion.div>
        </AnimatePresence>
      </div>
    </main>
  );
}
