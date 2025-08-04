export interface Dictionary<T> {
  [key: string]: T;
}

export interface TokenData {
  access_token: string;
  token_type: string;
  expires_in: number;
}

// --------------------------------------------------------------------------------------------------------------
// General Page Items
// --------------------------------------------------------------------------------------------------------------

export class TableItem {
  constructor(
    public id: string,
    public timestamp: number,
    public model: string,
    public version: string,
    public test_suite_id?: string,
    public measurement?: string,
    public type?: string,
  ) {}
}

export class QAOption {
  constructor(
    public value: string,
    public text: string,
    public description: string,
    public parent: string,
  ) {}
}

export class SelectOption {
  constructor(
    public value: string,
    public text: string,
  ) {}
}

export interface TagOption {
  name: string;
  selected: boolean;
}

// --------------------------------------------------------------------------------------------------------------
// General Artifacts
// --------------------------------------------------------------------------------------------------------------

export interface Model {
  identifier: string;
  versions: Array<string>;
}

export interface ArtifactModel<
  TBody =
    | NegotiationCardModel
    | TestSuiteModel
    | EvidenceModel
    | TestResultsModel
    | ReportModel,
> {
  header: ArtifactHeader;
  body: TBody;
}

export class ArtifactHeader {
  constructor(
    public identifier: string = "",
    public type: string = "",
    public timestamp: number = -1,
    public creator: string = "",
  ) {}
}

export interface TestCase {
  identifier: string;
  goal: string;
  qas_list: Array<string>;
  measurement: object;
  validator: object;
}

export class TestSuiteModel {
  public readonly artifact_type = "test_suite";
  constructor(public test_cases: Array<TestCase> = []) {}
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

export class TestResultsModel {
  public readonly artifact_type = "test_results";
  constructor(
    public test_suite_id: string = "",
    public test_suite: TestSuiteModel = new TestSuiteModel(),
    public results: Dictionary<Result> = {},
  ) {}
}

export interface EvidenceModel {
  artifact_type: "evidence";
  metadata: {
    test_case_id: string;
    measurement: {
      measurement_class: string;
      output_class: string;
      additional_data: object;
    };
  };
  evidence_class: string;
  value: {
    evidence_type: string;
    data: {
      avg: number;
      min: number;
      max: number;
      unit: string;
    };
  };
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
    public other: Array<string> = [],
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

export interface CustomListEntry {
  name: string;
  description: string;
  parent: string;
}

export class QASDescriptor {
  constructor(
    public quality: string = "",
    public stimulus: string = "<Stimulus>",
    public source: string = "<Source>",
    public environment: string = "<Environment>",
    public response: string = "<Response>",
    public measure: string = "<Response Measure>",
    public identifier?: string,
  ) {}
}

export class NegotiationCardModel {
  public readonly artifact_type = "negotiation_card";
  constructor(
    public system: SystemDescriptor = new SystemDescriptor(),
    public data: Array<DataDescriptor> = [new DataDescriptor()],
    public model: ModelDescriptor = new ModelDescriptor(),
    public system_requirements: Array<QASDescriptor> = [new QASDescriptor()],
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Report
// --------------------------------------------------------------------------------------------------------------

export class CommentDescriptor {
  constructor(public content: string = "") {}
}

export class ReportModel {
  public readonly artifact_type = "report";
  constructor(
    public negotiation_card_id: string = "",
    public negotiation_card: NegotiationCardModel = new NegotiationCardModel(),
    public test_suite_id: string = "",
    public test_suite: TestSuiteModel = new TestSuiteModel(),
    public test_results_id: string = "",
    public test_results: TestResultsModel = new TestResultsModel(),
    public comments: Array<CommentDescriptor> = [new CommentDescriptor()],
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Frontend Report Items
// --------------------------------------------------------------------------------------------------------------

export interface QualityAttributeScenario {
  id: string;
  qa: string;
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
    public email: string = "",
    public full_name: string = "",
    public disabled: boolean = false,
    public role: string = "",
    public groups: Array<Group> = [],
    public password?: string,
  ) {}
}

export interface UserUpdateBody {
  username: string;
  email: string;
  full_name: string;
  disabled: boolean;
  role: string;
  password?: string;
}

export class Permission {
  constructor(
    public resource_type: string,
    public resource_id: string | undefined,
    public method: string,
  ) {}
}

export class PermissionCheckboxOption extends Permission {
  constructor(
    resource_type: string,
    resource_id: string | undefined,
    method: string,
    public selected: boolean,
  ) {
    super(resource_type, resource_id, method);
  }
}

export class Group {
  constructor(
    public name: string = "",
    public permissions: Array<Permission> = [],
  ) {}
}

export class GroupCheckboxOption extends Group {
  constructor(
    name: string,
    permissions: Array<Permission>,
    public selected: boolean,
  ) {
    super(name, permissions);
  }
}
