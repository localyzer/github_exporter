
# How to Create a Fine-Grained Personal Access Token for Exporting Issues

## Step 1: Access GitHub Settings
1. Log in to your GitHub account.
2. Click on your profile picture in the top-right corner and select **Settings**.

## Step 2: Create a Fine-Grained Personal Access Token
1. In the left sidebar, click on **Developer settings**.
2. Select **Personal access tokens**, then choose **Fine-grained tokens**.
3. Click on **Generate new token**.

## Step 3: Configure Token Settings
1. **Token Name**: Provide a descriptive name, e.g., "Export Issues for localyzer/roadmap".
2. **Expiration**: Set an appropriate expiration date based on your needs.

## Step 4: Set Repository Access
1. **Resource Owner**: Select your organization, `localyzer`.
2. **Repository Access**: Choose **Only select repositories**, then select `roadmap`.

## Step 5: Assign Necessary Permissions
To export issues along with their attachments and comments, assign the following permissions:

### Repository Permissions
- **Contents**: Set to **Read-only**. This allows access to the repository contents, which is essential for fetching issue data.
- **Issues**: Set to **Read-only**. This permits reading issue information, including titles, descriptions, and comments.
- **Metadata**: Set to **Read-only**. This grants access to repository metadata, necessary for API interactions.

## Step 6: Generate and Secure the Token
1. After configuring the permissions, click **Generate token**.
2. Copy the token immediately and store it securely, as it won't be displayed again.

## Step 7: Update Your Environment Configuration
1. Open your `.env` file and update the `GITHUB_TOKEN` entry:
   ```plaintext
   GITHUB_TOKEN=your_fine_grained_personal_access_token
   ```
   Replace `your_fine_grained_personal_access_token` with the token you just generated.

## Step 8: Test the Token
Use `curl` to test the token's access:
```bash
curl -H "Authorization: Bearer YOUR_FINE_GRAINED_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/localyzer/roadmap/issues
```
Replace `YOUR_FINE_GRAINED_TOKEN` with your actual token. A successful response indicates correct permissions.

## Additional Considerations
- **Organization Policies**: Ensure that your organization permits the use of fine-grained personal access tokens. Organization owners can manage these settings in the organization's security or access policies.
- **Scope Limitation**: Fine-grained tokens are designed to provide the least privilege necessary. Assign only the permissions required for your task to enhance security.

## Useful Links
- [Introducing Fine-Grained Personal Access Tokens for GitHub](https://github.blog/security/application-security/introducing-fine-grained-personal-access-tokens-for-github/)
- [Fine-Grained Personal Access Token Permissions](https://github.com/orgs/community/discussions/133558)


