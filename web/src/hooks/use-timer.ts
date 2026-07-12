"use client";

import { useState, useEffect, useCallback, useRef } from "react";

interface UseTimerOptions {
  duration: number;
  onExpire?: () => void;
  autoStart?: boolean;
}

export function useTimer({ duration, onExpire, autoStart = true }: UseTimerOptions) {
  const [timeLeft, setTimeLeft] = useState(duration);
  const [isRunning, setIsRunning] = useState(autoStart);
  const onExpireRef = useRef(onExpire);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  onExpireRef.current = onExpire;

  const stop = useCallback(() => {
    setIsRunning(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const reset = useCallback(
    (newDuration?: number) => {
      stop();
      setTimeLeft(newDuration ?? duration);
      setIsRunning(true);
    },
    [duration, stop]
  );

  const start = useCallback(() => {
    setIsRunning(true);
  }, []);

  useEffect(() => {
    if (!isRunning) return;

    intervalRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isRunning]);

  useEffect(() => {
    if (timeLeft === 0 && isRunning) {
      setIsRunning(false);
      onExpireRef.current?.();
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
  }, [timeLeft, isRunning]);

  const isExpired = timeLeft === 0;
  const progress = duration > 0 ? timeLeft / duration : 0;

  return { timeLeft, isRunning, isExpired, progress, start, stop, reset };
}
