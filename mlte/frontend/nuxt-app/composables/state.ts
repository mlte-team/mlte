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

// --------------------------------------------------------------------------------------------------------------
// Custom Lists
// --------------------------------------------------------------------------------------------------------------

export const useCustomListOptions = async () => {
  const customListOptions = useState<Array<SelectOption>>("customListOptions", () => []);

  const fetchData = async () => {
    const apiData = await getCustomListNames();

    if (apiData) {
      customListOptions.value = [];
      apiData.forEach((name: string) => {
        customListOptions.value.push(new SelectOption(name, name));
      });
    }
  };

  if (customListOptions.value.length === 0) {
    await fetchData();
  }

  return {
    customListOptions,
  };
};

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

  if (QACategoryOptions.value.length === 0) {
    await fetchQACData();
  }

  return {
    QACategoryOptions,
    fetchQACData,
  };
};

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

  if (qualityAttributeOptions.value.length === 0) {
    await fetchQAData();
  }

  return {
    qualityAttributeOptions,
    fetchQAData,
  };
};
