# Security and data handling

- Use only the official public report URLs in config/sources.json.
- Never add SAP credentials, plant network details, employee records or internal files.
- Keep .env files, credential JSON, SQLite databases and logs outside Git.
- Use Google Application Default Credentials for local cloud authentication; do not paste credential contents into issues or documentation.
- Cloud deployment is optional and not performed by the local pipeline.
- Review staged changes before committing and review outputs before sharing.
- If a credential is accidentally committed, revoke/rotate it through its issuer; deleting a file alone does not remove history.
- Report project defects through a private channel to the repository owner. Do not disclose secrets in public issues.

