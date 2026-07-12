import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    root: "./",
  },
  outputFileTracingRoot: process.cwd(),
};

export default nextConfig;
