"use client";

import { useRouter } from "next/navigation";
import { useCallback } from "react";
import { Hero } from "@/components/landing/hero";
import { Pipeline } from "@/components/landing/pipeline";
import { Architecture } from "@/components/landing/architecture";
import { Features } from "@/components/landing/features";
import { DesktopEdition } from "@/components/landing/desktop-edition";
import { Footer } from "@/components/landing/footer";

export default function LandingPage() {
  const router = useRouter();

  const handleStartQuiz = useCallback(() => {
    router.push("/quiz");
  }, [router]);

  return (
    <>
      <Hero onStartQuiz={handleStartQuiz} />
      <Pipeline />
      <Features />
      <Architecture />
      <DesktopEdition />
      <Footer />
    </>
  );
}
