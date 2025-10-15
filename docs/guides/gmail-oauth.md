---
title: Get Gmail OAuth Credentials
---

# Get Gmail OAuth Credentials

Follow these concrete steps to obtain the OAuth client credentials required by the Email AI Assistant.

## 1. Open Google Cloud Console

- Visit <https://console.cloud.google.com/> and sign in with the Gmail account you want the assistant to analyze.

## 2. Create or Select a Project

- Click the project selector in the top bar.
- Choose **New Project**, give it a name (e.g., “Email AI Assistant”), then click **Create**.
- Make sure the new project is active—the name should appear in the header.

## 3. Enable the Gmail API

- In the left sidebar, go to **APIs & Services → Library**.
- Search for **Gmail API**, select it, and click **Enable**.

## 4. Configure the OAuth Consent Screen

- Navigate to **APIs & Services → OAuth consent screen**.
- Choose **External** as the user type and click **Create**.
- Fill in:
  - **App name**: e.g., “Email AI Assistant”.
  - **User support email** and **Developer contact information**: your Gmail address.
- Click **Save and Continue** through scopes (you can add `.../auth/gmail.readonly` now or later), and add your Gmail address under **Test users**.
- Finish the remaining steps and save.

## 5. Create OAuth Client Credentials

- Go to **APIs & Services → Credentials**.
- Click **Create Credentials → OAuth client ID**.
- Application type: **Desktop app**.
- Name it (e.g., “Email AI Assistant CLI”) and click **Create**.

## 6. Download the JSON

- A modal appears with your new credentials—click **Download JSON**.
- Rename the file to `credentials.json`.
- Move it to the location expected by the app (default: `~/.credentials/email-ai-assistant/credentials.json`). Create directories if needed:

  ```bash
  mkdir -p ~/.credentials/email-ai-assistant
  mv ~/Downloads/credentials.json ~/.credentials/email-ai-assistant/credentials.json
  chmod 600 ~/.credentials/email-ai-assistant/credentials.json
  ```

## 7. Wire It Into the App

- In the repository root, copy `.env.example` to `.env` if you haven’t already.
- Edit `.env` so it contains:

  ```env
  GOOGLE_APPLICATION_CREDENTIALS=/Users/<you>/.credentials/email-ai-assistant/credentials.json
  PRIMARY_EMAIL=youremail@gmail.com
  ```

## 8. First Run Authentication

- Run `python scripts/run_mvp.py recruiters`.
- A browser window opens to request Gmail access—approve the read-only scope.
- The app writes `token.json` (in the repo root by default) so future runs reuse the credentials.

You now have the Gmail OAuth credentials required to use the Email AI Assistant.
