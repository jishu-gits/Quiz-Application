"use client";

import { motion } from "motion/react";
import {
  FileText,
  Eye,
  Brain,
  MessageSquareText,
  Gamepad2,
  Trophy,
} from "lucide-react";
import { SectionHeading } from "@/components/shared/section-heading";

const stages = [
  {
    icon: FileText,
    label: "PDF Upload",
    description: "Drag and drop any PDF document",
    color: "from-blue-500 to-blue-600",
    glowColor: "blue-500",
  },
  {
    icon: Eye,
    label: "Vision Analysis",
    description: "Each page is analyzed by a vision model",
    color: "from-violet-500 to-purple-600",
    glowColor: "violet-500",
  },
  {
    icon: Brain,
    label: "Knowledge Extraction",
    description: "Key information is extracted and merged",
    color: "from-purple-500 to-pink-600",
    glowColor: "purple-500",
  },
  {
    icon: MessageSquareText,
    label: "AI Question Generation",
    description: "Questions with options are generated",
    color: "from-pink-500 to-rose-600",
    glowColor: "pink-500",
  },
  {
    icon: Gamepad2,
    label: "Interactive Quiz",
    description: "Timed quiz experience with scoring",
    color: "from-orange-500 to-amber-600",
    glowColor: "orange-500",
  },
  {
    icon: Trophy,
    label: "Results & Insights",
    description: "Performance analysis and feedback",
    color: "from-emerald-500 to-green-600",
    glowColor: "emerald-500",
  },
];

export function Pipeline() {
  return (
    <section id="pipeline" className="py-32 relative">
      <div className="section-container">
        <SectionHeading
          badge="How it Works"
          title="AI-Powered Pipeline"
          subtitle="From PDF to interactive quiz in six intelligent stages, all powered by local AI models running on your machine."
        />

        <div className="mt-20 relative">
          {/* Connecting line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-white/10 to-transparent hidden lg:block" />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-y-16 lg:gap-x-24">
            {stages.map((stage, index) => {
              const Icon = stage.icon;
              const isLeft = index % 2 === 0;

              return (
                <motion.div
                  key={stage.label}
                  initial={{ opacity: 0, x: isLeft ? -40 : 40 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: "-80px" }}
                  transition={{
                    duration: 0.6,
                    delay: index * 0.1,
                    ease: [0.25, 0.46, 0.45, 0.94],
                  }}
                  className={`relative ${isLeft ? "lg:text-right" : "lg:col-start-2"}`}
                >
                  {/* Stage number connector (desktop) */}
                  <div
                    className={`hidden lg:flex absolute top-1/2 -translate-y-1/2 items-center ${
                      isLeft ? "-right-[3.25rem]" : "-left-[3.25rem]"
                    }`}
                  >
                    <motion.div
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.4, delay: index * 0.1 + 0.3 }}
                      className={`w-10 h-10 rounded-full bg-gradient-to-br ${stage.color}
                        flex items-center justify-center text-sm font-bold shadow-lg`}
                      style={{
                        boxShadow: `0 0 30px -5px var(--color-${stage.glowColor}, rgba(139, 92, 246, 0.3))`,
                      }}
                    >
                      {index + 1}
                    </motion.div>
                  </div>

                  {/* Card */}
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    className="glass p-6 glass-hover group"
                  >
                    <div
                      className={`flex items-start gap-4 ${
                        isLeft ? "lg:flex-row-reverse lg:text-right" : ""
                      }`}
                    >
                      <div
                        className={`flex-shrink-0 w-12 h-12 rounded-xl bg-gradient-to-br ${stage.color}
                          flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300`}
                      >
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 lg:hidden mb-1">
                          <span className="text-xs font-mono text-white/30">
                            {String(index + 1).padStart(2, "0")}
                          </span>
                        </div>
                        <h3 className="text-lg font-semibold text-white mb-1">
                          {stage.label}
                        </h3>
                        <p className="text-sm text-white/50 leading-relaxed">
                          {stage.description}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
