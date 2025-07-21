import type { Dictionary } from "../composables/types";

export function resetFormErrors(
  formErrors: Dictionary<boolean>,
): Dictionary<boolean> {
  for (const key in formErrors) {
    formErrors[key] = false;
  }

  return formErrors;
}
