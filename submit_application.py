#!/usr/bin/env python3
"""
Script to submit B12 application via POST request.
This script is designed to be run in a GitHub Action or CI environment.
"""

import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_signature(body: bytes, secret: str) -> str:
    """Create HMAC-SHA256 signature for the request body."""
    signature = hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


def get_canonical_json(data: dict) -> str:
    """Create compact JSON with sorted keys (canonical form)."""
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False, sort_keys=True)


def main():
    # Get required environment variables
    name = os.environ.get('APPLICATION_NAME')
    email = os.environ.get('APPLICATION_EMAIL')
    resume_link = os.environ.get('APPLICATION_RESUME_LINK')
    repository_link = os.environ.get('GITHUB_REPOSITORY_URL', 
                                     os.environ.get('APPLICATION_REPOSITORY_LINK'))
    action_run_link = os.environ.get('GITHUB_RUN_URL',
                                     os.environ.get('APPLICATION_ACTION_RUN_LINK'))
    
    # Validate required fields
    required_fields = {
        'name': name,
        'email': email,
        'resume_link': resume_link,
        'repository_link': repository_link,
        'action_run_link': action_run_link
    }
    
    missing_fields = [k for k, v in required_fields.items() if not v]
    if missing_fields:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")
    
    # Create timestamp in ISO 8601 format
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Build payload with keys sorted alphabetically
    payload = {
        'action_run_link': action_run_link,
        'email': email,
        'name': name,
        'repository_link': repository_link,
        'resume_link': resume_link,
        'timestamp': timestamp
    }
    
    # Create canonical JSON (compact, sorted keys, UTF-8)
    json_body = get_canonical_json(payload)
    body_bytes = json_body.encode('utf-8')
    
    # Get configuration from environment variables
    signing_secret = os.environ.get('SIGNING_SECRET')
    url = os.environ.get('SUBMISSION_URL')
    
    # Validate configuration
    if not signing_secret:
        raise ValueError("SIGNING_SECRET environment variable is required")
    if not url:
        raise ValueError("SUBMISSION_URL environment variable is required")
    
    # Create signature
    signature = create_signature(body_bytes, signing_secret)
    headers = {
        'Content-Type': 'application/json',
        'X-Signature-256': signature
    }
    
    print(f"Submitting application to {url}")
    print(f"Payload: {json_body}")
    print(f"Signature: {signature}")
    
    response = requests.post(url, data=body_bytes, headers=headers)
    
    # Check response
    if response.status_code == 200:
        result = response.json()
        if result.get('success') and 'receipt' in result:
            receipt = result['receipt']
            print(f"\n✓ Submission successful!")
            print(f"Receipt: {receipt}")
            return receipt
        else:
            raise ValueError(f"Unexpected response format: {response.text}")
    else:
        raise RuntimeError(
            f"Submission failed with status {response.status_code}: {response.text}"
        )


if __name__ == '__main__':
    try:
        receipt = main()
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

