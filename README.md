# B12 Application Submission

This repository contains the Python script and GitHub Action workflow for submitting an application to B12.

## Setup

1. **Fork or clone this repository** to your GitHub account.

2. **Create a `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and ensure the values are correct:
   - `APPLICATION_NAME`: Your full name
   - `APPLICATION_EMAIL`: Your email address
   - `APPLICATION_RESUME_LINK`: URL to your resume (PDF, HTML, or LinkedIn profile)
   - `SIGNING_SECRET`: The signing secret for HMAC-SHA256 (default: `hello-there-from-b12`)
   - `SUBMISSION_URL`: The URL to POST submissions to (default: `https://b12.io/apply/submission`)

3. **Set up GitHub Secrets** in your repository settings (Settings → Secrets and variables → Actions):
   - `APPLICATION_NAME`: Your full name
   - `APPLICATION_EMAIL`: Your email address
   - `APPLICATION_RESUME_LINK`: URL to your resume (PDF, HTML, or LinkedIn profile)
   - `SIGNING_SECRET`: The signing secret (same value as in `.env`)
   - `SUBMISSION_URL`: The submission URL (same value as in `.env`)

4. **Trigger the workflow**:
   - The workflow runs automatically on pushes to `main` or `master` branches
   - Or manually trigger it via the "Actions" tab → "Submit B12 Application" → "Run workflow"

## Files

- `submit_application.py`: Main Python script that handles the POST request to B12's submission endpoint
- `.github/workflows/submit.yml`: GitHub Actions workflow configuration
- `requirements.txt`: Python dependencies
- `.env.example`: Example environment variables file (copy to `.env` for local development)

## How it works

1. The GitHub Action sets up the Python environment and installs dependencies
2. It constructs the repository URL and action run URL automatically
3. The Python script:
   - Creates a canonical JSON payload with all required fields
   - Generates an HMAC-SHA256 signature using the signing secret
   - POSTs the request to `https://b12.io/apply/submission`
   - Prints the receipt upon successful submission

## Testing locally

1. **Create a `.env` file** (copy from `.env.example`) and edit it with your values:
   ```bash
   cp .env.example .env
   # Edit .env with your application details
   ```

2. **For local testing**, you'll also need to set these additional environment variables (these are automatically set by GitHub Actions):
   ```bash
   export APPLICATION_REPOSITORY_LINK="https://github.com/yourusername/repo"
   export APPLICATION_ACTION_RUN_LINK="https://github.com/yourusername/repo/actions/runs/123"
   ```
   
   Or you can add them to your `.env` file:
   ```
   APPLICATION_REPOSITORY_LINK=https://github.com/yourusername/repo
   APPLICATION_ACTION_RUN_LINK=https://github.com/yourusername/repo/actions/runs/123
   ```

3. **Run the script**:
   ```bash
   python submit_application.py
   ```

## Notes

- The script creates a canonical JSON format (sorted keys, compact separators, UTF-8 encoded)
- The signature is generated using HMAC-SHA256 with the secret from the `SIGNING_SECRET` environment variable
- The submission URL is read from the `SUBMISSION_URL` environment variable
- The timestamp is generated in ISO 8601 format with UTC timezone
- The script loads environment variables from a `.env` file if present (using `python-dotenv`)

