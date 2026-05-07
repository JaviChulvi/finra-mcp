# Access And Errors

FINRA Query API access is not uniform. Some endpoints may be public, while
others require a token or account entitlements.

## Credential States

`FINRA_API_TOKEN` missing:

- The MCP server may return `MissingCredentialsError`.
- The FINRA request may not be sent.
- Ask the user to configure a token if the requested operation is token-gated.

Token present but rejected:

- FINRA may return `401 Unauthorized`.
- The MCP response usually maps this to `FinraAuthenticationError`.
- Causes include an invalid token, expired token, wrong environment, or missing
  dataset entitlement.

Dataset entitlement missing:

- The tool can be implemented correctly while FINRA denies access.
- Do not repeatedly retry equivalent calls.
- Identify the group, dataset, and operation that requires entitlement.

## Public Versus Restricted Behavior

Do not assume all datasets in a group share the same access policy. A metadata
endpoint may be public while the data endpoint is restricted. A group list from
the bundled catalog may work while live `/datasets` requires a token.

When a user asks whether a tool works:

- If data is returned, validate the data shape and request alignment.
- If FINRA denies access, validate that the error is coherent and explain the
  credential boundary.
- If local validation rejects the request, explain the unsupported input.

## Read-Only Violations

The MCP server should reject payload keys outside the read-only Query API set.
If a user requests an unsupported operation, do not try to force it through a
query tool. State that the server is read-only and scoped to Query API data
access.

Mutating intent includes:

- create
- update
- delete
- submit
- upload
- acknowledge
- subscribe
- unsubscribe
- send
- file transfer workflows outside Query API result downloads

## Reporting Access Failures

Use direct wording:

- "The tool was called, but FINRA denied access."
- "The MCP server requires `FINRA_API_TOKEN` before it can call this endpoint."
- "This verifies error handling, not live data for that restricted dataset."

Avoid saying:

- "The data is correct" when no data was returned.
- "All tools are fully verified" when some tools only returned access errors.
- "The endpoint is public" when the only evidence is a bundled catalog entry.
