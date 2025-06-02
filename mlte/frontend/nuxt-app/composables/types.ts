// --------------------------------------------------------------------------------------------------------------
// Artifacts
// --------------------------------------------------------------------------------------------------------------

export interface Artifact {
  header: ArtifactHeader;
}

export class ArtifactHeader {
  constructor(
    public identifier: string = "",
    public creator: string = "",
    public created: number = -1,
    public updated: number = -1,
    public catalog_id: string = "",
  ) {}
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
    public outputs: string = "",
  ) {}
}
