%%%

    Title = "SCIM Federated Authentication"
    abbrev = "SCIM Federated AuthN"
    category = "std"
    docName = "draft-schlyter-scim-fed-authn-00"
    ipr= "trust200902"
    area = "Internet"
    workgroup = "DNSOP"
 
    date = 2017-05-04T00:00:00Z
 
    [[author]]
    initials="J."
    surname="Schlyter"
    fullname="Jakob Schlyter"
    organization="Kirei AB"
        [author.address]
        email="jakob@kirei.se"

    [[author]]
    initials="P."
    surname="Girgensohn"
    fullname="Palle Girgensohn"
    organization="Ping Pong BA"
        [author.address]
        email="girgen@pingpong.net"

%%%

.# Abstract

This document describes a mechanism how to federate authentication SCIM [@RFC7642].

{mainmatter}

# Introduction

...


##  Reserved Words

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [@!RFC2119].


# Authentication

Certificates are issued for all endpoints. Certificate issuers published in the metadata as well as the endpoints' name and certificate public key pins.

Upon connection, endpoints validate the peer's certificate against the published certificate issuers as well as the matching public key pin.

If a TLS session is terminated separately from the application (e.g., when using a a load balancer), the TLS session termination point can validate the certificate issuer and defer public key pin matching the to application (given that the peer certificate is transferred to the application).


# Metadata

## Metadata Contents

Metadata contains a list of entities that wish to communicate. Each entity has the following properties:

- an identity (usually a domain name)
- a list of certificate issuers that are allowed to issue certificates for the entity's endpoints
- a list of the entity's servers and clients

Servers and clients has a name (for identification) and a list of public key pins used to limit valid endpoint certificates. Public key pinning syntax and semantics is similar to [@RFC7469]. Server endpoints also include a base URI to connect to the endpoint.

## Metadata Signing

Metadata is in JSON format, signed with JWS [@RFC7515] and published using JWS JSON Serialization.


# Usage Examples

## SCIM Client

A certificate is issued for the SCIM client and the issuer published in the metadata together with client's name and certificate public key pin.

When the SCIM client wants to connect to a remote server, the following steps need to be taken:

1. Find server base URI in metadata.
2. Populate list of trusted CAs using the entity's published issuers.
3. Connect to the server URI.
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
