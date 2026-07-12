"use client";

import { motion } from "motion/react";
import {
  ShieldCheck,
  Zap,
  Lock,
  Cpu,
  Layers,
  RefreshCw,
} from "lucide-react";
import { SectionHeading } from "@/components/shared/section-heading";
import { GlassCard } from "@/components/shared/glass-card";

const features = [
  {
    icon: Cpu,
    title: "100% Local AI",
    description:
      "All processing happens on your machine via Ollama. Your documents never leave your computer.",
  },
  {
    icon: Zap,
    title: "Vision-Powered Extraction",
    description:
      "Every page is analyzed by granite3.2-vision, a multimodal model that understands images natively.",
  },
  {
    icon: Layers,
    title: "Multi-Page Understanding",
    description:
      "Process multi-page documents with context preserved across all pages of your PDF.",
  },
  {
    icon: ShieldCheck,
    title: "Validated Questions",
    description:
      "Questions include 4 options, a correct answer, and explanations — structured as validated JSON.",
  },
  {
    icon: RefreshCw,
    title: "Instant Retake",
    description:
      "Retake quizzes or upload a new document at any time. No sign-up or rate limits required.",
  },
  {
    icon: Lock,
    title: "Privacy First",
    description:
      "No cloud APIs, no data collection. Your PDFs and quiz data stay entirely on your local machine.",
  },
];

export function Features() {
  return (
    <section className="py-32 relative">
      <div className="section-container">
        <SectionHeading
          badge="Features"
          title="Built for Knowledge"
          subtitle="Everything you need to transform documents into interactive learning experiences."
        />

        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <GlassCard key={feature.title} delay={index * 0.08}>
                <div className="space-y-4">
                  <motion.div
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: "spring", stiffness: 400 }}
                    className="w-12 h-12 rounded-xl bg-brand-500/10 border border-brand-500/20
                      flex items-center justify-center"
                  >
                    <Icon className="w-6 h-6 text-brand-400" />
                  </motion.div>
                  <h3 className="text-lg font-semibold text-white">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-white/50 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </GlassCard>
            );
          })}
        </div>
      </div>
    </section>
  );
}
