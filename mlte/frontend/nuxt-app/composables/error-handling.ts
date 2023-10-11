export function requestErrorAlert(){
  alert(
    "Error encountered while communicating with API. Ensure store is running and allowed-origins is configured correctly.",
  );
}

export function responseErrorAlert() {
  alert(
    "Error encountered in response from API. Check browser and store console for more information.",
  );
}