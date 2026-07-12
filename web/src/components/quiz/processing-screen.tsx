"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  FileText,
  Eye,
  Brain,
  MessageSquareText,
  CheckCircle2,
  Loader2,
} from "lucide-react";
import type { ProcessingStage } from "@/types/quiz";

const STAGES: ProcessingStage[] = [
  {
    id: "reading",
    label: "Reading PDF",
    description: "Converting document pages to images",
    icon: "FileText",
    status: "pending",
  },
  {
    id: "analyzing",
    label: "Analyzing Pages",
    description: "Running vision model on each page",
    icon: "Eye",
    status: "pending",
  },
  {
    id: "extracting",
    label: "Extracting Knowledge",
    description: "Merging page descriptions into context",
    icon: "Brain",
    status: "pending",
  },
  {
    id: "generating",
    label: "Generating Questions",
    description: "Creating quiz questions from extracted knowledge",
    icon: "MessageSquareText",
    status: "pending",
  },
  {
    id: "preparing",
    label: "Preparing Quiz",
    description: "Validating and formatting quiz data",
    icon: "CheckCircle2",
    status: "pending",
  },
];

const ICON_MAP = {
  FileText,
  Eye,
  Brain,
  MessageSquareText,
  CheckCircle2,
} as const;

interface ProcessingScreenProps {
  isComplete: boolean;
}

export function ProcessingScreen({ isComplete }: ProcessingScreenProps) {
  const [stages, setStages] = useState<ProcessingStage[]>(STAGES);
  const [activeIndex, setActiveIndex] = useState(0);

  const advanceStage = useCallback(() => {
    setStages((prev) =>
      prev.map((stage, i) => {
        if (i < activeIndex) return { ...stage, status: "complete" };
        if (i === activeIndex) return { ...stage, status: "active" };
        return { ...stage, status: "pending" };
      })
    );
  }, [activeIndex]);

  useEffect(() => {
    advanceStage();
  }, [advanceStage]);

  useEffect(() => {
    if (isComplete) {
      setStages((prev) => prev.map((s) => ({ ...s, status: "complete" })));
      return;
    }

    // Simulate stage progression with realistic-feeling durations
    const durations = [3000, 8000, 5000, 10000, 3000];
    const timer = setTimeout(() => {
      if (activeIndex < STAGES.length - 1) {
        setActiveIndex((prev) => prev + 1);
      }
    }, durations[activeIndex]);

    return () => clearTimeout(timer);
  }, [activeIndex, isComplete]);

  const progress = isComplete
    ? 100
    : Math.round(((activeIndex + 0.5) / STAGES.length) * 100);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="w-full max-w-lg mx-auto py-12"
    >
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <motion.div
          animate={!isComplete ? { rotate: 360 } : { rotate: 0 }}
          transition={
            !isComplete
              ? { duration: 3, repeat: Infinity, ease: "linear" }
              : { duration: 0.3 }
          }
          className="w-16 h-16 mx-auto mb-6 rounded-full bg-brand-500/10 border border-brand-500/20
            flex items-center justify-center"
        >
          {isComplete ? (
            <CheckCircle2 className="w-8 h-8 text-emerald-400" />
          ) : (
            <Loader2 className="w-8 h-8 text-brand-400" />
          )}
        </motion.div>
        <h2 className="text-2xl font-bold gradient-text-white mb-2">
          {isComplete ? "Quiz Ready!" : "Processing Your Document"}
        </h2>
        <p className="text-white/40 text-sm">
          {isComplete
            ? "Your quiz has been generated successfully"
            : "Our AI is analyzing your PDF with local vision models"}
        </p>
      </motion.div>

      {/* Progress bar */}
      <div className="mb-10 px-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-white/30 font-mono">{progress}%</span>
        </div>
        <div className="h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-brand-500 to-accent-500"
            initial={{ width: "0%" }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          />
        </div>
      </div>

      {/* Stage list */}
      <div className="space-y-3 px-4">
        <AnimatePresence>
          {stages.map((stage, index) => {
            const Icon =
              ICON_MAP[stage.icon as keyof typeof ICON_MAP] || FileText;
            const isActive = stage.status === "active";
            const isComplete = stage.status === "complete";

            return (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className={`flex items-center gap-4 p-4 rounded-xl transition-all duration-500 ${
                  isActive
                    ? "bg-brand-500/10 border border-brand-500/20"
                    : isComplete
                    ? "bg-white/[0.02] border border-white/[0.04]"
                    : "bg-transparent border border-transparent"
                }`}
              >
                {/* Icon */}
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 transition-all duration-500 ${
                    isComplete
                      ? "bg-emerald-500/10 text-emerald-400"
                      : isActive
                      ? "bg-brand-500/20 text-brand-400"
                      : "bg-white/[0.04] text-white/20"
                  }`}
                >
                  {isActive ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "linear",
                      }}
                    >
                      <Loader2 className="w-5 h-5" />
                    </motion.div>
                  ) : isComplete ? (
                    <CheckCircle2 className="w-5 h-5" />
                  ) : (
                    <Icon className="w-5 h-5" />
                  )}
                </div>

                {/* Text */}
                <div className="flex-1 min-w-0">
                  <p
                    className={`text-sm font-medium transition-colors duration-500 ${
                      isComplete
                        ? "text-white/60"
                        : isActive
                        ? "text-white"
                        : "text-white/30"
                    }`}
                  >
                    {stage.label}
                  </p>
                  <p
                    className={`text-xs transition-colors duration-500 ${
                      isActive ? "text-white/40" : "text-white/20"
                    }`}
                  >
                    {stage.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
