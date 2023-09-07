// artifact-validation.ts - provides functions to validate that JSON artifacts comply with their schemas.

import { Validator } from 'jsonschema';

import * as negotiationSchemaData from '~/assets/schema/artifact/spec/v0.0.1/schema.json';
import * as specSchemaData from '~/assets/schema/artifact/spec/v0.0.1/schema.json';
import * as validatedSchemaData from '~/assets/schema/artifact/spec/v0.0.1/schema.json';
import * as valueSchemaData from '~/assets/schema/artifact/spec/v0.0.1/schema.json';


export function isValidNegotiation(artifactJsonString: string) : boolean {
    return isValidArtifact(artifactJsonString, negotiationSchemaData);
}

export function isValidSpec(artifactJsonString: string) : boolean {
    return isValidArtifact(artifactJsonString, specSchemaData);
}

export function isValidValidatedSpec(artifactJsonString: string) : boolean {
    return isValidArtifact(artifactJsonString, validatedSchemaData);
}

export function isValidValue(artifactJsonString: string) : boolean {
    return isValidArtifact(artifactJsonString, valueSchemaData);
}

// Validates if a given JSON string is a valid JSON artifact for the provided schema.
function isValidArtifact(artifactJsonString: string, schema: object) : boolean {
    let artifactObject = {};
    try {
        artifactObject = JSON.parse(artifactJsonString);
    } catch(e) {
        console.log("INVALID!!! String: " + artifactJsonString + " is not a valid JSON object.");
        return false;
    }

    if(!("body" in artifactObject)) {
        console.log("INVALID!!! Object has no body section.")
        return false;
    }

    let v = new Validator();
    let validation = v.validate(artifactObject.body, schema);
    if(validation.errors.length == 0) {
        console.log("VALID!!!")
        return true;
    } else {
        console.log("INVALID!!!")
        console.log(validation.errors);
        return false;
    }
}
