"use client";

import { useState, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronRight, Send } from "lucide-react";
import { cn } from "@/lib/utils";
import { useQuizStore } from "@/stores/quiz-store";
import { useTimer } from "@/hooks/use-timer";
import { QuizTimer } from "./quiz-timer";
import type { QuizResult } from "@/types/quiz";

const TIMER_DURATION = 15;

interface QuizCardProps {
  onComplete: (result: QuizResult) => void;
}

export function QuizCard({ onComplete }: QuizCardProps) {
  const {
    questions,
    currentIndex,
    answers,
    selectOption,
    nextQuestion,
    submitQuiz,
  } = useQuizStore();

  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const isLastQuestion = currentIndex === questions.length - 1;
  const currentQuestion = questions[currentIndex];

  const handleTimerExpire = useCallback(() => {
    if (isLastQuestion) {
      const result = submitQuiz();
      onComplete(result);
    } else {
      nextQuestion();
    }
  }, [isLastQuestion, nextQuestion, submitQuiz, onComplete]);

  const { timeLeft, progress, reset } = useTimer({
    duration: TIMER_DURATION,
    onExpire: handleTimerExpire,
    autoStart: true,
  });

  const handleSelectOption = useCallback(
    (option: string) => {
      setSelectedOption(option);
      selectOption(option);
    },
    [selectOption]
  );

  const handleNext = useCallback(() => {
    if (!selectedOption) return;
    setSelectedOption(null);
    nextQuestion();
    reset();
  }, [selectedOption, nextQuestion, reset]);

  const handleSubmit = useCallback(() => {
    const result = submitQuiz();
    onComplete(result);
  }, [submitQuiz, onComplete]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!currentQuestion) return;

      const keyNum = parseInt(e.key);
      if (keyNum >= 1 && keyNum <= currentQuestion.options.length) {
        handleSelectOption(currentQuestion.options[keyNum - 1]);
        return;
      }

      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        if (selectedOption) {
          if (isLastQuestion) {
            handleSubmit();
          } else {
            handleNext();
          }
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [
    currentQuestion,
    selectedOption,
    isLastQuestion,
    handleSelectOption,
    handleNext,
    handleSubmit,
  ]);

  // Reset selection when question changes
  useEffect(() => {
    const existingAnswer = answers.find(
      (a) => a.questionIndex === currentIndex
    );
    setSelectedOption(existingAnswer?.selectedOption ?? null);
  }, [currentIndex, answers]);

  if (!currentQuestion) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="w-full max-w-3xl mx-auto"
    >
      {/* Header: Progress + Timer */}
      <div className="flex items-center justify-between mb-8">
        <div className="space-y-2 flex-1">
          <div className="flex items-center gap-3">
            <span className="text-sm font-mono text-white/30">
              {currentIndex + 1} / {questions.length}
            </span>
          </div>
          {/* Progress bar */}
          <div className="h-1 rounded-full bg-white/[0.06] overflow-hidden max-w-xs">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-brand-500 to-accent-500"
              animate={{
                width: `${((currentIndex + 1) / questions.length) * 100}%`,
              }}
              transition={{ duration: 0.4 }}
            />
          </div>
        </div>

        <QuizTimer
          timeLeft={timeLeft}
          duration={TIMER_DURATION}
          progress={progress}
        />
      </div>

      {/* Question card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentIndex}
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -40 }}
          transition={{ duration: 0.35, ease: [0.25, 0.46, 0.45, 0.94] }}
        >
          {/* Question text */}
          <div className="glass-strong p-8 mb-6">
            <h2 className="text-xl sm:text-2xl font-semibold text-white leading-relaxed">
              {currentQuestion.question}
            </h2>
          </div>

          {/* Options */}
          <div className="space-y-3 mb-8">
            {currentQuestion.options.map((option, index) => {
              const isSelected = selectedOption === option;
              const optionKey = String.fromCharCode(65 + index);

              return (
                <motion.button
                  key={`${currentIndex}-${index}`}
                  onClick={() => handleSelectOption(option)}
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                  className={cn(
                    "w-full text-left p-5 rounded-xl border transition-all duration-200 flex items-center gap-4 group",
                    isSelected
                      ? "bg-brand-500/15 border-brand-500/40 shadow-lg shadow-brand-500/10"
                      : "bg-white/[0.02] border-white/[0.08] hover:bg-white/[0.05] hover:border-white/[0.15]"
                  )}
                >
                  {/* Option key */}
                  <span
                    className={cn(
                      "flex-shrink-0 w-9 h-9 rounded-lg text-sm font-semibold flex items-center justify-center transition-all duration-200",
                      isSelected
                        ? "bg-brand-500 text-white"
                        : "bg-white/[0.06] text-white/40 group-hover:bg-white/[0.1] group-hover:text-white/60"
                    )}
                  >
                    {optionKey}
                  </span>
                  <span
                    className={cn(
                      "text-sm sm:text-base transition-colors duration-200",
                      isSelected ? "text-white" : "text-white/70"
                    )}
                  >
                    {option}
                  </span>
                  {/* Keyboard hint */}
                  <span className="ml-auto text-xs text-white/20 hidden sm:block">
                    {index + 1}
                  </span>
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Action button */}
      <div className="flex justify-end">
        {isLastQuestion ? (
          <motion.button
            onClick={handleSubmit}
            disabled={!selectedOption}
            whileHover={selectedOption ? { scale: 1.03 } : undefined}
            whileTap={selectedOption ? { scale: 0.97 } : undefined}
            className={cn(
              "btn-primary",
              !selectedOption && "opacity-40 cursor-not-allowed"
            )}
          >
            <Send className="w-5 h-5" />
            Submit Quiz
          </motion.button>
        ) : (
          <motion.button
            onClick={handleNext}
            disabled={!selectedOption}
            whileHover={selectedOption ? { scale: 1.03 } : undefined}
            whileTap={selectedOption ? { scale: 0.97 } : undefined}
            className={cn(
              "btn-primary",
              !selectedOption && "opacity-40 cursor-not-allowed"
            )}
          >
            Next Question
            <ChevronRight className="w-5 h-5" />
          </motion.button>
        )}
      </div>

      {/* Keyboard hint */}
      <p className="mt-6 text-center text-xs text-white/20">
        Press <kbd className="px-1.5 py-0.5 rounded bg-white/[0.06] text-white/40 font-mono text-[10px]">1</kbd>-<kbd className="px-1.5 py-0.5 rounded bg-white/[0.06] text-white/40 font-mono text-[10px]">4</kbd> to select
        {" · "}
        <kbd className="px-1.5 py-0.5 rounded bg-white/[0.06] text-white/40 font-mono text-[10px]">Enter</kbd> to continue
      </p>
    </motion.div>
  );
}
