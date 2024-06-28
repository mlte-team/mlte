export function requestErrorAlert() {
  alert(
    "Error encountered while communicating with API. Ensure store is running and allowed-origins is configured correctly.",
  );
}

export function handleHttpError(
  errorCode: number,
  errorMessage: string | null,
) {
  if (errorCode === 400) {
    http400(errorMessage);
  } else if (errorCode === 401) {
    http401();
  } else if (errorCode === 403) {
    http403();
  } else if (errorCode === 409) {
    http409();
  } else if (errorCode === 422) {
    http422();
  } else {
    httpOther(errorCode);
  }
}

function http400(errorMessage: string | null) {
  if (errorMessage) {
    alert(errorMessage);
  } else {
    alert("HTTP 400 Bad Request Error");
  }
}

function http401() {
  alert(
    "Token expired. If you have unsaved work, login in a separate tab and try again or refresh to be redirected to login page.",
  );
}

function http403() {
  location.href = "/";
  alert("HTTP 403 Access to requested resource is forbidden.");
}

function http409() {
  alert("Name specified is already in use.");
}

function http422() {
  alert(
    "HTTP 422 Unprocessable Entity. Please contact developers relating to this bug.",
  );
}

function httpOther(errorCode: number) {
  alert(
    "Unexpected HTTP " +
      errorCode +
      " error. Please contact developers relating to this bug.",
  );
}
