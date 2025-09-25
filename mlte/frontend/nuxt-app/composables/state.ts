// TODO: Pull these from the schema
export const useClassificationOptions = () =>
  useState<Array<SelectOption>>("classificationOptions", () => [
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
  useState<Array<SelectOption>>("problemTypeOptions", () => [
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

export const useQACategoryOptions = () =>
  useState<Array<QAOption>>("QAcategoryOptions", () => []);

export async function updateQACategoryOptions() {
  console.log("in state cat");
  const stateOptions = useQACategoryOptions();
  const categoryList = await getCustomList("qa_categories");

  if (categoryList) {
    stateOptions.value = [];
    categoryList.forEach((entry: CustomListEntry) => {
      stateOptions.value.push(
        new QAOption(entry.name, entry.name, entry.description, entry.parent),
      );
    });
    stateOptions.value.push(new QAOption("Other", "Other", "", ""));
  }
}

export const useQualityAttributeOptions = () =>
  useState<Array<QAOption>>("qualityAttributeOptions", () => []);

export async function updateQAOptions() {
  console.log("in state");
  const stateOptions = useQualityAttributeOptions();
  const attributeList = await getCustomList("quality_attributes");

  if (attributeList) {
    stateOptions.value = [];
    attributeList.forEach((entry: CustomListEntry) => {
      stateOptions.value.push(
        new QAOption(entry.name, entry.name, entry.description, entry.parent),
      );
    });
  }
}
