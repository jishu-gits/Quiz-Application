import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  if (mins > 0) {
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  }
  return `${secs}s`;
}

export function calculatePercentage(correct: number, total: number): number {
  if (total === 0) return 0;
  return Math.round((correct / total) * 100);
}

export function getPerformanceLabel(percentage: number): {
  label: string;
  description: string;
  color: string;
} {
  if (percentage >= 90) {
    return {
      label: "Outstanding",
      description: "Exceptional mastery of the material",
      color: "text-emerald-400",
    };
  }
  if (percentage >= 75) {
    return {
      label: "Excellent",
      description: "Strong understanding demonstrated",
      color: "text-green-400",
    };
  }
  if (percentage >= 60) {
    return {
      label: "Good",
      description: "Solid grasp with room for improvement",
      color: "text-blue-400",
    };
  }
  if (percentage >= 40) {
    return {
      label: "Fair",
      description: "Some gaps in understanding identified",
      color: "text-yellow-400",
    };
  }
  return {
    label: "Needs Improvement",
    description: "Review the material and try again",
    color: "text-orange-400",
  };
}
