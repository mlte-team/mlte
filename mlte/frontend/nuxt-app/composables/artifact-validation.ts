// artifact-validation.ts - provides functions to validate that JSON artifacts comply with their schemas.

import { Validator } from "jsonschema";

import * as negotiationSchemaData from "~/assets/schema/artifact/negotiation/v0.0.1/schema.json";
import * as testSuiteSchemaData from "~/assets/schema/artifact/tests/v0.0.1/schema.json";
import * as testResultsSchemaData from "~/assets/schema/artifact/results/v0.0.1/schema.json";
import * as evidenceSchemaData from "~/assets/schema/artifact/evidence/v0.0.1/schema.json";
import * as reportSchemaData from "~/assets/schema/artifact/report/v0.0.1/schema.json";

/** Validate if Negotiation Card object is valid.
 *
 * @param {object} artifact Artifact to validate
 * @returns Boolean specifying if any validation errors were found.
 */
export function isValidNegotiation(artifact: object): boolean {
  return isValidArtifact(artifact, negotiationSchemaData);
}

/** Validate if Test Suite object is valid.
 *
 * @param {object} artifact Artifact to validate
 * @returns Boolean specifying if any validation errors were found.
 */
export function isValidTestSuite(artifact: object): boolean {
  return isValidArtifact(artifact, testSuiteSchemaData);
}

/** Validate if Test Results object is valid.
 *
 * @param {object} artifact Artifact to validate
 * @returns Boolean specifying if any validation errors were found.
 */
export function isValidTestResults(artifact: object): boolean {
  return isValidArtifact(artifact, testResultsSchemaData);
}

/** Validate if Evidence object is valid.
 *
 * @param {object} artifact Artifact to validate
 * @returns Boolean specifying if any validation errors were found.
 */
export function isValidEvidence(artifact: object): boolean {
  return isValidArtifact(artifact, evidenceSchemaData);
}

/** Validate if Report object is valid.
 *
 * @param {object} artifact Artifact to validate
 * @returns Boolean specifying if any validation errors were found.
 */
export function isValidReport(artifact: object): boolean {
  return isValidArtifact(artifact, reportSchemaData);
}

/** Validate if a given JSON string is a valid according to provided schema.
 *
 * @param {object} artifact Artifact to validate
 * @param {object} schema Schema to use to validate
 * @returns {boolean} Boolean specifying if any validation errors were found.
 */
function isValidArtifact(artifact: object, schema: object): boolean {
  if (!("body" in artifact)) {
    return false;
  }

  const v = new Validator();
  const validation = v.validate(artifact.body, schema);
  if (validation.errors.length === 0) {
    return true;
  } else {
    console.log("Errors found in validation check.");
    console.log(validation.errors);
    return false;
  }
}
