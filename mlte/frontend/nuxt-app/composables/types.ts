export interface Dictionary<T> {
  [key: string]: T;
}

// --------------------------------------------------------------------------------------------------------------
// General Page Items
// --------------------------------------------------------------------------------------------------------------

export class QAOption {
  constructor(
    public value: string,
    public text: string,
    public description: string,
    public parent: string,
  ) {}
}

export interface SelectOption {
  value: string;
  text: string;
}

export interface TagOption {
  name: string;
  selected: boolean;
}

// --------------------------------------------------------------------------------------------------------------
// General Artifacts
// --------------------------------------------------------------------------------------------------------------

export type Artifact = TestResults;

export class ArtifactHeader {
  constructor(
    public identifier: string = "",
    public type: string = "",
    public timestamp: number = -1,
    public creator: string = "",
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Negotiation Card
// --------------------------------------------------------------------------------------------------------------

export class MetricDescriptor {
  constructor(
    public description: string = "",
    public baseline: string = "",
  ) {}
}

export class GoalDescriptor {
  constructor(
    public description: string = "",
    public metrics: Array<MetricDescriptor> = [new MetricDescriptor()],
  ) {}
}

export class RiskDescriptor {
  constructor(
    public fp: string = "",
    public fn: string = "",
    public other: string = "",
  ) {}
}

export class ModelResourcesDescriptor {
  constructor(
    public cpu: string = "0",
    public gpu: string = "0",
    public memory: string = "0",
    public storage: string = "0",
  ) {}
}

export class ModelIODescriptor {
  constructor(
    public name: string = "",
    public description: string = "",
    public type: string = "",
    public expected_values: string = "",
  ) {}
}

export class ModelDescriptor {
  constructor(
    public development_compute_resources: ModelResourcesDescriptor = new ModelResourcesDescriptor(),
    public deployment_platform: string = "",
    public capability_deployment_mechanism: string = "",
    public input_specification: Array<ModelIODescriptor> = [new ModelIODescriptor()], // eslint-disable-line
    public output_specification: Array<ModelIODescriptor> = [new ModelIODescriptor()], // eslint-disable-line
    public production_compute_resources: ModelResourcesDescriptor = new ModelResourcesDescriptor(),
  ) {}
}

export class LabelDescriptor {
  constructor(
    public name: string = "",
    public description: string = "",
    public percentage: number = 0,
  ) {}
}

export class FieldDescriptor {
  constructor(
    public name: string = "",
    public description: string = "",
    public type: string = "",
    public expected_values: string = "",
    public missing_values: string = "",
    public special_values: string = "",
  ) {}
}

export class DataDescriptor {
  constructor(
    public description: string = "",
    public source: string = "",
    public classification: string = "unclassified",
    public access: string = "",
    public labeling_method: string = "",
    public labels: Array<LabelDescriptor> = [new LabelDescriptor()],
    public fields: Array<FieldDescriptor> = [new FieldDescriptor()],
    public rights: string = "",
    public policies: string = "",
  ) {}
}

export class SystemDescriptor {
  constructor(
    public goals: Array<GoalDescriptor> = [new GoalDescriptor()],
    public problem_type: string = "classification",
    public task: string = "",
    public usage_context: string = "",
    public risks: RiskDescriptor = new RiskDescriptor(),
  ) {}
}

// Not currently used
export class NegotiationCardDataModel {
  constructor(
    public system: SystemDescriptor = new SystemDescriptor(),
    public data: Array<DataDescriptor> = [new DataDescriptor()],
    public model: ModelDescriptor = new ModelDescriptor(),
    public system_requirements: Array<QASDescriptor> = [new QASDescriptor()],
  ) {}
}

// Not currently used
export class NegotiationCardModel {
  constructor(
    public artifact_type: string = "negotiation_card",
    public nc_data: NegotiationCardDataModel = new NegotiationCardDataModel(),
  ) {}
}

export class QASDescriptor {
  constructor(
    public identifier?: string,
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

export interface CatalogReply {
  id: string;
  read_only: boolean;
  type: string;
}

export class TestCatalogHeader {
  constructor(
    public identifier: string = "",
    public creator: string = "",
    public created: number = -1,
    public updater: string = "",
    public updated: number = -1,
    public catalog_id: string = "",
  ) {}
}

export class TestCatalogEntry {
  constructor(
    public header: TestCatalogHeader = new TestCatalogHeader(),
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

// --------------------------------------------------------------------------------------------------------------
// Profile Management
// --------------------------------------------------------------------------------------------------------------

export class User {
  constructor(
    public username: string = "",
    public password?: string,
    public email: string = "",
    public full_name: string = "",
    public disabled: boolean = false,
    public role: string = "",
    public groups: Array<Group> = [],
  ) {}
}

export interface UserUpdateBody {
  username: string;
  password?: string;
  email: string;
  full_name: string;
  disabled: boolean;
  role: string;
}

export interface PermissionCheckboxOption extends Permission {
  selected: boolean;
}

export class Permission {
  constructor(
    public resource_id: string | undefined = "",
    public resource_type: string = "",
    public method: string = "",
  ) {}
}

export interface GroupCheckboxOption extends Group {
  selected: boolean;
}

export class Group {
  constructor(
    public name: string = "",
    public permissions: Array<Permission> = [],
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Backend Internals
// --------------------------------------------------------------------------------------------------------------

export interface CustomListEntry {
  name: string;
  description: string;
  parent: string;
}
