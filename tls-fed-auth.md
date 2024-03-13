%%%

    title = "Federated TLS Authentication"
    abbrev = "FedTLS"
    category = "std"
    ipr = "trust200902"
    submissiontype = "independent"
    area = "Internet"
    date = 2024-02-16T00:00:00Z

    [seriesInfo]
    status = "informational"
    name = "Internet-Draft"
    value = "draft-halen-fed-tls-auth-08"
    stream = "independent"

    [[author]]
    initials="J."
    surname="Schlyter"
    fullname="Jakob Schlyter"
    organization="Kirei AB"
        [author.address]
        email="jakob@kirei.se"

    [[author]]
    initials="S."
    surname="Halén"
    fullname="Stefan Halén"
    organization="The Swedish Internet Foundation"
        [author.address]
        email="stefan.halen@internetstiftelsen.se"

%%%

.# Abstract

This document describes the Federated TLS Authentication (FedTLS) protocol, enabling secure end-to-end communication within a federated environment. Both clients and servers perform mutual TLS authentication, establishing trust based on a centrally managed trust anchor published by the federation. Additionally, FedTLS ensures unambiguous identification of entities, as only authorized members within the federation can publish metadata, further mitigating risks associated with unauthorized entities impersonating legitimate participants. This framework promotes seamless and secure interoperability across different trust domains adhering to common policies and standards within the federation.

{mainmatter}


# Introduction

This document outlines the Federated TLS Authentication (FedTLS) protocol, which facilitates secure end-to-end communication between two parties within a federation. Both the client and server undergo mutual TLS authentication (as defined in [@!RFC8446]), establishing a robust foundation of trust. This trust relies on a central trust anchor held and published by the federation, acting as a trusted third party connecting distinct trust domains under a common set of policies and standards.

The FedTLS framework leverages a centralized repository of federation metadata to ensure secure communication between servers and clients within the federation. This repository includes information about public keys, certificate issuers, and additional entity details, such as organizational information and service descriptions. This centralized approach simplifies certificate management, promotes interoperability, and establishes trust within the federation. By directly accessing the federation metadata, efficient connections are established, eliminating manual configuration even for new interactions.

Without a FedTLS federation, implementing mutual TLS authentication often requires organizations to establish their own PKI infrastructure (or rely on third-party CAs) to issue and validate client certificates, leading to complexity and administrative burden. FedTLS allows the use of self-signed certificates, potentially reducing costs and administrative overhead. While self-signed certificates inherently lack the trust level of certificates issued by trusted CAs, the strong trust within the FedTLS framework is established through several mechanisms, including public key pinning [@!RFC7469] and member vetting procedures. This ensures the validity and authenticity of self-signed certificates within the federation, fostering secure communication without compromising trust.

The Swedish education sector illustrates the value of FedTLS by securing user lifecycle management endpoints through this framework. This successful collaboration between school authorities and service providers highlights FedTLS's ability to enable trust, simplify operations, and strengthen security within federated environments.


##  Reserved Words

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [@!RFC2119].


## Terminology

-   **Federation**: A trusted network of entities that adhere to common security policies and standards,using FedTLS for secure communication.
-   **Federation Metadata**: A centralized repository storing critical information about all entities within the federation.
-   **Member Metadata**: Information about entities associated with a specific member within the federation.
-   **Federation Member**: An entity that has been approved to join the federation and can leverage FedTLS for secure communication with other members.
-   **Federation Operator**: The entity responsible for the overall operation and management of the federation, including managing the federation metadata, enforcing security policies, and onboarding new members.
-   **Member Vetting**: The process of verifying and approving applicants to join the federation, ensuring they meet security and trustworthiness requirements.
-   **Trust Anchor**: The federation's root of trust is established by the federation metadata signing certificate, which verifies the federation metadata and allows participants to confidently rely on the information it contains.


# Federation Chain of Trust

Federation members submit member metadata to the federation. Both the authenticity of the submitted member metadata and the submitting member need to be ensured by the federation. The specific methods for achieving this are beyond the scope of this document.

The federation operator aggregates, signs, and publishes the federation metadata, which combines all members' member metadata with some additional information added by the federation. By trusting the federation and its certificate, federation members trust the information contained within the federation metadata.

