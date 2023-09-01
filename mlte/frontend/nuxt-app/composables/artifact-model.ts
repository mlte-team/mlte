
/// Tests
const artifact = parseArtifact('{"body": 1}');
printArtifact(artifact)

function parseArtifact(jsonString: string) : Artifact {
    return JSON.parse(jsonString) as Artifact
}

function printArtifact(data: Artifact) {
    console.log(data.body)
}

//////////////////////////////////////
// Basic Artifact models.
//////////////////////////////////////

interface Artifact {
    header: ArtifactHeader;
    body: any;
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
