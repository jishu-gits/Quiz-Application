"use client";

import { motion, AnimatePresence } from "motion/react";
import { X, AlertCircle, Loader2 } from "lucide-react";
import { FileUpload } from "@/components/ui/file-upload";

interface UploadZoneProps {
  onUpload: (file: File) => void;
  isUploading: boolean;
  error: string | null;
  onClearError: () => void;
}

export function UploadZone({
  onUpload,
  isUploading,
  error,
  onClearError,
}: UploadZoneProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-2xl mx-auto"
    >
      {/* Error display */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-6 p-4 rounded-xl bg-destructive/10 border border-destructive/20 flex items-start gap-3"
          >
            <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm text-destructive">{error}</p>
            </div>
            <button
              onClick={onClearError}
              className="text-destructive hover:text-destructive/80 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="relative">
        {isUploading && (
          <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm rounded-lg border border-border">
            <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
            <p className="text-muted-foreground font-medium">Uploading document...</p>
          </div>
        )}
        <div className={isUploading ? "pointer-events-none opacity-50" : ""}>
          <FileUpload
            onChange={(files) => {
              if (files.length > 0) {
                onUpload(files[0]);
              }
            }}
          />
        </div>
      </div>
    </motion.div>
  );
}

