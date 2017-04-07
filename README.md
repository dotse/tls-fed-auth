# Federated SCIM Authentication

This repository contains work-in-progress for describing a mechanism how to perform federate authentication for SCIM.

## Requirements

- Mutual authentication (trusted list PKI)
- Authorization via certificate pinning (implicit whitelist)
- Server endpoint discovery via metadata

## Metadata Publication

- Metadata is signed by the federation using JSON Web Signature (RFC 7515) and published via HTTPS.

## Example Use

- Generate self-signed certificate and publish in metadata as issuer. One could also use any webtrust CA and publish the root CA as issuer.
- Fetch all clients or servers from metadata, add all issuers certificates to list of trusted certificate issuers.
- Authenticate connections using trusted certificate issuers.
- Validate authenticated certificates using certificate pinning directives (RFC 7469).

Servers can authenticate connections when terminating TLS and transfer the client certificate to the server application who can validate the connection based on certificate pinning information.
