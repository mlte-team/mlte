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
    public parent: string | null,
  ) {}
}

export class SelectOption {
  constructor(
    public value: string,
    public text: string,
  ) {}
}

export class CheckboxOption {
  constructor(
    public name: string,
    public selected: boolean,
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// General Artifacts
// --------------------------------------------------------------------------------------------------------------

export interface Model {
  identifier: string;
  versions: Array<string>;
}

export interface Version {
  identifier: string;
}

export interface WriteArtifactResponse<T = ArtifactModel> {
  artifact: T;
}

export interface ArtifactModel<
  T =
    | NegotiationCardModel
    | EvidenceModel
    | TestSuiteModel
    | TestResultsModel
    | ReportModel,
> {
  header: ArtifactHeader;
  body: T;
}

export class ArtifactHeader {
  constructor(
    public identifier: string = "",
    public type: string = "",
    public timestamp: number = -1,
    public creator: string = "",
    public level: string = "version",
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

export class ModelResourcesDescriptor {
  constructor(
    public cpu: string = "0",
    public gpu: string = "0",
    public gpu_memory: string = "0",
    public main_memory: string = "0",
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
    public model_source: string = "",
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
    public purpose: string = "",
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
    public risks: Array<string> = [],
  ) {}
}

export class CustomListEntry {
  constructor(
    public name: string = "",
    public description: string = "",
    public parent: string | null = null,
  ) {}
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
  public readonly artifact_type = "card";
  constructor(
    public system: SystemDescriptor = new SystemDescriptor(),
    public data: Array<DataDescriptor> = [new DataDescriptor()],
    public model: ModelDescriptor = new ModelDescriptor(),
    public system_requirements: Array<QASDescriptor> = [new QASDescriptor()],
  ) {}
}

// --------------------------------------------------------------------------------------------------------------
// Evidence
// --------------------------------------------------------------------------------------------------------------

export class EvidenceModel {
  public readonly artifact_type = "evidence";
  constructor(
    public metadata: EvidenceMetadata = new EvidenceMetadata(),
    public evidence_class: string = "",
    public value:
      | IntegerValueModel
      | RealValueModel
      | OpaqueValueModel
      | ImageValueModel
      | ArrayValueModel
      | StringValueModel = new StringValueModel(),
  ) {}
}

export class EvidenceMetadata {
  constructor(
    public test_case_id: string = "",
    public measurement: MeasurementMetadata = new MeasurementMetadata(),
  ) {}
}

export class IntegerValueModel {
  public readonly evidence_type = "integer";
  constructor(
    public integer: number = -1,
    public unit: string | null = null,
  ) {}
}

export class RealValueModel {
  public readonly evidence_type = "real";
  constructor(
    public real: number = -1,
    public unit: string | null = null,
  ) {}
}

export class OpaqueValueModel {
  public readonly evidence_type = "opaque";
  constructor(public data: Dictionary<unknown>) {}
}

export class ImageValueModel {
  public readonly evidence_type = "image";
  constructor(public data: string = "") {}
}

export class ArrayValueModel {
  public readonly evidence_type = "array";
  constructor(public data: Array<unknown>) {}
}

export class StringValueModel {
  public readonly evidence_type = "string";
  constructor(public string: string = "") {}
}

// --------------------------------------------------------------------------------------------------------------
// Test Suite
// --------------------------------------------------------------------------------------------------------------

export class TestSuiteModel {
  public readonly artifact_type = "suite";
  constructor(public test_cases: Array<TestCaseModel> = []) {}
}

export interface TestCaseModel {
  identifier: string;
  goal: string;
  qas_list: Array<string>;
  measurement: MeasurementMetadata;
  validator: Validator;
}

export class MeasurementMetadata {
  constructor(
    public measurement_class = "",
    public output_class = "",
    public additional_data: Dictionary<string> = {},
  ) {}
}

export interface Validator {
  bool_exp: string;
  bool_exp_str: string;
  thresholds: Array<string>;
  success: string;
  failure: string;
  info: string | null;
  input_types: Array<string>;
  creator_entity: Array<string>;
  creator_function: string;
  creator_args: Array<string>;
}

// --------------------------------------------------------------------------------------------------------------
// Test Results
// --------------------------------------------------------------------------------------------------------------

export class TestResultsModel {
  public readonly artifact_type = "results";
  constructor(
    public test_suite_id: string = "",
    public test_suite: TestSuiteModel = new TestSuiteModel(),
    public results: Dictionary<Result> = {},
  ) {}
}

export interface Result {
  type: string;
  message: string;
  evidence_metadata: EvidenceMetadata;
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
    public updater: string | null = null,
    public updated: number = -1,
    public catalog_id: string = "",
  ) {}
}

export class TestCatalogEntry {
  constructor(
    public header: TestCatalogHeader = new TestCatalogHeader(),
    public tags: Array<string> = [],
    public quality_attribute: string = "",
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
