import { z } from "zod";

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
const ACCEPTED_FILE_TYPES = ["application/pdf"];

export const pdfFileSchema = z
  .instanceof(File)
  .refine((file) => file.size > 0, "File is empty")
  .refine(
    (file) => file.size <= MAX_FILE_SIZE,
    `File size must be less than ${MAX_FILE_SIZE / (1024 * 1024)}MB`
  )
  .refine(
    (file) =>
      ACCEPTED_FILE_TYPES.includes(file.type) ||
      file.name.toLowerCase().endsWith(".pdf"),
    "Only PDF files are accepted"
  );

export const quizQuestionSchema = z.object({
  question: z.string().min(1),
  options: z.array(z.string()).min(2).max(6),
  answer: z.string().min(1),
});

export const quizDataSchema = z.object({
  questions: z.array(quizQuestionSchema).min(1),
});

export const extractResponseSchema = z.object({
  message: z.string(),
  quiz: z.string(),
});

export type ValidatedQuizData = z.infer<typeof quizDataSchema>;
