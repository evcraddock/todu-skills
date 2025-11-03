#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.31.0",
# ]
# requires-python = ">=3.9"
# ///

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
import requests

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from label_utils import get_forgejo_url

def create_comment(repo_name, issue_number, body):
    """Create a comment on a Forgejo issue and return JSON."""
    token = os.environ.get('FORGEJO_TOKEN')
    if not token:
        print(json.dumps({"error": "FORGEJO_TOKEN environment variable not set"}), file=sys.stderr)
        sys.exit(1)

    base_url = get_forgejo_url(repo_name)

    try:
        # Forgejo API endpoint for creating issue comments
        api_url = f"{base_url}/api/v1/repos/{repo_name}/issues/{issue_number}/comments"

        headers = {
            'Authorization': f'token {token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'body': body
        }

        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        comment = response.json()

        # Return comment details
        result = {
            "id": comment['id'],
            "issue_number": issue_number,
            "author": comment['user']['login'],
            "body": comment['body'],
            "created_at": comment['created_at'],
            "updated_at": comment['updated_at'],
            "html_url": comment['html_url'],
            "system": "forgejo",
            "repo": repo_name
        }

        print(json.dumps(result, indent=2))
        return 0

    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e.response, 'text'):
            error_msg = f"{error_msg}: {e.response.text}"
        print(json.dumps({"error": error_msg}), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(description='Create a comment on a Forgejo issue')
    parser.add_argument('--repo', required=True, help='Repository in owner/name format')
    parser.add_argument('--issue', type=int, required=True, help='Issue number')
    parser.add_argument('--body', required=True, help='Comment body/text')

    args = parser.parse_args()

    return create_comment(args.repo, args.issue, args.body)

if __name__ == '__main__':
    sys.exit(main())
