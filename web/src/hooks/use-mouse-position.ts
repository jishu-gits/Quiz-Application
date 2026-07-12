"use client";

import { useState, useEffect, useCallback, type RefObject } from "react";

interface MousePosition {
  x: number;
  y: number;
  normalizedX: number;
  normalizedY: number;
}

export function useMousePosition(
  containerRef?: RefObject<HTMLElement | null>
): MousePosition {
  const [position, setPosition] = useState<MousePosition>({
    x: 0,
    y: 0,
    normalizedX: 0.5,
    normalizedY: 0.5,
  });

  const handleMouseMove = useCallback(
    (event: MouseEvent) => {
      if (containerRef?.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        setPosition({
          x,
          y,
          normalizedX: x / rect.width,
          normalizedY: y / rect.height,
        });
      } else {
        setPosition({
          x: event.clientX,
          y: event.clientY,
          normalizedX: event.clientX / window.innerWidth,
          normalizedY: event.clientY / window.innerHeight,
        });
      }
    },
    [containerRef]
  );

  useEffect(() => {
    const target = containerRef?.current || window;
    target.addEventListener(
      "mousemove",
      handleMouseMove as EventListener
    );
    return () => {
      target.removeEventListener(
        "mousemove",
        handleMouseMove as EventListener
      );
    };
  }, [handleMouseMove, containerRef]);

  return position;
}
