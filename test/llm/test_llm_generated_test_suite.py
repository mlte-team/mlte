import ast
import os
import re
from pathlib import Path

GENERATED_OUTPUT_DIR = "test/generated_llm_outputs"

REQUIRED_TESTCASE_FIELDS = {
    "identifier",
    "goal",
    "quality_scenarios",
    "validator",
}

OPTIONAL_TESTCASE_FIELDS = {
    "measurement",
    "note",
}

ALLOWED_TESTCASE_FIELDS = REQUIRED_TESTCASE_FIELDS | OPTIONAL_TESTCASE_FIELDS

QAS_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+-qas_\d{3}$")

BASE_ALLOWED_SYMBOLS = {
    "spec",
    "TestSuite",
    "TestCase",
    "ExternalMeasurement",
    "ImportMeasurement",
    "Real",
    "Integer",
    "String",
    "Array",
    "Opaque",
    "Image",
    "ConfusionMatrix",
    "LocalObjectSize",
    "LocalProcessMemoryUtilization",
    "LocalProcessCPUUtilization",
    "NvidiaGPUMemoryUtilization",
    "NvidiaGPUPowerUtilization",
    "Units",
    "validators",
    "model",
    "ProcessMeasurement",
    "ProcessMeasurementGroup",
    "CommonStatistics",
    "CPUStatistics",
    "MemoryStatistics",
    "NvidiaGPUMemoryStatistics",
    "NvidiaGPUPowerStatistics",
    "Measurement",
    "MeasurementMetadata",
}


def test_llm_generated_test_suite() -> None:
    generated_output_filename = os.environ.get(
        "GENERATED_OUTPUT_FILE",
        "llm_generated_test_suite.py",
    )

    generated_source_code = read_generated_output(generated_output_filename)

    assert_generated_output_has_required_format(generated_source_code)

    parsed_generated_module = parse_python_source(generated_source_code)

    assert_mlte_suite_structure(parsed_generated_module)
    assert_allowed_symbol_usage(parsed_generated_module, BASE_ALLOWED_SYMBOLS)
    assert_quality_scenarios_are_well_formed(parsed_generated_module)
    assert_testcases_have_quality_comments(
        generated_source_code,
        parsed_generated_module,
    )
    assert_validators_have_reviewer_comments(
        generated_source_code,
        parsed_generated_module,
    )


def read_generated_output(filename: str) -> str:
    generated_output_directory = os.environ.get(
        "GENERATED_OUTPUT_DIR",
        GENERATED_OUTPUT_DIR,
    )
    generated_output_directory_path = Path(generated_output_directory)
    generated_output_file_path = generated_output_directory_path / filename

    if not generated_output_file_path.exists():
        raise AssertionError(
            f"Generated output file does not exist: {generated_output_file_path}"
        )

    return generated_output_file_path.read_text(encoding="utf-8")


def assert_generated_output_has_required_format(
    generated_source_code: str,
) -> None:
    generated_source_lines = generated_source_code.splitlines()

    if not generated_source_lines:
        raise AssertionError("Generated output is empty")

    first_source_line = generated_source_lines[0]
    last_source_line = generated_source_lines[-1]

    if first_source_line != "spec = TestSuite(":
        raise AssertionError(f"Unexpected first line: {first_source_line!r}")

    if last_source_line != "spec.save(parents=True, force=True)":
        raise AssertionError(f"Unexpected last line: {last_source_line!r}")

    if "```" in generated_source_code:
        raise AssertionError("Generated output contains markdown code fences")


def parse_python_source(generated_source_code: str) -> ast.Module:
    try:
        parsed_generated_module = ast.parse(generated_source_code)
    except SyntaxError as syntax_error:
        raise AssertionError(
            f"Generated output is not valid Python: {syntax_error}"
        ) from syntax_error

    return parsed_generated_module


def assert_mlte_suite_structure(parsed_generated_module: ast.Module) -> None:
    test_suite_calls = find_calls_named(parsed_generated_module, "TestSuite")
    test_case_calls = find_calls_named(parsed_generated_module, "TestCase")

    if not test_suite_calls:
        raise AssertionError("No TestSuite(...) call found")

    if not test_case_calls:
        raise AssertionError("No TestCase(...) calls found")

    test_case_index = 1

    for test_case_call in test_case_calls:
        assert_testcase_structure(test_case_call, test_case_index)
        test_case_index += 1


