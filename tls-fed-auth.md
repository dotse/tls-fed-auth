%%%

    title = "Federated TLS Authentication"
    abbrev = "Federated TLS AuthN"
    category = "std"
    ipr = "trust200902"
    area = "Internet"
    date = 2018-09-26T00:00:00Z

    [seriesInfo]
    status = "informational"
    name = "Internet-Draft"
    value = "draft-fed-tls-auth-00"
    stream = "IETF"

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

This document describes a mechanism how to federate TLS authentication.

{mainmatter}

# Introduction

This document describes how to, with TLS [@!RFC8446], establish a secure end-to-end channel between two parties, where both client and server are mutually authenticated. Authentication is performed with Mutual TLS Authentication (mTLS) [@!RFC8446]. The trust relationship is based upon a trust anchor held and published by a federation. A federation is a trusted third party that inter-connect different trust domains with a common set of policies and standards. The federation aggregates and publish information about all the federated entities including certificate issuers and public key information.


##  Reserved Words

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [@!RFC2119].


# Federation Chain of Trust

The members of the federation upload their metadata including issuer certificates to the federation. The metadata registrar validates the issuer of metadata and aggregates and signs the metadata with its private key. By verifying the metadata signature, federation members trust the metadata content.

The root of the chain of trust is the metadata signature and the trust anchor is the federation's public key certificate. The certificate needs to be securely distributed, there MUST be an out-of-band function to verify the certificate.


# Authentication

All sessions are authenticated via mutual (client and server) TLS authentication. Trust is limited to a set of certificate issuers published in the federation metadata and further constrained by certificate public key pins for each endpoint (also published in metadata).

Upon connection, endpoints validate the peer's certificate against the published certificate issuers as well as the matching public key pin. If a TLS session is terminated separately from the application (e.g., when using a reverse proxy), the TLS session termination point can validate the certificate issuer and defer public key pin matching the to application given that the peer certificate is transferred to the application (e.g. via a HTTP header).


# Federation Metadata

Entities has an organization claim (for identification). Servers and clients have a list of public key pins used to limit valid endpoint certificates. Public key pinning syntax and semantics is similar to [@RFC7469]. Server endpoints also include a base URI to connect to the endpoint.

The following is a non-normative example of a metadata statement.

<{{example.json}}


## Entities

Metadata contains a list of entities that may be used for communication within the federation. Each entity has the following properties:

-   entity_id (REQUIRED)

    URI that identifies the entity. MUST be globally unique.

    Example: `https://example.com`

-   organization (OPTIONAL)

    Name identifying the organization that the entity’s metadata represents.

    Example: `Example Org.`

-   issuers (REQUIRED)

    A list of certificate issuers that are allowed to issue certificates for the entity's endpoints. For each issuer, the issuer's root CA certificate is included in the x509certificate property (PEM-encoded).

-   servers (OPTIONAL)

    List of the entity's servers (syntax described in next section)

-   clients (OPITIONAL)

    List of the entity's clients (syntax described in next section).


### Servers / Clients

A list of the entity's servers and clients.

-   description (OPTIONAL)

    A human readable text describing the server.

    Example: `SCIM Server 1`

-   base_uri (OPTIONAL)

    Base URL of the server (hence required for endpoints describing servers).
    Example: `https://scim.example.com/`

-   pins (REQUIRED)

    A list of Public Key Pins [@RFC7469]. Each pin has the following properties:

    -   name (REQUIRED)

        The name of the cryptographic hash algorithm. The only allowed value at this time is "sha256".

        Example: `sha256`

    -   value (REQUIRED)

        Base64 encoded Subject Public Key Information (SPKI) fingerprint.

        Example: `+hcmCjJEtLq4BRPhrILyhgn98Lhy6DaWdpmsBAgOLCQ=`

-   tags (OPTIONAL)

    A list of strings that describe the functionality of the server. To discover interoperability the client SHOULD do a conditional comparison of the tags. If an entity has multiple servers that are compatible, the client SHOULD arbitrarily connect to one of the servers. If connection to a server fails, the client SHOULD try with the next server. If the claim is missing or is empty, there MUST be an out-of-band agreement of the servers functionality.

    Pattern: `^[a-z0-9]{1,64}$`  
    Example: `["scim", "xyzzy"]`


## Metadata Schema

A metadata JSON schema (in YAML format) can be found at [https://github.com/kirei/tls-fed-auth](https://github.com/kirei/tls-fed-auth/blob/master/tls-fed-metadata.yaml).


## Metadata Signing

Metadata is signed with JWS [@RFC7515] and published using JWS JSON Serialization. It is RECOMMENDED that metadata signatures are created wih algorithm _ECDSA using P-256 and SHA-256_ ("ES256") as defined in [@RFC7518].

The following metadata signature protected headers are REQUIRED:

*   `alg` (Algorithm)

    Identifies the algorithm used to generate the JWT signature [@RFC7515] section 4.1.1.

*   `iat` (Issued At)

    Identifies the time on which the signature was issued. Its value MUST be a number containing a NumericDate value.

*   `exp` (Expiration Time)

    Identifies the expiration time on and after which the signature and metadata are no longer valid. The expiration time of the metadata MUST be set to the value of exp. Its value MUST be a number containing a NumericDate value.

*   `iss` (Issuer)

    URI that identifies the publisher of metadata. The issuer claim MUST be used to prevent conflicts of entities of the same name from different federations.

*   `kid` (Key Identifier)

    The key ID is used to identify the signing key in the key set used to sign the JWT.


# Usage Examples

The following is a non-normative example of an server and client setup.

<{{usage-example.ascii-art}}

{style="letters"}
1. Entities collects metadata from the federation metadata endpoint.
2. The client pins the server's public key pins.
3. The reverse proxy trust anchor is setup with the clients certificate issuers.
4. The client establish a connection to the server using the base_uri from metadata.
5. The reverse proxy forwards the certificate to the application.
6. The application converts the certificate to a public key pin and the metadata for the pin and extracts the entity_id that will be used for authorization.


## Client

A certificate is issued to the client and the issuer published in the metadata together with the client's certificate public key pins

When the client wants to connect to a remote server (identified by an entity identifier) the following steps need to be taken:

1. Find possible server candidates by filtering the remote entity's list of clients based on tags.
2. Connect to the server URI. Include the entity's list of certificate issuers in the TLS clients list of trusted CAs, or trust the listed pins explicitly.
3. If pinning was not used, validate the received server certificate using the entity's published pins.
4. Commence transactions


## Server

A certificate is issued for the server and the issuer published in the metadata together with server's name and certificate public key pin.

When the server receives a connection from a a remote client, the following steps need to be taken:

1. Populate list of trusted CAs using all known entities' published issuers and required TLS client certificate authentication, or configure optional untrusted TLS client certificate authentication (e.g., `optional_no_ca`).
2. One a connection has been accepted, validate the received client certificate using the client's published pins.
3. Commence transactions.


{backmatter}
