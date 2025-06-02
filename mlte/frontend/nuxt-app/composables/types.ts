interface Dictionary<T> {
  [key: string]: T;
}

// --------------------------------------------------------------------------------------------------------------
// General Artifacts
// --------------------------------------------------------------------------------------------------------------

export interface SelectOption {
  value: string;
  text: string;
}

// --------------------------------------------------------------------------------------------------------------
// General Artifacts
// --------------------------------------------------------------------------------------------------------------

export type Artifact = TestResults;

export class ArtifactHeader {
  constructor(
    public identifier: string = "",
    public creator: string = "",
    public created: number = -1,
    public updated: number = -1,
    public catalog_id: string = "",
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Negotiation Card
// --------------------------------------------------------------------------------------------------------------

export class DataDescriptor {
  constructor(
    public description: string = "",
    public source: string = "",
    public classification: string = "unclassified",
    public access: string = "",
    public labeling_method: string = "",
    public labels: Array<Label> = [new Label()],
    public fields: Array<Field> = [new Field()],
    public rights: string = "",
    public policies: string = "",
  ) {}
}

export class Label {
  constructor(
    public name: string = "",
    public description: string = "",
    public percentage: number = 0,
  ) {}
}

export class Field {
  constructor(
    public name: string = "",
    public description: string = "",
    public type: string = "",
    public expected_values: string = "",
    public missing_values: string = "",
    public special_values: string = "",
  ) {}
}

export class QASDescriptor {
  constructor(
    public identifier: string = "",
    public quality: string = "",
    public stimulus: string = "",
    public source: string = "",
    public environment: string = "",
    public response: string = "",
    public measure: string = "",
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Report
// --------------------------------------------------------------------------------------------------------------

export interface TestResults {
  header: ArtifactHeader;
  body: {
    artifact_type: string;
    test_suite_id: string;
    test_suite: {
      artifact_type: string;
      test_cases: Array<TestCase>;
    };
    results: Dictionary<Result>;
  };
}

export interface TestCase {
  identifier: string;
  goal: string;
  qas_list: Array<string>;
  measurement: object;
  validator: object;
}

export interface Result {
  type: string;
  message: string;
  evidence_metadata: {
    test_case_id: string;
    measurement: {
      measurement_class: string;
      output_class: string;
      additional_data: Dictionary<string>;
    };
  };
}

export class Finding {
  constructor(
    public status: string,
    public measurement: string,
    public test_case_id: string,
    public message: string,
    public qas_list: Array<QualityAttributeScenario>,
  ) {}
}

export interface QualityAttributeScenario {
  id: string;
  qa: string;
}

// --------------------------------------------------------------------------------------------------------------
// Test Catalog
// --------------------------------------------------------------------------------------------------------------

export class TestCatalogEntry {
  constructor(
    public header: ArtifactHeader = new ArtifactHeader(),
    public tags: Array<string> = [],
    public qa_category: string = "",
    public quality_attribute: string = "",
    public code_type: string = "",
    public code: string = "",
    public description: string = "",
    public inputs: string = "",
    public output: string = "",
  ) {}
}