def assert_testcase_structure(
    test_case_call: ast.Call,
    test_case_index: int,
) -> None:
    test_case_field_names = collect_keyword_names(test_case_call)

    missing_required_fields = REQUIRED_TESTCASE_FIELDS - test_case_field_names
    unsupported_fields = test_case_field_names - ALLOWED_TESTCASE_FIELDS

    if missing_required_fields:
        raise AssertionError(
            f"TestCase #{test_case_index} missing required fields: "
            f"{sorted(missing_required_fields)}"
        )

    if unsupported_fields:
        raise AssertionError(
            f"TestCase #{test_case_index} uses unsupported fields: "
            f"{sorted(unsupported_fields)}"
        )

    validator_expression = get_keyword_value(test_case_call, "validator")

    if validator_expression is not None:
        if not isinstance(validator_expression, ast.Call):
            raise AssertionError(
                f"TestCase #{test_case_index} validator must be a call, "
                f"such as Real.greater_than(...) or validators.<name>(...)"
            )


def assert_allowed_symbol_usage(
    parsed_generated_module: ast.Module,
    allowed_prompt_symbols: set[str],
) -> None:
    used_symbol_roots = collect_symbol_roots(parsed_generated_module)
    unexpected_symbol_roots = used_symbol_roots - allowed_prompt_symbols

    if unexpected_symbol_roots:
        raise AssertionError(
            "Generated output uses symbols outside the prompt's allowed symbols\n"
            f"Unexpected symbols: {sorted(unexpected_symbol_roots)}\n"
            f"Allowed symbols: {sorted(allowed_prompt_symbols)}"
        )


def assert_quality_scenarios_are_well_formed(
    parsed_generated_module: ast.Module,
) -> None:
    validation_failures = []
    test_case_calls = find_calls_named(parsed_generated_module, "TestCase")

    test_case_index = 1

    for test_case_call in test_case_calls:
        quality_scenarios_expression = get_keyword_value(
            test_case_call,
            "quality_scenarios",
        )

        if quality_scenarios_expression is None:
            validation_failures.append(
                f"TestCase #{test_case_index} is missing quality_scenarios"
            )
            test_case_index += 1
            continue

        if not isinstance(quality_scenarios_expression, ast.List):
            validation_failures.append(
                f"TestCase #{test_case_index} quality_scenarios must be "
                "a list of QAS ID strings"
            )
            test_case_index += 1
            continue

        quality_scenario_ids = extract_top_level_string_literals(
            quality_scenarios_expression
        )

        if not quality_scenario_ids:
            validation_failures.append(
                f"TestCase #{test_case_index} quality_scenarios must contain "
                "at least one QAS ID string"
            )
            test_case_index += 1
            continue

        if len(quality_scenario_ids) != len(quality_scenarios_expression.elts):
            validation_failures.append(
                f"TestCase #{test_case_index} quality_scenarios must contain "
                "only string literal QAS IDs"
            )
            test_case_index += 1
            continue

        duplicate_quality_scenario_ids = find_duplicates(quality_scenario_ids)

        if duplicate_quality_scenario_ids:
            validation_failures.append(
                f"TestCase #{test_case_index} quality_scenarios contains "
                f"duplicate IDs: {sorted(duplicate_quality_scenario_ids)}"
            )

        malformed_quality_scenario_ids = set()

        for quality_scenario_id in quality_scenario_ids:
            if not QAS_ID_PATTERN.match(quality_scenario_id):
                malformed_quality_scenario_ids.add(quality_scenario_id)

        if malformed_quality_scenario_ids:
            validation_failures.append(
                f"TestCase #{test_case_index} quality_scenarios contains "
                f"malformed QAS IDs: {sorted(malformed_quality_scenario_ids)}"
            )

        test_case_index += 1

    if validation_failures:
        raise AssertionError("\n".join(validation_failures))


def assert_testcases_have_quality_comments(
    generated_source_code: str,
    parsed_generated_module: ast.Module,
) -> None:
    generated_source_lines = generated_source_code.splitlines()
    test_case_calls = find_calls_named(parsed_generated_module, "TestCase")
    validation_failures = []

    for test_case_call in test_case_calls:
        test_case_line_number = test_case_call.lineno
        previous_comment = get_previous_nonblank_line(
            generated_source_lines,
            test_case_line_number - 1,
        )

        if not is_quality_comment(previous_comment):
            validation_failures.append(
                f"TestCase near line {test_case_line_number} is missing "
                "a quality comment immediately above TestCase(...)"
            )

    if validation_failures:
        raise AssertionError("\n".join(validation_failures))


