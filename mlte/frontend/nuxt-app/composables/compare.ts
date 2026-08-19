/**
 * Compare two headers and return list of fields that are different.
 *
 * @param {ArtifactHeader} header1 First Artfiact Header to be compared
 * @param {ArtifactHeader} header2 Second Artifact Header to be compared
 * @returns {Array<string>} List of fields that are different
 */
export function compareHeaders(
  header1: ArtifactHeader,
  header2: ArtifactHeader,
) {
  const differences: Array<string> = [];

  if (header1.identifier != header2.identifier) {
    differences.push("Identifier");
  }
  if (header1.timestamp != header2.timestamp) {
    differences.push("Timestamp");
  }
  if (header1.creator != header2.creator) {
    differences.push("Creator");
  }

  if (differences.length === 0) {
    differences.push("None");
  }

  return differences;
}

/**
 * Compare two dictionaries of results and return list of fields that are different.
 *
 * @param {Array<string>} keys List of all keys contained in result1 and result2
 * @param {Dictionary<result>} results1 First dictionary of Results to be compared
 * @param {Dictionary<result>} results2 Second dictionary of Results to be compared
 * @returns {Dictionary<Array<string>>} Dictionary containing a list of fields that are different for each result, for each key in keys
 */
export function compareResults(
  keys: Array<string>,
  results1: Dictionary<Result>,
  results2: Dictionary<Result>,
) {
  const differences: Dictionary<Array<string>> = {};

  keys.forEach((key: string) => {
    const res1 = results1[key];
    const res2 = results2[key];
    const keyDiffs: string[] = [];

    if (!res1 || !res2) {
      keyDiffs.push("No matching result.");
    } else {
      if (res1.type !== res2.type) {
        keyDiffs.push("Status");
      }
      if (res1.message !== res2.message) {
        keyDiffs.push("Message");
      }

      const meta1 = res1.evidence_metadata;
      const meta2 = res2.evidence_metadata;

      if (
        Boolean(meta1) !== Boolean(meta2) ||
        meta1?.measurement?.measurement_class !==
          meta2?.measurement?.measurement_class
      ) {
        keyDiffs.push("Measurement");
      }

      if (keyDiffs.length === 0) {
        keyDiffs.push("None");
      }
    }

    differences[key] = keyDiffs;
  });

  return differences;
}
