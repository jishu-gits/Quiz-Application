"use client";

import { useRef } from "react";
import { useMousePosition } from "@/hooks/use-mouse-position";

export function AnimatedGradient() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mouse = useMousePosition(containerRef);

  return (
    <div ref={containerRef} className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Primary gradient orb — follows mouse */}
      <div
        className="absolute w-[800px] h-[800px] rounded-full opacity-20 blur-[120px] transition-transform duration-[2000ms] ease-out"
        style={{
          background:
            "radial-gradient(circle, oklch(0.55 0.22 265) 0%, transparent 70%)",
          left: `${mouse.normalizedX * 100 - 25}%`,
          top: `${mouse.normalizedY * 100 - 25}%`,
        }}
      />

      {/* Secondary orb — ambient */}
      <div
        className="absolute w-[600px] h-[600px] rounded-full opacity-15 blur-[100px] animate-float"
        style={{
          background:
            "radial-gradient(circle, oklch(0.7 0.18 165) 0%, transparent 70%)",
          right: "-10%",
          top: "20%",
        }}
      />

      {/* Tertiary orb — ambient */}
      <div
        className="absolute w-[500px] h-[500px] rounded-full opacity-10 blur-[80px] animate-float"
        style={{
          background:
            "radial-gradient(circle, oklch(0.6 0.2 300) 0%, transparent 70%)",
          left: "10%",
          bottom: "10%",
          animationDelay: "3s",
        }}
      />

      {/* Noise texture overlay */}
      <div
        className="absolute inset-0 opacity-[0.015]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Grid overlay */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />
    </div>
  );
}
