# Federated SCIM Authentication

This repository contains work-in-progress for describing a mechanism how to perform federate authentication for SCIM.

## Requirements

- Mutual authentication (trusted list PKI)
- Authorization via certificate pinning (implicit whitelist)
- Server endpoint discovery via metadata


## Example Use

- Generate self-signed certificate and publish in metadata as authn/authz
- Fetch all clients or servers from metadata, add all authn certificates to list of trusted certificate issuers.
- Authenticate connections using trusted certificate issuers.
- Authorized connections via authz data.

Servers can authenticate connections when terminating TLS and transfer the client certificate to the server application who can authorize the connection based on authz information (certificate pinning).
