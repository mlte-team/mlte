import Papa from "papaparse";
import type { z } from "zod";

export interface CsvParseError {
  row: number;
  messages: string[];
}

/**
 * Composable for parsing and validating CSV files against a Zod schema.
 *
 * @template T - The Zod schema type
 * @param schema - Zod schema that will be used to parse each CSV row
 * @returns Object containing reactive state and parsing controls:
 *   - `rows`: Ref containing successfully parsed and validated rows.
 *   - `errors`: Ref containing row-level validation and parsing errors.
 *   - `isParsing`: Ref indicating if file processing is currently active.
 *   - `parseFile`: Async function to process a file and return local `{ data, errors }`.
 *   - `reset`: Function to clear current `rows` and `errors` reactive state.
 */
export function parseCsv<TSchema extends z.ZodType>(schema: TSchema) {
  type ParsedData = z.infer<TSchema>;

  const rows = ref<ParsedData[]>([]) as Ref<ParsedData[]>;
  const errors = ref<CsvParseError[]>([]);
  const isParsing = ref(false);

  const parseFile = (
    file: File,
  ): Promise<{ data: ParsedData[]; errors: CsvParseError[] }> => {
    isParsing.value = true;
    rows.value = [];
    errors.value = [];

    return new Promise((resolve) => {
      Papa.parse<Record<string, unknown>>(file, {
        header: true,
        dynamicTyping: false,
        skipEmptyLines: true,
        complete: (results) => {
          const validRows: ParsedData[] = [];
          const parseErrors: CsvParseError[] = [];

          results.data.forEach((row, index) => {
            const parsed = schema.safeParse(row);
            if (parsed.success) {
              validRows.push(parsed.data);
            } else {
              parseErrors.push({
                row: index + 1,
                messages: parsed.error.issues.map((issue) => issue.message),
              });
            }
          });

          rows.value = validRows;
          errors.value = parseErrors;
          isParsing.value = false;

          resolve({ data: validRows, errors: parseErrors });
        },
        error: (err) => {
          isParsing.value = false;
          errors.value = [{ row: 0, messages: [err.message] }];
          resolve({ data: [], errors: errors.value });
        },
      });
    });
  };

  const resetCsv = () => {
    rows.value = [];
    errors.value = [];
    isParsing.value = false;
  };

  return {
    rows,
    errors,
    isParsing,
    parseFile,
    resetCsv,
  };
}