The trust anchor for the federation is established through the federation's signing certificate, which in turn needs to be securely distributed and verified. The distribution and verification methods for the federation's certificate are outside the scope of this document.


# Authentication

All communication established within the federation leverages mutual Transport Layer Security (TLS) authentication, as defined in [@!RFC8446]. This mechanism ensures the authenticity of both communicating parties, establishing a robust foundation for secure data exchange.


## Public Key Pinning

To further fortify this trust and mitigate risks associated with fraudulent certificates issued by unauthorized entities, the federation implements public key pinning as specified in [@!RFC7469]. Public key pinning associates a unique public key with each endpoint within the federation, stored in the federation metadata. During connection establishment, clients and servers validate the received certificate against the pre-configured public key pins retrieved from the federation metadata. This effectively thwarts attempts to utilize fraudulent certificates impersonating legitimate endpoints.


## Pin Discovery and Preloading

Peers in the federation retrieve these unique public key pins, serving as pre-configured trust parameters, from the federation metadata. The federation MUST facilitate the discovery process, enabling peers to identify the relevant pins for each endpoint. Information such as organization, tags, and descriptions within the federation metadata aids in this discovery.

Before initiating any connection, both clients and servers preload the chosen pins in strict adherence to the guidelines outlined in section 2.7 of [@!RFC7469]. This preloading ensures connections only occur with endpoints possessing matching public keys, effectively blocking attempts to use fraudulent certificates.


## Verification of Received Certificates

Upon connection establishment, both endpoints (client and server) must either leverage public key pinning or validate the received certificate against the published pins. Additionally, the federation metadata contains issuer information, which implementations MAY optionally use to verify certificate issuers. This step remains at the discretion of each individual implementation.

In scenarios where a TLS session terminates independent of the application (e.g., via a reverse proxy), the termination point can utilize optional untrusted TLS client certificate authentication or validate the certificate issuer itself. Depending on the specific implementation, pin validation can then be deferred to the application itself, assuming the peer certificate is appropriately transferred (e.g., via an HTTP header).


## Failure to Validate

It is crucial to note that failure to validate a received certificate against the established parameters, whether through pinning or issuer verification, results in immediate termination of the connection. This strict approach ensures only authorized and secure communication channels are established within the federation.


# Federation Metadata

Federation metadata is published as a JWS [@!RFC7515]. The payload contains statements
about federation members entities.

Metadata is used for authentication and service discovery. A client select a server based on metadata claims (e.g., organization, tags). The client then use the selected server claims base_uri, pins and if needed issuers to establish a connection.

Upon receiving a connection, a server validates the received client certificate using the client's published pins. Server MAY also check other claims such as organization and tags to determine if the connections is accepted or terminated.


## Federation Metadata claims

This section defines the set of claims that can be included in metadata.

