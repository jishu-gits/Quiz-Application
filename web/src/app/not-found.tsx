import Link from "next/link";
import { FileQuestion } from "lucide-react";

export default function NotFound() {
  return (
    <main className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-linear-to-b from-brand-500/10 via-transparent to-transparent" />

      <div className="section-container text-center py-24">
        <div className="glass glass-hover glow-brand inline-flex items-center justify-center w-20 h-20 mb-8">
          <FileQuestion className="w-9 h-9 text-brand-400" />
        </div>

        <p className="font-mono text-sm tracking-widest text-white/40 mb-4">
          ERROR 404
        </p>

        <h1 className="text-4xl sm:text-5xl font-bold gradient-text-white mb-4">
          Page not found
        </h1>

        <p className="max-w-md mx-auto text-white/50 mb-10">
          The page you&apos;re looking for doesn&apos;t exist or may have been
          moved. Let&apos;s get you back on track.
        </p>

        <Link href="/" className="btn-primary">
          Back to home
        </Link>
      </div>
    </main>
  );
}
