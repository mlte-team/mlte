// artifact-validation.ts - provides functions to validate that JSON artifacts comply with their schemas.

import { Validator } from "jsonschema";

import * as negotiationSchemaData from "~/assets/schema/artifact/negotiation/v0.0.1/schema.json";
import * as testSuiteSchemaData from "~/assets/schema/artifact/tests/v0.0.1/schema.json";
import * as testResultsSchemaData from "~/assets/schema/artifact/results/v0.0.1/schema.json";
import * as evidenceSchemaData from "~/assets/schema/artifact/evidence/v0.0.1/schema.json";
import * as reportSchemaData from "~/assets/schema/artifact/report/v0.0.1/schema.json";

export function isValidNegotiation(artifact: object): boolean {
  return isValidArtifact(artifact, negotiationSchemaData);
}

export function isValidTestSuite(artifact: object): boolean {
  return isValidArtifact(artifact, testSuiteSchemaData);
}

export function isValidTestResults(artifact: object): boolean {
  return isValidArtifact(artifact, testResultsSchemaData);
}

export function isValidEvidence(artifact: object): boolean {
  return isValidArtifact(artifact, evidenceSchemaData);
}

export function isValidReport(artifact: object): boolean {
  return isValidArtifact(artifact, reportSchemaData);
}

// Validates if a given JSON string is a valid JSON artifact for the provided schema.
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
