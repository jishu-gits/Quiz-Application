"use client";

import { motion } from "motion/react";
import {
  Globe,
  Server,
  Route,
  FlaskConical,
  Eye,
  Brain,
  FileJson,
  Monitor,
  ArrowDown,
} from "lucide-react";
import { SectionHeading } from "@/components/shared/section-heading";

const nodes = [
  { icon: Globe, label: "Browser", sub: "Next.js Client", color: "bg-blue-500/20 text-blue-400 border-blue-500/30" },
  { icon: Server, label: "Next.js Server", sub: "API Route Layer", color: "bg-indigo-500/20 text-indigo-400 border-indigo-500/30" },
  { icon: Route, label: "API Proxy", sub: "/api/extract → Flask", color: "bg-violet-500/20 text-violet-400 border-violet-500/30" },
  { icon: FlaskConical, label: "Flask Backend", sub: "Port 5000", color: "bg-purple-500/20 text-purple-400 border-purple-500/30" },
  { icon: Eye, label: "Vision Model", sub: "granite3.2-vision via Ollama", color: "bg-pink-500/20 text-pink-400 border-pink-500/30" },
  { icon: Brain, label: "Quiz Generator", sub: "LLM Prompt → JSON", color: "bg-rose-500/20 text-rose-400 border-rose-500/30" },
  { icon: FileJson, label: "JSON Response", sub: "{ questions: [...] }", color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
  { icon: Monitor, label: "Frontend", sub: "Interactive Quiz UI", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
];

export function Architecture() {
  return (
    <section className="py-32 relative">
      <div className="section-container">
        <SectionHeading
          badge="Architecture"
          title="System Design"
          subtitle="A modern multi-tier architecture where the browser never directly communicates with the AI backend."
        />

        <div className="mt-20 max-w-lg mx-auto">
          {nodes.map((node, index) => {
            const Icon = node.icon;
            return (
              <div key={node.label} className="flex flex-col items-center">
                {/* Node */}
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true, margin: "-40px" }}
                  transition={{
                    duration: 0.5,
                    delay: index * 0.08,
                    ease: [0.25, 0.46, 0.45, 0.94],
                  }}
                  whileHover={{ scale: 1.04 }}
                  className={`w-full glass p-4 flex items-center gap-4 ${
                    index === 0 || index === nodes.length - 1
                      ? "glass-strong"
                      : ""
                  }`}
                >
                  <div
                    className={`flex-shrink-0 w-11 h-11 rounded-lg border flex items-center justify-center ${node.color}`}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-white">
                      {node.label}
                    </h4>
                    <p className="text-xs text-white/40 font-mono">
                      {node.sub}
                    </p>
                  </div>
                </motion.div>

                {/* Arrow connector */}
                {index < nodes.length - 1 && (
                  <motion.div
                    initial={{ opacity: 0, scaleY: 0 }}
                    whileInView={{ opacity: 1, scaleY: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.3, delay: index * 0.08 + 0.15 }}
                    className="flex flex-col items-center py-1.5 text-white/20"
                  >
                    <div className="w-px h-4 bg-white/10" />
                    <ArrowDown className="w-4 h-4" />
                  </motion.div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
