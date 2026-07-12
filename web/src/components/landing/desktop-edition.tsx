"use client";

import { motion } from "motion/react";
import { Monitor, Timer, Keyboard, GripVertical } from "lucide-react";
import { SectionHeading } from "@/components/shared/section-heading";

export function DesktopEdition() {
  return (
    <section className="py-32 relative">
      <div className="section-container">
        <SectionHeading
          badge="Desktop Edition"
          title="Also Available on Desktop"
          subtitle="A Java Swing desktop client shares the same AI backend — perfect for offline quiz-taking."
        />

        <div className="mt-16 max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.7 }}
            className="glass-strong overflow-hidden"
          >
            {/* Desktop window chrome */}
            <div className="flex items-center gap-2 px-4 py-3 border-b border-white/[0.06] bg-white/[0.02]">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/60" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
                <div className="w-3 h-3 rounded-full bg-green-500/60" />
              </div>
              <div className="flex-1 text-center">
                <span className="text-xs text-white/30 font-mono">
                  JETSO TESTO — Quiz Application
                </span>
              </div>
            </div>

            {/* Desktop app mockup */}
            <div className="p-8 space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <h3 className="text-xl font-bold text-brand-400">
                    JETSO TESTO
                  </h3>
                  <p className="text-sm text-white/40">
                    Java Swing Desktop Client
                  </p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-500/10 border border-green-500/20">
                  <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                  <span className="text-xs font-medium text-green-400">
                    Connected to AI Backend
                  </span>
                </div>
              </div>

              {/* Feature list */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  {
                    icon: GripVertical,
                    title: "Drag & Drop Upload",
                    desc: "Drop PDFs directly into the application",
                  },
                  {
                    icon: Timer,
                    title: "Timed Questions",
                    desc: "15-second timer per question",
                  },
                  {
                    icon: Keyboard,
                    title: "Native Performance",
                    desc: "Built with Java Swing for speed",
                  },
                  {
                    icon: Monitor,
                    title: "Offline Ready",
                    desc: "No browser required",
                  },
                ].map((feature) => {
                  const Icon = feature.icon;
                  return (
                    <div
                      key={feature.title}
                      className="flex items-start gap-3 p-3 rounded-lg bg-white/[0.02]"
                    >
                      <Icon className="w-5 h-5 text-white/30 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-white/80">
                          {feature.title}
                        </p>
                        <p className="text-xs text-white/30">{feature.desc}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              <p className="text-xs text-white/30 text-center pt-4 border-t border-white/[0.06]">
                Both the web and desktop clients communicate with the same Flask
                AI backend running on localhost:5000
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
