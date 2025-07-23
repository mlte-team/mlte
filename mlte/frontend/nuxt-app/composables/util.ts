import type { Dictionary } from "../composables/types";

export function resetFormErrors(
  formErrors: Dictionary<boolean>,
): Dictionary<boolean> {
  for (const key in formErrors) {
    formErrors[key] = false;
  }

  return formErrors;
}

/**
 * Convert a unix timestamp to a date string.
 *
 * @param {number} timestamp Unix timestamp to be converted
 * @returns Timestamp as date string
 */
export function timestampToString(timestamp: number): string {
  return new Date(timestamp * 1000).toLocaleString("en-US");
}
