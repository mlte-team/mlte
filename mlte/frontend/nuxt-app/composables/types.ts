export interface artifactHeader {
  identifier: string;
  creator: string;
  created: Number;
  updated: Number;
  catalog_id: string;
}

export class testCatalogEntry {
  header: artifactHeader;
  tags: Array<string>;
  qa_category: string;
  quality_attribute: string;
  code_type: string;
  code: string;
  description: string;
  inputs: string;
  output: string;

  constructor(){
    this.header = {
      identifier: "",
      creator: "",
      created: -1,
      updated: -1,
      catalog_id: "",
    },
    this.tags = [];
    this.qa_category = "";
    this.quality_attribute = "";
    this.code_type = "";
    this.code = "";
    this.description = "";
    this.inputs = "";
    this.output = ""
  }
}
