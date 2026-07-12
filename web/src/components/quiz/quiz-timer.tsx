"use client";

import { motion } from "motion/react";
import { formatTime } from "@/lib/utils";

interface QuizTimerProps {
  timeLeft: number;
  duration: number;
  progress: number;
}

export function QuizTimer({ timeLeft, duration, progress }: QuizTimerProps) {
  const size = 72;
  const strokeWidth = 4;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - progress);

  const getTimerColor = () => {
    if (progress > 0.5) return "text-emerald-400";
    if (progress > 0.25) return "text-yellow-400";
    return "text-red-400";
  };

  const getStrokeColor = () => {
    if (progress > 0.5) return "stroke-emerald-400";
    if (progress > 0.25) return "stroke-yellow-400";
    return "stroke-red-400";
  };

  return (
    <div className="relative flex items-center justify-center">
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
        viewBox={`0 0 ${size} ${size}`}
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-white/[0.06]"
        />
        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          className={`${getStrokeColor()} transition-colors duration-500`}
          style={{
            strokeDasharray: circumference,
            strokeDashoffset: strokeDashoffset,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          key={timeLeft}
          initial={{ scale: 1.2, opacity: 0.8 }}
          animate={{ scale: 1, opacity: 1 }}
          className={`text-lg font-bold tabular-nums ${getTimerColor()} transition-colors duration-500`}
        >
          {formatTime(timeLeft)}
        </motion.span>
        {duration > 0 && (
          <span className="text-[10px] text-white/30 font-mono">
            / {duration}s
          </span>
        )}
      </div>
    </div>
  );
}
