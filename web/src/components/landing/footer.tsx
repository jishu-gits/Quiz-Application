"use client";

import { ExternalLink, Code2 } from "lucide-react";

export function Footer() {
  return (
    <footer className="relative py-16 border-t border-white/[0.06]">
      <div className="section-container">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-2 text-center md:text-left">
            <h3 className="text-xl font-bold gradient-text">JETSO TESTO</h3>
            <p className="text-sm text-white/40">
              AI-Powered Quiz Generation Platform
            </p>
          </div>

          <div className="flex items-center gap-6">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-white/40 hover:text-white/80 transition-colors"
            >
              <Code2 className="w-4 h-4" />
              GitHub
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-white/[0.04] text-center">
          <p className="text-xs text-white/20">
            Built with Next.js, Flask, and Ollama. Powered by local AI models.
          </p>
        </div>
      </div>
    </footer>
  );
}
