import requests
import mimetypes
import csv
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get sensitive info from environment variables
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")
token = os.getenv("GITHUB_TOKEN")
enable_attachment_download = os.getenv("ENABLE_ATTACHMENT_DOWNLOAD", "false").lower() == "true"

if not owner or not repo or not token:
    raise ValueError("Please ensure GITHUB_OWNER, GITHUB_REPO, and GITHUB_TOKEN are set in your .env file.")

headers = {"Authorization": f"token {token}"}

# Directory to save attachments
attachment_dir = "attachments"
if enable_attachment_download:
    os.makedirs(attachment_dir, exist_ok=True)

# Regex to identify attachment URLs
# attachment_pattern = re.compile(r"https://[\w./-]+\.(png|jpg|jpeg|gif|pdf|docx|zip|txt|csv|xlsx)")
attachment_pattern = re.compile(r"!\[.*?\]\((https?://github\.com/user-attachments/assets/[^\s]+)\)")


# Filters
# issue_ids_to_include = [1, 5, 10]  # Example: List of issue IDs to include (leave empty to ignore)
issue_ids_to_include = []
title_starts_with = "[Redberry]"  # Example: Filter titles starting with this pattern (leave empty to ignore)

# Connect to github in browser. then open dev tools > application > cookies
# and copy/paste the content of the user_session
session_cookie = os.getenv("GITHUB_COOKIE")
cookies = {
    "user_session": session_cookie,
    # Add more cookie name-value pairs as needed
}

def download_attachment(url, save_dir):
    """Download an attachment and handle missing extensions."""
    try:
        response = requests.get(url, cookies=cookies, stream=True)
        response.raise_for_status()

        # Determine file extension from the Content-Type header
        content_type = response.headers.get("Content-Type", "")
        extension = mimetypes.guess_extension(content_type)
        if not extension:  # Default to .bin if the type is unknown
            extension = ".bin"

        # Use the original filename from the URL, adding the correct extension if needed
        base_name = url.split("/")[-1]
        if not base_name.endswith(extension):
            base_name += extension

        filename = os.path.join(save_dir, base_name)

        # Save the file
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")



# Fetch all issues with pagination
issues = []
page = 1

while True:
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues?page={page}&per_page=100", headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        break

    page_issues = response.json()

    # Break if no more issues are returned
    if not page_issues:
        break

    issues.extend(page_issues)
    page += 1

print(f"Fetched {len(issues)} issues.")

# Export issues and download attachments
with open("issues_with_creation_date_and_filters.csv", "w", newline="") as csvfile:
    fieldnames = ["id", "title", "body", "comments", "attachments", "created_at"]  # Include 'created_at'
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for issue in issues:
        issue_id = issue["id"]
        title = issue["title"]
        body = issue["body"] or ""
        comments_url = issue["comments_url"]
        created_at = issue["created_at"]  # Extract creation date

        # Apply OR filters
        if not (
            (issue_ids_to_include and issue_id in issue_ids_to_include) or
            (title_starts_with and title.startswith(title_starts_with))
        ):
            continue

        # Fetch comments
        comments_response = requests.get(comments_url, headers=headers)
        comments = comments_response.json()
        comment_texts = "\n".join(comment["body"] for comment in comments if comment["body"])

        # Find attachments
        attachments = []
        for content in [body, comment_texts]:
            if content:
                attachments += attachment_pattern.findall(content)
                print(f"Detected attachments: {attachments}")


        # Download attachments
        if enable_attachment_download:
            for attachment_url in attachments:
                download_attachment(attachment_url, attachment_dir)

        # Write issue details to CSV
        writer.writerow({
            "id": issue_id,
            "title": title,
            "body": body,
            "comments": comment_texts,
            "attachments": ", ".join(attachments),
            "created_at": created_at,  # Include creation date in CSV
        })

print(f"Issues exported to 'issues_with_creation_date_and_filters.csv'. Attachments saved to '{attachment_dir}'.")
