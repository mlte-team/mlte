// artifact-validation.ts - provides functions to validate that JSON artifacts comply with their schemas.

import { Validator } from "jsonschema";

import * as negotiationSchemaData from "~/assets/schema/artifact/negotiation/v0.0.1/schema.json";
import * as specSchemaData from "~/assets/schema/artifact/spec/v0.0.1/schema.json";
import * as validatedSchemaData from "~/assets/schema/artifact/validated/v0.0.1/schema.json";
import * as valueSchemaData from "~/assets/schema/artifact/value/v0.0.1/schema.json";
import * as reportSchemaData from "~/assets/schema/artifact/report/v0.0.1/schema.json";

export function isValidNegotiation(artifact: object): boolean {
  return isValidArtifact(artifact, negotiationSchemaData);
}

export function isValidSpec(artifact: object): boolean {
  return isValidArtifact(artifact, specSchemaData);
}

export function isValidValidatedSpec(artifact: object): boolean {
  return isValidArtifact(artifact, validatedSchemaData);
}

export function isValidValue(artifact: object): boolean {
  return isValidArtifact(artifact, valueSchemaData);
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
