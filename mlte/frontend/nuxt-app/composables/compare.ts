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
    differences[key] = [];

    if (!(key in results1) || !(key in results2)) {
      differences[key].push("No matching result.");
    } else {
      if (results1[key].type != results2[key].type) {
        differences[key].push("Status");
      }
      if (results1[key].message != results2[key].message) {
        differences[key].push("Message");
      }
      if (
        (results1[key].evidence_metadata &&
          results2[key].evidence_metadata &&
          results1[key].evidence_metadata.measurement.measurement_class !=
            results2[key].evidence_metadata.measurement.measurement_class) ||
        (!results1[key].evidence_metadata && results2[key].evidence_metadata) ||
        (results1[key].evidence_metadata && !results2[key].evidence_metadata)
      ) {
        differences[key].push("Measurement");
      }

      if (differences[key].length === 0) {
        differences[key].push("None");
      }
    }
  });

  return differences;
}
