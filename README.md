# Installation

## Setup venv

```
python -m venv env
source env/bin/activate # Linux
.\env\Scripts\Activate.ps1   # Windows
```

## Install packages

```
pip install requests 
pip install dotenv
```

### Create .env file

Copy .env.example to .env
Customize the .env settings

**Note:** To download attachments, we must apply some hacking. Open your browser, signin to github. Then open dev tools and get the value of the cookie user_session. Paste that value to the the GITHUB_COOKIE variable in .env file.  
If you want to enable the attachment download, set ENABLE_ATTACHMENT_DOWNLOAD=true in .env file and set GITHUB_COOKIE.

## Filter

Modify github_exporter.py.
The to filters use a OR logic.

```
issue_ids_to_include = [1,2,3]  # use [] to ignore
title_starts_with = "TitleStartsWith"  # Example: Filter titles starting with this pattern (leave empty to ignore)
```

### Run
```
python github_exporter.py
```