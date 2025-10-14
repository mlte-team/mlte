// --------------------------------------------------------------------------------------------------------------
// Schema values
// --------------------------------------------------------------------------------------------------------------

// TODO: Pull these from the schema or a custom list
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

// TODO: Pull these from the schema or a custom list
export const useProblemTypeOptions = () =>
  useState<Array<SelectOption>>("problemTypeOptions", () => [
    { value: "alert", text: "Alert" },
    { value: "benchmarking", text: "Benchmarking" },
    { value: "classification", text: "Classification" },
    { value: "clustering", text: "Clustering" },
    { value: "content_generation", text: "Content Generation" },
    { value: "detection", text: "Detection" },
    { value: "forecasting", text: "Forecasting" },
    { value: "goals", text: "Goals" },
    { value: "sentiment_analysis", text: "Sentiment Analysis" },
    { value: "summarization", text: "Summarization" },
    { value: "translation", text: "Translation" },
    { value: "trend", text: "Trend" },
    { value: "other", text: "Other" },
  ]);

// TODO: Pull these from the schema or a custom list
export const useTagOptions = () =>
  useState<Array<CheckboxOption>>("tagOptions", () => [
    { name: "Audio Analysis", selected: false },
    { name: "Classification", selected: false },
    { name: "Computer Vision", selected: false },
    { name: "Decoder", selected: false },
    { name: "Encoder", selected: false },
    { name: "General", selected: false },
    { name: "Generative Model", selected: false },
    { name: "Infrared", selected: false },
    { name: "NLP", selected: false },
    { name: "Object Detection", selected: false },
    { name: "Sentiment Analysis", selected: false },
    { name: "Regression", selected: false },
    { name: "Segmentation", selected: false },
    { name: "Tabular", selected: false },
    { name: "Time Series", selected: false },
  ]);

// --------------------------------------------------------------------------------------------------------------
// Custom Lists
// --------------------------------------------------------------------------------------------------------------

/**
 * Export the state variable customListOptions to be globally available.
 *
 * customListOptions: List of SelectOptions to be used when making a <Select> for Custom List Names.
 *
 * @returns {Array<SelectOption>} customListOptions Ref to global customListOptions
 */
export const useCustomListOptions = async () => {
  const customListOptions = useState<Array<SelectOption>>(
    "customListOptions",
    () => [],
  );

  // Populate customListOptions with data from the API
  const fetchData = async () => {
    const apiData = await getCustomListNames();

    if (apiData) {
      customListOptions.value = [];
      apiData.forEach((name: string) => {
        customListOptions.value.push(new SelectOption(name, name));
      });
    }
  };

  // On setup, populate the data if it is not present
  if (customListOptions.value.length === 0) {
    await fetchData();
  }

  return {
    customListOptions,
  };
};

// Function to update both QAC and QA with API
export async function updateQAData() {
  const { fetchQACData } = await useQACategoryOptions();
  await fetchQACData();
  const { fetchQAData } = await useQualityAttributeOptions();
  await fetchQAData();
}

/**
 * Export the state variable QACategoryOptions to be globally available.
 *
 * QACategoryOptions: List of QAOptions to be used when making a <Select> for QA Categories.
 *
 * @returns {ref<Array<QAOption>>} QACategoryOptions Ref to global QACategoryOptions
 * @returns {function} fetchQACData Hook to update QACategoryOptions list with API
 */
export const useQACategoryOptions = async () => {
  const QACategoryOptions = useState<Array<QAOption>>(
    "QACategoryOptions",
    () => [],
  );

  const fetchQACData = async () => {
    const apiData = await getCustomList("qa_categories");
    if (apiData) {
      QACategoryOptions.value = [];
      apiData.forEach((entry: CustomListEntry) => {
        QACategoryOptions.value.push(
          new QAOption(entry.name, entry.name, entry.description, entry.parent),
        );
      });
      QACategoryOptions.value.push(new QAOption("Other", "Other", "", ""));
    }
  };

  // On setup, populate the data if it is not present
  if (QACategoryOptions.value.length === 0) {
    await fetchQACData();
  }

  return {
    QACategoryOptions,
    fetchQACData,
  };
};

/**
 * Export the state variable qualityAttributeOptions to be globally available.
 *
 * qualityAttributeOptions: List of QAOptions to be used when making a <Select> for quality attributes.
 *
 * @returns {ref<Array<QAOption>>} qualityAttributeOptions Ref to global qualityAttributeOptions
 * @returns {function} fetchQACData Hook to update qualityAttributeOptions list with API
 */
export const useQualityAttributeOptions = async () => {
  const qualityAttributeOptions = useState<Array<QAOption>>(
    "qualityAttributeOptions",
    () => [],
  );

  const fetchQAData = async () => {
    const apiData = await getCustomList("quality_attributes");
    if (apiData) {
      qualityAttributeOptions.value = [];
      apiData.forEach((entry: CustomListEntry) => {
        qualityAttributeOptions.value.push(
          new QAOption(entry.name, entry.name, entry.description, entry.parent),
        );
      });
    }
  };

  // On setup, populate the data if it is not present
  if (qualityAttributeOptions.value.length === 0) {
    await fetchQAData();
  }

  return {
    qualityAttributeOptions,
    fetchQAData,
  };
};
