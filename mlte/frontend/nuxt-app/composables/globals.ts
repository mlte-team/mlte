// TODO: Pull these from the schema
export const useClassificationOptions = () =>
  useState<Array<object>>("classificationOptions", () => [
    { value: "unclassified", text: "Unclassified" },
    {
      value: "cui",
      text: "Controlled Unclassified Information (CUI)",
    },
    {
      value: "pii",
      text: "Personally Identifiable Information (PII)",
    },
    {
      value: "phi",
      text: "Protected Health Information (PHI)",
    },
    { value: "other", text: "Other" },
  ]);

// TODO: Pull these from the schema
export const useProblemTypeOptions = () =>
  useState<Array<object>>("problemTypeOptions", () => [
    { value: "classification", text: "Classification" },
    { value: "clustering", text: "Clustering" },
    { value: "detection", text: "Detection" },
    { value: "trend", text: "Trend" },
    { value: "alert", text: "Alert" },
    { value: "forecasting", text: "Forecasting" },
    { value: "content_generation", text: "Content Generation" },
    { value: "benchmarking", text: "Benchmarking" },
    { value: "goals", text: "Goals" },
    { value: "other", text: "Other" },
  ]);