-   version (REQUIRED)

    Schema version follows semantic versioning (https://semver.org)

-   cache_ttl (OPTIONAL)

    Specifies the duration (in seconds) for caching the downloaded federation metadata. This enables caching independent of specific HTTP implementations or configurations, beneficial for scenarios where the underlying communication mechanism is not solely HTTP-based.

-   Entities (REQUIRED)

    List of entities (see (#entities))


### Entities

Metadata contains a list of entities that may be used for communication within the federation. Each entity describes one or more endpoints owned by a member. An entity has the following properties:

-   entity_id (REQUIRED)

    A URI that uniquely identifies the entity. This identifier MUST NOT collide with any other entity_id within the system or any external systems that the entity might interact with.

    Example: "https://example.com"

-   organization (OPTIONAL)

    A name identifying the organization that the entity's metadata represents. The FedTLS federation operator MUST ensure a mechanism is in place to verify that the organization claim corresponds to the rightful owner of the information exchanged between nodes. This is crucial for the trust model, ensuring certainty about the identities of the involved parties. The federation operator SHOULD choose an approach that best suits the specific needs and trust model of the federation.

    Example: "Example Org".

-   issuers (REQUIRED)

    A list of certificate issuers that are allowed to issue certificates for the entity's endpoints. For each issuer, the issuer's root CA certificate is included in the x509certificate property (PEM-encoded).

-   servers (OPTIONAL)

    List of the entity's servers (see (#servers-clients)).

-   clients (OPTIONAL)

    List of the entity's clients (see (#servers-clients)).


#### Servers / Clients

A list of the entity's servers and clients.

-   description (OPTIONAL)

    A human readable text describing the server or client.

    Example: "SCIM Server 1"

-   base_uri (OPTIONAL)

    The base URL of the server (hence required for endpoints describing servers).

    Example: "https://scim.example.com/"

-   pins (REQUIRED)

    A list of Public Key Pins [@!RFC7469]. Each pin has the following properties:

    -   alg (REQUIRED)

        The name of the cryptographic hash algorithm. The only allowed value is "sha256".

        Example: "sha256"

    -   digest (REQUIRED)

        The public key of the end-entity certificate converted to a Subject Public Key Information (SPKI) fingerprint, as specified in section 2.4 of [@!RFC7469]. For clients, the digest MUST be globally unique for unambiguous identification. However, within the same entity_id object, the same digest MAY be assigned to multiple clients.

        Example: "+hcmCjJEtLq4BRPhrILyhgn98Lhy6DaWdpmsBAgOLCQ="

-   tags (OPTIONAL)

    A list of strings that describe the endpoint's capabilities.
    
    Tags are fundamental for discovery within a federation, aiding both servers and clients in identifying appropriate connections.

    -   Servers:  Tags enable servers to identify clients with specific characteristics or capabilities. For instance, a server might want to serve only clients with particular security clearances or those supporting specific protocol versions. By filtering incoming requests based on relevant tags, servers can efficiently identify suitable clients for serving.

    -   Clients:  Tags also assist clients in discovering servers offering the services they require. Clients can search for servers based on tags indicating supported protocols or the type of data they handle. This enables clients to efficiently locate servers meeting their specific needs.

    Federation-Specific Considerations

    While tags are tied to individual federations and serve distinct purposes within each, several key considerations are crucial to ensure clarity and promote consistent tag usage:

    -   Well-Defined Scope: Each federation MUST establish a clear scope for its tags, detailing their intended use, allowed tag values, associated meanings, and any relevant restrictions. Maintaining a well-defined and readily accessible registry of approved tags is essential for the federation.

    -   Validation Mechanisms: Implementing validation mechanisms for tags is highly recommended. This may involve a dedicated operation or service verifying tag validity and compliance with the federation's regulations. Such validation ensures consistency within the federation by preventing the use of unauthorized or irrelevant tags.

    Pattern: `^[a-z0-9]{1,64}$`

    Example: `["scim", "xyzzy"]`


## Metadata Schema

The FedTLS metadata schema is defined in (#json-schema-for-fedtls-metadata). This schema specifies the format for describing entities involved in FedTLS and their associated information.

**Note:** The schema in Appendix A is folded due to line length limitations as specified in  [@RFC8792].


## Metadata Signing

The federation metadata is signed with JWS and published using JWS JSON Serialization according to the General JWS JSON Serialization Syntax defined in [@!RFC7515]. It is RECOMMENDED that federation metadata signatures are created with algorithm _ECDSA using P-256 and SHA-256_ ("ES256") as defined in [@RFC7518].

The following federation metadata signature protected headers are REQUIRED:

*   `alg` (Algorithm)

    Identifies the algorithm used to generate the JWS signature [@!RFC7515], section 4.1.1.

*   `iat` (Issued At)

    Identifies the time on which the signature was issued. Its value MUST be a number containing a NumericDate value.

*   `exp` (Expiration Time)

    Identifies the expiration time on and after which the signature and federation metadata are no longer valid. The expiration time of the federation metadata MUST be set to the value of exp. Its value MUST be a number containing a NumericDate value.

*   `iss` (Issuer)

    A URI uniquely identifying the issuing federation, playing a critical role in establishing trust and securing interactions within the FedTLS framework. The iss claim differentiates federations, preventing ambiguity and ensuring entities are recognized within their intended context. Verification of the iss claim, along with the corresponding issuer's certificate, enables relying parties to confidently determine information origin and establish trust with entities within the identified federation. This ensures secure communication and mitigates potential security risks.

*   `kid` (Key Identifier)

    The key ID is used to identify the signing key in the key set used to sign the JWS.


## Metadata Example

The following is a non-normative example of a metadata statement. Line breaks within the issuers' claim is for readability only.

~~~ json
{
  "version": "1.0.0",
  "cache_ttl": 3600,
  "entities": [{
    "entity_id": "https://example.com",
    "organization": "Example Org",
    "issuers": [{
      "x509certificate": "-----BEGIN CERTIFICATE-----\nMIIDDDCCAf
      SgAwIBAgIJAIOsfJBStJQhMA0GCSqGSIb3DQEBCwUAMBsxGTAXBgNV\nBAM
      MEHNjaW0uZXhhbXBsZS5jb20wHhcNMTcwNDA2MDc1MzE3WhcNMTcwNTA2MD
      c1\nMzE3WjAbMRkwFwYDVQQDDBBzY2ltLmV4YW1wbGUuY29tMIIBIjANBgk
      qhkiG9w0B\nAQEFAAOCAQ8AMIIBCgKCAQEAyr+3dXTC8YXoi0LDJTH0lTfv
      8omQivWFOr3+/PBE\n6hmpLSNXK/EZJBD6ZT4Q+tY8dPhyhzT5RFZCVlrDs
      e/kY00F4yoflKiqx9WSuCrq\nZFr1AUtIfGR/LvRUvDFtuHo1MzFttiK8Wr
      wskMYZrw1zLHTIVwBkfMw1qr2XzxFK\njt0CcDmFxNdY5Q8kuBojH9+xt5s
      ZbrJ9AVH/OI8JamSqDjk9ODyGg+GrEZFClP/B\nxa4Fsl04En/9GfaJnCU1
      NpU0cqvWbVUlLOy8DaQMN14HIdkTdmegEsg2LR/XrJkt\nho16diAXrgS25
      3xbkdD3T5d6lHiZCL6UxkBh4ZHRcoftSwIDAQABo1MwUTAdBgNV\nHQ4EFg
      QUs1dXuhGhGc2UNb7ikn3t6cBuU34wHwYDVR0jBBgwFoAUs1dXuhGhGc2U\
      nNb7ikn3t6cBuU34wDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAA
      OCAQEA\nrR9wxPhUa2XfQ0agAC0oC8TFf8wbTYb0ElP5Ej834xMMW/wWTSA
      N8/3WqOWNQJ23\nf0vEeYQwfvbD2fjLvYTyM2tSPOWrtQpKuvulIrxV7Zz8
      A61NIjblE3rfea1eC8my\nTkDOlMKV+wlXXgUxirride+6ubOWRGf92fgze
      DGJWkmm/a9tj0L/3e0xIXeujxC7\nMIt3p99teHjvnZQ7FiIBlvGc1o8FD1
      FKmFYd74s7RxrAusBEAAmBo3xyB89cFU0d\nKB2fkH2lkqiqkyOtjrlHPoy
      6ws6g1S6U/Jx9n0NEeEqCfzXnh9jEpxisSO+fBZER\npCwj2LMNPQxZBqBF
      oxbFPw==\n-----END CERTIFICATE-----"
    }],
    "servers": [{
      "description": "SCIM Server 1",
      "base_uri": "https://scim.example.com/",
      "pins": [{
        "alg": "sha256",
        "digest": "+hcmCjJEtLq4BRPhrILyhgn98Lhy6DaWdpmsBAgOLCQ="
      }],
      "tags": [
        "scim"
      ]
    }],
    "clients": [{
      "description": "SCIM Client 1",
      "pins": [{
        "alg": "sha256",
        "digest": "+hcmCjJEtLq4BRPhrILyhgn98Lhy6DaWdpmsBAgOLCQ="
      }]
    }]
  }]
}
~~~


# Usage Examples

The examples in this section are non-normative.

The example below is from the federation called "Skolfederation" where federated TLS authentication is already in use. Clients and servers are registered in the federation. The clients intend to manage cross-domain user accounts within the service. The standard used for account management is SS 12000:2018 (i.e., a SCIM extension).

~~~ ascii-art
+---------------------------------------------+
|                                             |
|             Federation Metadata             |
|                                             |
+---+--------------------------+--------------+
    |                          |
   (A)                        (A)
    |                          |
    v                          v
+---+----+        +------------+--------------+
|Local MD|        |         Local MD          |
+---+----+        +----+------------- ---+----+
    |                  |                 |
   (B)                (C)               (F)
    |                  |                 |
    v                  v                 v
+---+----+        +----+---+        +----+---+
|        |        |        |        |        |
| Client |        | Reverse|        |  App   |
|        +--(D)-->+ Proxy  +--(E)-->+        |
|        |        |        |        |        |
|        |        |        |        |        |
+--------+        +--------+        +--------+
~~~

{type="A"}
1. Entities collect member metadata from the federation metadata.
2. The client pins the server's public key pins.
3. The reverse proxy trust anchor is setup with the clients' certificate issuers.
4. The client establishes a connection with the server using the base_uri from the federation metadata.
5. The reverse proxy forwards the client certificate to the application.
6. The application converts the certificate to a public key pin and checks the federation metadata for a matching pin. The entity's entity_id should be used as an identifier.


## Client

A certificate is issued for the client and the issuer is published in the federation metadata together with the client's certificate public key pins

When the client wants to connect to a remote server (identified by an entity identifier) the following steps need to be taken:

1. Find possible server candidates by filtering the remote entity's list of servers based on tags.
2. Connect to the server URI. Include the entity's list of certificate issuers in the TLS clients list of trusted CAs, or trust the listed pins explicitly.
3. If pinning was not used, validate the received server certificate using the entity's published pins.
4. Commence transactions.


## Server

A certificate is issued for the server and the issuer is published in the federation metadata together with the server's name and certificate public key pin.

When the server receives a connection from a remote client, the following steps need to be taken:

1. Populate list of trusted CAs using all known entities' published issuers and required TLS client certificate authentication, or configure optional untrusted TLS client certificate authentication (e.g., optional\_no\_ca).
2. Once a connection has been accepted, validate the received client certificate using the client's published pins.
3. Commence transactions.


## SPKI Generation

Example of how to use OpenSSL to generate a SPKI fingerprint from a PEM-encoded certificate.

~~~ bash
  openssl x509 -in <certificate.pem> -pubkey -noout | \
  openssl pkey -pubin -outform der | \
  openssl dgst -sha256 -binary | \
  openssl enc -base64
~~~


## Curl and Public Key Pinning

Example of public key pinning with curl. Line breaks are for readability only.

~~~ bash
  curl --cert client.pem --client.key --pinnedpubkey 'sha256//0Ok2aNf
  crCNDMhC2uXIdxBFOvMfEVtzlNVUT5pur0Dk=' https://host.example.com
~~~


# Security Considerations

## TLS

The security considerations for TLS 1.3 [@!RFC8446] are detailed in Section 10, along with Appendices C, D, and E of RFC 8446.


## Federation Metadata Updates

Regularly updating the local copy of federation metadata is essential for accessing the latest information about active entities, current public key pins, and valid certificates. The use of outdated metadata may expose systems to security risks, such as interaction with revoked entities or acceptance of manipulated data. If specified in the federation metadata, cache_ttl values SHOULD be respected.


## Verifying the Federation Metadata Signature

Ensuring data integrity and security within the FedTLS framework relies on verifying the signature of downloaded federation metadata. This process confirms the data's origin, validating that it comes from the intended source and has not been altered by unauthorized parties. Through the process of verifying the metadata's authenticity, trust is established in the information it contains, including valid member certificates and public key pins.


# Acknowledgements

This project was funded through the NGI0 PET Fund, a fund established by NLnet with financial support from the European Commission's Next Generation Internet programme, under the aegis of DG Communications Networks, Content and Technology under grant agreement No 825310.

The authors would like to thank the following people for the detailed review and suggestions:

*   Rasmus Larsson
*   Mats Dufberg
*   Joe Siltberg
*   Stefan Norberg
*   Petter Blomberg

The authors would also like to thank participants in the EGIL working group for their comments on this specification.


# IANA Considerations

This document has no IANA actions.


{backmatter}


# JSON Schema for FedTLS Metadata

This JSON schema defines the format of FedTLS metadata.

Version: 1.0.0
```
=============== NOTE: '\\' line wrapping per RFC 8792 ===============

{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://www.fedtls.se/schema/fedtls-metadata-schema.json\
\",
    "title": "JSON Schema for Federated TLS Authentication",
    "description": "Version: 1.0.0",
    "type": "object",
    "additionalProperties": true,
    "required": [
        "version",
        "entities"
    ],
    "properties": {
        "version": {
            "title": "Metadata schema version",
            "description": "Schema version follows semantic versioni\
\ng (https://semver.org)",
            "type": "string",
            "pattern": "^\\d+\\.\\d+\\.\\d+$",
            "examples": [
                "1.0.0"
            ]
        },
        "cache_ttl": {
            "title": "Metadata cache TTL",
            "description": "How long (in seconds) to cache metadata.\
\ Effective maximum TTL is the minimum of HTTP Expire and TTL",
            "type": "integer",
            "minimum": 0,
            "examples": [
                3600
            ]
        },
        "entities": {
            "type": "array",
            "items": {
                "$ref": "#/components/entity"
            }
        }
    },
    "components": {
        "entity": {
            "type": "object",
            "additionalProperties": true,
            "required": [
                "entity_id",
                "issuers"
            ],
            "properties": {
                "entity_id": {
                    "title": "Entity identifier",
                    "description": "Globally unique identifier for t\
\he entity.",
                    "type": "string",
                    "format": "uri",
                    "examples": [
                        "https://example.com"
                    ]
                },
                "organization": {
                    "title": "Name of entity organization",
                    "description": "Name identifying the organizatio\
\n that the entity's metadata represents.",
                    "type": "string",
                    "examples": [
                        "Example Org"
                    ]
                },
                "issuers": {
                    "title": "Entity certificate issuers",
                    "description": "A list of certificate issuers th\
\at are allowed to issue certificates for the entity's endpoints. Fo\
\r each issuer, the issuer's root CA certificate is included in the \
\x509certificate property (PEM-encoded).",
                    "type": "array",
                    "items": {
                        "$ref": "#/components/cert_issuers"
                    }
                },
                "servers": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/endpoint"
                    }
                },
                "clients": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/endpoint"
                    }
                }
            }
        },
        "endpoint": {
            "type": "object",
            "additionalProperties": true,
            "required": [
                "pins"
            ],
            "properties": {
                "description": {
                    "title": "Endpoint description",
                    "type": "string",
                    "examples": [
                        "SCIM Server 1"
                    ]
                },
                "tags": {
                    "title": "Endpoint tags",
                    "description": "A list of strings that describe \
\the endpoint's capabilities.",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^[a-z0-9]{1,64}$",
                        "examples": [
                            "xyzzy"
                        ]
                    }
                },
                "base_uri": {
                    "title": "Endpoint base URI",
                    "type": "string",
                    "format": "uri",
                    "examples": [
                        "https://scim.example.com"
                    ]
                },
                "pins": {
                    "title": "Certificate pin set",
                    "type": "array",
                    "items": {
                        "$ref": "#/components/pin_directive"
                    }
                }
            }
        },
        "cert_issuers": {
            "title": "Certificate issuers",
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "x509certificate": {
                    "title": "X.509 Certificate (PEM)",
                    "type": "string"
                }
            }
        },
        "pin_directive": {
            "title": "RFC 7469 pin directive",
            "type": "object",
            "additionalProperties": false,
            "required": [
                "alg",
                "digest"
            ],
            "properties": {
                "alg": {
                    "title": "Directive name",
                    "type": "string",
                    "enum": [
                        "sha256"
                    ],
                    "examples": [
                        "sha256"
                    ]
                },
                "digest": {
                    "title": "Directive value (Base64)",
                    "type": "string",
                    "pattern": "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+\
\/]{2}==|[A-Za-z0-9+/]{3}=)?$",
                    "examples": [
                        "HiMkrb4phPSP+OvGqmZd6sGvy7AUn4k3XEe8OMBrzt8\
\="
                    ]
                }
            }
        }
    }
}
```