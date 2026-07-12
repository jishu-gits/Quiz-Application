"use client";

import { useState, useEffect } from "react";
import { motion } from "motion/react";
import { RotateCcw, Upload, Trophy, Target, Clock, Monitor } from "lucide-react";
import { getPerformanceLabel, formatTime } from "@/lib/utils";
import type { QuizResult } from "@/types/quiz";

interface ResultsScreenProps {
  result: QuizResult;
  onRestart: () => void;
  onNewUpload: () => void;
}

export function ResultsScreen({
  result,
  onRestart,
  onNewUpload,
}: ResultsScreenProps) {
  const [displayScore, setDisplayScore] = useState(0);
  const performance = getPerformanceLabel(result.percentage);

  // Animated score counter
  useEffect(() => {
    const duration = 1500;
    const steps = 60;
    const increment = result.percentage / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = Math.min(Math.round(increment * step), result.percentage);
      setDisplayScore(current);
      if (step >= steps) {
        clearInterval(timer);
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [result.percentage]);

  // Circular progress ring
  const size = 200;
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - result.percentage / 100);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="w-full max-w-2xl mx-auto py-8"
    >
      {/* Score circle */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.7, ease: [0.25, 0.46, 0.45, 0.94] }}
        className="flex flex-col items-center mb-12"
      >
        <div className="relative mb-8">
          <svg
            width={size}
            height={size}
            className="transform -rotate-90"
            viewBox={`0 0 ${size} ${size}`}
          >
            <circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              fill="none"
              stroke="currentColor"
              strokeWidth={strokeWidth}
              className="text-white/[0.06]"
            />
            <motion.circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              fill="none"
              strokeWidth={strokeWidth}
              strokeLinecap="round"
              className="stroke-brand-400"
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset }}
              transition={{ duration: 1.5, delay: 0.3, ease: "easeOut" }}
              style={{ strokeDasharray: circumference }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <motion.span
              className="text-5xl font-bold gradient-text tabular-nums"
              key={displayScore}
            >
              {displayScore}%
            </motion.span>
            <span className="text-sm text-white/30 mt-1">Score</span>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="text-center space-y-2"
        >
          <h2 className={`text-3xl font-bold ${performance.color}`}>
            {performance.label}
          </h2>
          <p className="text-white/40 text-sm">{performance.description}</p>
        </motion.div>
      </motion.div>

      {/* Stats grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
        className="grid grid-cols-3 gap-4 mb-12"
      >
        {[
          {
            icon: Target,
            label: "Correct",
            value: `${result.correctAnswers} / ${result.totalQuestions}`,
          },
          {
            icon: Trophy,
            label: "Points",
            value: `${result.score} / ${result.maxScore}`,
          },
          {
            icon: Clock,
            label: "Time",
            value: formatTime(result.timeTaken),
          },
        ].map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="glass p-5 text-center space-y-3">
              <Icon className="w-6 h-6 mx-auto text-white/30" />
              <div>
                <p className="text-xl font-bold text-white">{stat.value}</p>
                <p className="text-xs text-white/30 mt-1">{stat.label}</p>
              </div>
            </div>
          );
        })}
      </motion.div>

      {/* Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.2 }}
        className="flex flex-col sm:flex-row items-center justify-center gap-4"
      >
        <motion.button
          onClick={onRestart}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          className="btn-primary w-full sm:w-auto"
        >
          <RotateCcw className="w-5 h-5" />
          Retake Quiz
        </motion.button>

        <motion.button
          onClick={onNewUpload}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          className="btn-secondary w-full sm:w-auto"
        >
          <Upload className="w-5 h-5" />
          Upload Another PDF
        </motion.button>
      </motion.div>

      {/* Desktop edition CTA */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="mt-12 glass p-5 text-center"
      >
        <div className="flex items-center justify-center gap-3 text-sm text-white/40">
          <Monitor className="w-4 h-4" />
          <span>
            Also available as a{" "}
            <span className="text-brand-400 font-medium">
              Java Desktop Application
            </span>{" "}
            — same AI backend, native experience
          </span>
        </div>
      </motion.div>
    </motion.div>
  );
}
