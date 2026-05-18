# agent-builder

## Environment variables

Set these variables in your environment or `.env`:

- `GEMINI_API_KEY` (required for AI responses)
- `SECRET_KEY` (recommended for Flask session security)
- `MAX_MESSAGE_LENGTH` (optional, default `2000`)
- `MAX_AGENT_NAME_LENGTH` (optional, default `100`)
- `MAX_AGENT_INSTRUCTIONS_LENGTH` (optional, default `10000`)

### Deployment webhook (PythonAnywhere)

If using the `/update_server` webhook, configure:

- `DEPLOY_WEBHOOK_SECRET`
- `DEPLOY_REPO_PATH`
- `DEPLOY_WSGI_PATH`
- `DEPLOY_EXPECTED_REMOTE_URL` (recommended)
- `DEPLOY_EXPECTED_BRANCH` (optional, default `main`)

The GitHub workflow sends `X-Deploy-Token` using `secrets.DEPLOY_WEBHOOK_SECRET`.
Set `vars.DEPLOY_WEBHOOK_URL` in GitHub repository variables to your webhook endpoint URL.
