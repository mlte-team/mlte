import { isA } from 'ts-type-checked';

/// Tests
const artifact: Artifact = parseArtifact('{"body": 1}');
console.log(artifact);

function parseArtifact(jsonString: string) : Artifact {
    const jsonObj: object = JSON.parse(jsonString);
    if (isA<Artifact>(jsonObj)) {
        console.log("it is an artifact");
        return jsonObj as Artifact;
    } else {
        console.log("it is NOT an artifact");
        throw new Error("Not an artifact!");
    }
}


//////////////////////////////////////
// Basic Artifact models.
//////////////////////////////////////

interface Artifact {
    header: ArtifactHeader;
    body: Value | Spec | ValidatedSpec;
}

interface ArtifactHeader {
    identifier: string;
    type: ArtifactType;
    timestamp: number;
}

enum ArtifactType {
    NEGOTIATION_CARD,
    VALUE,
    SPEC,
    VALIDATED_SPEC,
}

//////////////////////////////////////
// Value models.
//////////////////////////////////////

interface Value {
    artifact_type: ArtifactType.VALUE;
    metadata: EvidenceMetadata;
    value: any;
    value_type: ValueType;
}

interface EvidenceMetadata {
    measurement_type: string;
    identifier: string;
    info: string;
}

enum ValueType {
    INTEGER,
    REAL,
    OPAQUE,
    IMAGE,
}

//////////////////////////////////////
// Spec models.
//////////////////////////////////////

interface Spec {
    artifact_type: ArtifactType.SPEC;
    properties: Array<Property>;
}

interface Property {
    name: string;
    description: string;
    rationale: string;
    conditions: Record<string, Condition>;
}

interface Condition {
    name: string;
    arguments: Array<any>;
    callback: string;
}

//////////////////////////////////////
// ValidatedSpec models.
//////////////////////////////////////

interface ValidatedSpec {
    artifact_type: ArtifactType.VALIDATED_SPEC;
    spec_identifier: string;
    properties: Array<PropertyAndResults>;
}

interface PropertyAndResults {
    results: Record<string, Result>;
}

interface Result {
    type: string;
    message: string;
    metadata: EvidenceMetadata;
}