def assert_validators_have_reviewer_comments(
    generated_source_code: str,
    parsed_generated_module: ast.Module,
) -> None:
    generated_source_lines = generated_source_code.splitlines()
    test_case_calls = find_calls_named(parsed_generated_module, "TestCase")
    validation_failures = []

    for test_case_call in test_case_calls:
        custom_validator_name = get_custom_validator_name(test_case_call)

        if custom_validator_name is None:
            continue

        test_case_line_number = test_case_call.lineno
        reviewer_comment = get_previous_nonblank_line(
            generated_source_lines,
            test_case_line_number - 2,
        )
        expected_reviewer_comment_prefix = f"# Reviewer: implement validators.{custom_validator_name}(...) because "

        if not reviewer_comment.startswith(expected_reviewer_comment_prefix):
            validation_failures.append(
                f"Custom validator TestCase near line {test_case_line_number} "
                "is missing reviewer comment: "
                f"{expected_reviewer_comment_prefix}<reason>"
            )

    if validation_failures:
        raise AssertionError("\n".join(validation_failures))


def is_quality_comment(comment_line: str) -> bool:
    if not comment_line.startswith("# "):
        return False

    return "test case" in comment_line.lower()


def get_custom_validator_name(test_case_call: ast.Call) -> str | None:
    validator_expression = get_keyword_value(test_case_call, "validator")

    if not isinstance(validator_expression, ast.Call):
        return None

    validator_function = validator_expression.func

    if not isinstance(validator_function, ast.Attribute):
        return None

    validator_root = validator_function.value

    if not isinstance(validator_root, ast.Name):
        return None

    if validator_root.id != "validators":
        return None

    return validator_function.attr


def get_keyword_value(
    function_call: ast.Call,
    keyword_name: str,
) -> ast.expr | None:
    for keyword_argument in function_call.keywords:
        if keyword_argument.arg == keyword_name:
            return keyword_argument.value

    return None


def collect_keyword_names(function_call: ast.Call) -> set[str]:
    keyword_names = set()

    for keyword_argument in function_call.keywords:
        if keyword_argument.arg is not None:
            keyword_names.add(keyword_argument.arg)

    return keyword_names


def extract_top_level_string_literals(
    collection_expression: ast.List | ast.Tuple | ast.Set,
) -> list[str]:
    string_values = []

    for collection_element in collection_expression.elts:
        if isinstance(collection_element, ast.Constant):
            if isinstance(collection_element.value, str):
                string_values.append(collection_element.value)

    return string_values


def find_duplicates(values: list[str]) -> set[str]:
    seen_values = set()
    duplicate_values = set()

    for value in values:
        if value in seen_values:
            duplicate_values.add(value)
        else:
            seen_values.add(value)

    return duplicate_values


def find_calls_named(
    parsed_generated_module: ast.Module,
    function_name: str,
) -> list[ast.Call]:
    matching_calls = []

    for syntax_node in ast.walk(parsed_generated_module):
        if not isinstance(syntax_node, ast.Call):
            continue

        call_name = get_call_name(syntax_node)

        if call_name == function_name:
            matching_calls.append(syntax_node)

    return matching_calls


def get_call_name(function_call: ast.Call) -> str | None:
    called_function = function_call.func

    if isinstance(called_function, ast.Name):
        return called_function.id

    if isinstance(called_function, ast.Attribute):
        return called_function.attr

    return None


def collect_symbol_roots(parsed_generated_module: ast.Module) -> set[str]:
    symbol_roots = set()

    for syntax_node in ast.walk(parsed_generated_module):
        symbol_root = get_symbol_root(syntax_node)

        if symbol_root is not None:
            symbol_roots.add(symbol_root)

    return symbol_roots


def get_symbol_root(syntax_node: ast.AST) -> str | None:
    if isinstance(syntax_node, ast.Name):
        return syntax_node.id

    if isinstance(syntax_node, ast.Attribute):
        return get_attribute_root(syntax_node)

    return None


def get_attribute_root(attribute_node: ast.Attribute) -> str | None:
    current_node: ast.expr = attribute_node

    while isinstance(current_node, ast.Attribute):
        current_node = current_node.value

    if isinstance(current_node, ast.Name):
        return current_node.id

    return None


def get_previous_nonblank_line(
    source_lines: list[str],
    start_line_index: int,
) -> str:
    current_line_index = start_line_index - 1

    while current_line_index >= 0:
        current_line = source_lines[current_line_index].strip()

        if current_line:
            return current_line

        current_line_index -= 1

    return ""
