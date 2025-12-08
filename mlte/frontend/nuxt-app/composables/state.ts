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

/**
 * Export the state variable problemTypeOptions to be globally available.
 *
 * problemTypeOptions: List of SelectOption to be used when making a <Select> for Problem Types.
 *
 * @returns {ref<Array<SelectOption>>} problemTypeOptions Ref to global problemTypeOptions
 * @returns {function} fetchProblemTypeData Hook to update problemTypeOptions list with API
 */
export const useProblemTypeOptions = async () => {
  const problemTypeOptions = useState<Array<SelectOption>>(
    "problemTypeOptions",
    () => [],
  );

  const fetchProblemTypeData = async () => {
    const apiData = await getCustomList("problem_types");
    if (apiData) {
      problemTypeOptions.value = [];
      apiData.forEach((entry: CustomListEntry) => {
        problemTypeOptions.value.push(new SelectOption(entry.name, entry.name));
      });
      problemTypeOptions.value.push(new SelectOption("Other", "Other"));
    }
  };

  // On setup, populate the data if it is not present
  if (problemTypeOptions.value.length === 0) {
    await fetchProblemTypeData();
  }

  return {
    problemTypeOptions,
    fetchProblemTypeData,
  };
};

/**
 * Export the state variable tagOptions to be globally available.
 *
 * tagOptions: List of CheckboxOption to be used when making a list of checkboxes for tags.
 *
 * @returns {ref<Array<CheckboxOption>>} tagOptions Ref to global tagOptions
 * @returns {function} fetchTagData Hook to update tagOptions list with API
 */
export const useTagOptions = async () => {
  const tagOptions = useState<Array<CheckboxOption>>("tagOptions", () => []);

  const fetchTagData = async () => {
    const apiData = await getCustomList("tags");
    if (apiData) {
      tagOptions.value = [];
      apiData.forEach((entry: CustomListEntry) => {
        tagOptions.value.push(new CheckboxOption(entry.name, false));
      });
    }
  };

  // On setup, populate the data if it is not present
  if (tagOptions.value.length === 0) {
    await fetchTagData();
  }

  return {
    tagOptions,
    fetchTagData,
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
