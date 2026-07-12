"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { Home, AlertCircle } from "lucide-react";
import { AnimatedGradient } from "@/components/shared/animated-gradient";

export default function NotFound() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <AnimatedGradient />
      
      {/* Floating particles */}
      <div className="absolute inset-0 pointer-events-none">
        {Array.from({ length: 15 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 rounded-full bg-brand-400/20"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              opacity: [0.1, 0.5, 0.1],
              scale: [1, 1.5, 1],
            }}
            transition={{
              duration: 3 + Math.random() * 4,
              repeat: Infinity,
              delay: Math.random() * 3,
              ease: "easeInOut",
            }}
          />
        ))}
      </div>

      <div className="relative z-10 section-container flex flex-col items-center justify-center text-center">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
          className="glass p-10 md:p-16 max-w-xl w-full flex flex-col items-center relative overflow-hidden"
        >
          {/* Subtle background glow inside the card */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand-500/10 blur-[60px] rounded-full pointer-events-none" />

          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="w-20 h-20 mb-8 rounded-2xl bg-brand-500/10 flex items-center justify-center border border-brand-500/20 shadow-inner"
          >
            <AlertCircle className="w-10 h-10 text-brand-400" />
          </motion.div>
          
          <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-2 gradient-text-white drop-shadow-sm">
            404
          </h1>
          
          <h2 className="text-2xl md:text-3xl font-semibold mb-6 gradient-text">
            Page Not Found
          </h2>
          
          <p className="text-white/60 text-lg mb-10 max-w-md leading-relaxed">
            The page you're looking for doesn't exist, has been moved, or is temporarily unavailable.
          </p>
          
          <Link href="/">
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              className="group btn-primary text-lg glow-brand"
            >
              <Home className="w-5 h-5" />
              Return to Homepage
            </motion.button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
