%%%

    title = "Federated TLS Authentication"
    abbrev = "Federated TLS AuthN"
    category = "std"
    ipr = "trust200902"
    area = "Internet"

    [seriesInfo]
    status = "informational"
    name = "Internet-Draft"
    value = "draft-fed-tls-auth-00"
    stream = "IETF"

    date = 2018-08-20T00:00:00Z
 
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

This document describes a mechanism how to federate TLS authentication [@RFC7642].

{mainmatter}

# Introduction

This document describes how to establish a secure end-to-end channel between two parties where both client and server are mutually authenticated. To make it possible for two or more trust domains to interact, the trust relationship is based upon trust anchors held and published by a trusted third-party, i.e. the federation.

The federation publishes an aggregate of metadata containing information about all entities. The chain of trust in the federation is based upon the metadata and the entities' trust anchors that are published in the metadata

Authentication is performed with Mutual TLS Authentication (mTLS) [@!RFC8446]. Both side of the channel cryptographically authenticating each other.


##  Reserved Words

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [@!RFC2119].


# Federation Chain of Trust

The members of the federation upload their metadata including issuer certificates to the federation. The metadata registrar validates the issuer of metadata and aggregates and signs the metadata with its private key. By verifying the metadata signature, federation members trust the metadata content.

The root of the chain of trust is the metadata signature and the trust anchor is the federation's public key certificate. The certificate needs to be securely distributed, there MUST be an out-of-band function to verify the certificate.


# Authentication

All sessions are authenticated via mutual (client and server) TLS authentication. Trust is limited to a set of certificate issuers published in the federation metadata and further constrained by certificate public key pins for each endpoint (also published in metadata).

Upon connection, endpoints validate the peer's certificate against the published certificate issuers as well as the matching public key pin. If a TLS session is terminated separately from the application (e.g., when using a front-end proxy), the TLS session termination point can validate the certificate issuer and defer public key pin matching the to application given that the peer certificate is transferred to the application (e.g. via a HTTP header).


# Federation Metadata

Entities has an organization claim (for identification). Servers and clients have a list of public key pins used to limit valid endpoint certificates. Public key pinning syntax and semantics is similar to [@RFC7469]. Server endpoints also include a base URI to connect to the endpoint.

The following is a non-normative example of a metadata statement.

<{{example.json}}


## entities

Metadata contains a list of entities that may be used for communication within the federation. Each entity has the following properties:

*   entity_id REQUIRED

    URI that identifies the entity. MUST be globally unique.

*   organization OPTIONAL

    Name identifying the organization that the entity’s metadata represents

*   issuers REQUIRED

    A list of certificate issuers that are allowed to issue certificates for the entity's endpoints

*   x509certificate REQUIRED

    PEM-encoded certificate converted to an one-line format where line feed is substituted with \n.


## Metadata Schema

A metadata JSON schema (in YAML format) can be found at [https://github.com/kirei/tls-fed-auth](https://github.com/kirei/tls-fed-auth/blob/master/tls-fed-metadata.yaml).


## Metadata Signing

Metadata is signed with JWS [@RFC7515] and published using JWS JSON Serialization.

The following metadata signature protected headers are REQUIRED:

- alg (_algorithm_)
- exp (_expiration time_)

It is RECOMMENDED that metadata signatures are created wih algorithm _ECDSA using P-256 and SHA-256_ ("ES256") as defined in [@RFC7518].


# Usage Examples

## SCIM Client

A certificate is issued for the SCIM client and the issuer published in the metadata together with client's name and certificate public key pin.

When the SCIM client wants to connect to a remote server, the following steps need to be taken:

1. Find the entity for the remote entity_id.
2. Populate list of trusted CAs using the entity's published issuers.
3. Connect to the server URI (possibly selected by endpoint tag).
4. Validate the received server certificate using the entity's published pins.
5. Commence SCIM transactions.

## SCIM Server

A certificate is issued for the SCIM server and the issuer published in the metadata together with server's name and certificate public key pin.

When the SCIM server receives a connection from a a remote client, the following steps need to be taken:

1. Populate list of trusted CAs using all known entities' published issuers.
2. The server should require TLS client certificate authentication.
3. One a connection has been accepted, validate the received client certificate using the client's published pins.
4. Commence SCIM transactions.


<!--
# IANA Considerations

XXX

# Security Considerations

XXX
-->

{backmatter}
