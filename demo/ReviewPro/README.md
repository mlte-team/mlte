# Env setup

This demo requires an OpenAI API key in order to access the LLM during its execution. This must be setup in a `demo/ReviewPro/.env` file and will be loaded automatically when the `session.py`  is imported. A SSL cert file is also needed if operating behind a proxy.

```bash
# demo/ReviewPro/.env
OPENAPI_KEY="my_api_key"
# If behind a proxy
SSL_CERT_FILE="my_cert_file"
```