%%%

    title = "Federated TLS Authentication"
    abbrev = "FedTLS"
    category = "std"
    ipr = "trust200902"
    submissiontype = "independent"
    area = "Internet"
    date = 2024-09-30T00:00:00Z

    [seriesInfo]
    status = "informational"
    name = "Internet-Draft"
    value = "draft-halen-fed-tls-auth-15"
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

This document describes the Federated TLS Authentication (FedTLS) protocol, enabling secure machine-to-machine communication within a federation. Both clients and servers perform mutual TLS authentication, establishing trust based on a centrally managed trust anchor published by the federation. Additionally, FedTLS ensures unambiguous identification of entities, as only authorized members within the federation can publish metadata, further mitigating risks associated with unauthorized entities impersonating legitimate participants. This framework promotes seamless and secure interoperability across different trust domains adhering to common policies and standards within the federation.

{mainmatter}


# Introduction

This document describes the Federated TLS Authentication (FedTLS) framework. The initial use case for FedTLS was to complement SAML federations. In a SAML federation, the service is often populated with user data when the user logs into a service for the first time, so-called just-in-time provisioning. There are scenarios where user data must be present in the service before the user logs in for the first time. FedTLS was developed to bridge this gap by allowing machine-to-machine communications to pre-provision user information.

The FedTLS concept mirrors the trust model in SAML, where federation member entities are managed in metadata, and trust is established through a central trust anchor, held by a third party. This approach maintains the well-known trust model and use of metadata while extending its use to handle secure communication.

FedTLS broadens a federation ecosystem by enabling secure machine-to-machine communication. It can be used for any communication that needs an authenticated secure channel. Although FedTLS original use case was to complement SAML federations, it is an independent solution that provides a framework for secure communication.

The FedTLS framework uses a centralized registry that contains information about public keys, endpoints, and other entity details. The information in the registry is signed and published, this signed information constitutes the federation's metadata. Federation members use federation metadata to establish connections between clients and servers, eliminating the need for manual configuration. This approach simplifies administration and promotes interoperability between systems.

A federation operator is responsible for managing the central trust anchor. This trust anchor connects different trust domains under a common set of policies and standards. The federation operator is also responsible for auditing the members and ensuring the integrity of the federation metadata. It is essential that the federation members have undivided trust in the federation operator.

FedTLS enables secure machine-to-machine communication within a federation through mutual TLS authentication, (as defined in [@!RFC8446]). This establishes mutual trust, where both parties are authenticated and verified.

FedTLS enables the use of self-signed certificates. Signing by a CA of the certificate has no meaning in FedTLS and does not increase the security level in this context. Unlike Web PKI certificates, which depend on trust in external certificate authorities (CAs), FedTLS relies on a cryptographic trust mechanism rooted within the federation itself. This approach avoids challenges associated with varying levels of trust in CAs and the risk of compromised certificates within the Web PKI ecosystem.  

Through mechanisms like public key pinning [@!RFC7469], member vetting, and signed metadata, FedTLS establishes strong reliance on self-signed certificates. These measures ensure the validity and authenticity of self-signed certificates within the federation, providing a secure and cohesive trust framework.  

The Swedish education sector [reference??] demonstrates the benefits of FedTLS by securing endpoints for user lifecycle management with FedTLS. This successful collaboration between school authorities and service providers demonstrates FedTLS's ability to enable trust, streamline operations and improve security within federated environments.


##  Reserved Words

This document is an Informational RFC, which means it offers information and guidance but does not specify mandatory standards. Therefore, the keywords used throughout this document are for informational purposes only and do not imply any specific requirements.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [@!RFC2119].


## Terminology

-   **Federation**: A trusted network of entities that adhere to common security policies and standards,using FedTLS for secure communication.
-   **Federation Member**: An entity that has been approved to join the federation and can leverage FedTLS for secure communication with other members.
-   **Federation Operator**: The entity responsible for the overall operation and management of the federation, including managing the federation metadata, enforcing security policies, and onboarding new members.
-   **Federation Metadata**: A cryptographically signed document containing critical information about all entities within the federation.
-   **Metadata Repository**: A centralized repository storing information about all entities within the federation.
-   **Member Metadata**: Information about entities associated with a specific member within the federation.
-   **Member Vetting**: The process of verifying and approving applicants to join the federation, ensuring they meet security and trustworthiness requirements.
-   **Trust Anchor**: The federation's root of trust is established by the federation metadata signing key, which verifies the federation metadata and allows participants to confidently rely on the information it contains.


# Diverse Design Patterns

FedTLS is designed to be flexible and adaptable to the varying needs of different federations. Federations can differ significantly in terms of size, scope, and security requirements, which makes it challenging to prescribe a one-size-fits-all trust framework and security measures.

For instance, in the European Union, the eIDAS (electronic Identification, Authentication, and trust Services) regulation establishes a framework for electronic identification and trust services for electronic transactions within the EU. This regulation provides a comprehensive set of standards for secure electronic interactions across member states. National federations within EU member states adhere to these standards, ensuring interoperability and mutual recognition of electronic IDs across different countries.

Similarly, national federations, such as those found in education or healthcare sectors, often have their own specific trust frameworks and security measures tailored to their unique needs. These federations may leverage existing national identification systems or other trusted credentials to establish member identities and ensure secure interactions.

Organizations may also set up their own federations, tailored to the specific security requirements and trust models relevant to their context. For example, a private business federation might establish its own vetting processes and trust framework based on the nature of its business and the sensitivity of the data being exchanged.

By allowing federations the flexibility to tailor their trust frameworks and security measures, FedTLS can support a wide range of use cases. This flexibility is crucial for accommodating the diverse requirements and challenges faced by different federations, ensuring a secure and adaptable system for establishing trust and facilitating secure communication.


# Trust Model

The FedTLS framework operates on a trust model that is central to its design and functionality. This section outlines the key components of this trust model and its implications for federation members and the federation operator.


## Role of the Federation Operator

The federation operator plays a critical role in the FedTLS framework. This entity is responsible for:

-   Managing the central trust anchor, which is used to establish trust across different domains within the federation.
-   Vetting federation members to ensure they meet the required standards and policies.
-   Maintaining and securing the federation metadata, which includes public key pins [@!RFC7469], issuer certificates, and other essential information.

Additionally, the federation operator SHOULD develop their own threat models to proactively identify potential risks and threats. This process involves examining the operating environment, evaluating both internal and external threats, and understanding how vulnerabilities can be exploited. The goal of the threat model is to enable the federation operator to establish mitigation strategies that address the identified risks.

The security and stability of the federation rely on the integrity and competence of the federation operator. Members must have complete trust in this central authority to ensure the federation's reliability and security.


## Federation Members' Responsibilities

Federation members share the responsibility of maintaining trust and security within the federation. Their responsibilities include:

-   Adhering to the federation's security policies and procedures.
-   Ensuring the accuracy and timeliness of their metadata submissions.
-   Cooperating with the federation operator's vetting and security measures.

By fulfilling these responsibilities, federation members help sustain the overall trust framework that enables secure and reliable communication within the federation. Federation members submit member metadata to the federation. Both the authenticity of the submitted member metadata and the submitting member need to be ensured by the federation.


## Chain of Trust

Each federation operates within a trust framework that encompasses its own security policies and procedures. This framework is designed to ensure the integrity, authenticity, and confidentiality of communications within the federation. Key components of this framework include:

-   Public key pinning [@!RFC7469] and preloading to thwart man-in-the-middle attacks by ensuring validated certificates.
-   Regular updates and verification of federation metadata to prevent the use of outdated or compromised information.

The federation operator aggregates, signs, and publishes the federation metadata, which combines all members' member metadata along with additional federation-specific information. By placing trust in the federation and its associated signing key, federation members trust the information contained within the federation metadata.

The trust anchor for the federation is established through the federation's signing key, a critical component requiring secure distribution and verification. To achieve this, the federation's signing key is distributed using a JSON Web Key Set (JWKS) [@!RFC7517], providing a flexible framework for exposing multiple keys, including the signing key and keys for rollover. This structured approach ensures members can readily access the necessary keys for verification purposes.

An additional layer of security is introduced through thumbprint verification [@!RFC7638], where federation members can independently verify the key's authenticity. This involves comparing the calculated cryptographic thumbprint of the key with a trusted value, ensuring its integrity. Importantly, this verification process can be conducted through channels separate from the JWKS itself, enhancing security by eliminating reliance on a single distribution mechanism.

This trust framework is essential for enabling seamless and secure interoperability across different trust domains within the federation.


## Member Vetting

To ensure the security and integrity of the FedTLS framework, a member vetting process is essential. Detailed vetting processes are beyond the scope of this document but can be guided by established frameworks such as eIDAS and eduGAIN. 

The following are non-normative references to established frameworks:

-   eIDAS: The eIDAS regulation establishes a framework for electronic identification and trust services within the European Union. It ensures secure and standardized electronic interactions across member states, facilitating mutual recognition of electronic IDs. Operators can refer to the eIDAS framework for guidance on robust authentication and identity verification processes. See [@eIDAS].

-   eduGAIN: eduGAIN is an interfederation service connecting identity federations worldwide, primarily within the research and education sectors. It ensures high standards of security and interoperability, allowing institutions to collaborate seamlessly. eduGAIN's processes for vetting and federating identity providers can serve as a useful reference. See [@eduGAIN].


## Metadata Authenticity

Ensuring the authenticity of metadata is crucial for maintaining the security and trustworthiness of the FedTLS framework. The specific mechanisms for ensuring metadata authenticity are beyond the scope of this document and must be defined by the federation or regulatory bodies.


# Metadata Repository

The FedTLS metadata repository serves as the cornerstone of trust within a federation. It acts as a central vault, securely storing all information about all participating federation members and their respective entities. This information, known as federation metadata, is presented as a JWS [@!RFC7515]to ensure its authenticity and integrity.

The metadata repository is subject to stringent security measures to safeguard the integrity of the stored information. This MAY involve:

-   Member Management: The federation operator can centrally enforce security policies and vet new members before they are added to the repository.
-   Access Controls: Only authorized members within the federation should have access to the repository.
-   Regular Backups: Robust backup procedures ensure data recovery in case of unforeseen circumstances.

Before member metadata is added to the federation's repository, the submitted metadata MUST undergo a validation process. This process aims to verify the accuracy, completeness, and validity of the information provided by a member. The validation process MUST include, at a minimum but not limited to, the following checks:

-   Format Validation: The system checks if the submitted metadata adheres to the defined schema and format specifications.
-   Unique Entity ID: Checks are performed to ensure that the entity_id in the submitted metadata is not already registered by another member. Each entity within the federation must have a unique identifier.
-   Unique Public Key Pins: Public key pins [@!RFC7469] are used to identify client entities within the federation metadata during the connection validation process. When a server validates a client's TLS connection, it extracts the pin from the client's TLS certificate and matches it against entries in the federation metadata. The requirements for pin uniqueness and usage are detailed in Section (#servers-clients). 
-   Certificate Verification: The issuer certificates listed in the metadata are validated to ensure that the algorithms used in the certificates are well-known and secure, and that the certificates are currently valid and have not expired
-   Tag Validation: Ensures that tags (see (#servers-clients)) in the metadata adhere to the defined tag structure, verifying both mandatory and optional tags. This process is crucial for maintaining consistency and preventing unauthorized tags within a federation.

The FedTLS metadata repository serves as the vital foundation for establishing trust and enabling secure communication within a FedTLS environment. By providing a central, secure, and controlled repository for critical information, the metadata repository empowers members to confidently discover other trusted entities, and establish secure connections for seamless interaction.


## Metadata Submission

It is up to the federation to determine which channels should be provided to members for submitting their metadata to the metadata repository. Members typically have the option to either upload the metadata directly to the repository, provided such functionality exists, or to send it to the federation operator through a designated secure channel. If an insecure channel is used, additional measures MUST be taken to verify the authenticity and integrity of the metadata. Such measures may include verifying the checksum of the metadata through another channel. The choice of submission channel may depend on factors such as the federation's guidelines and the preferences of the member.


## Maintaining Up-to-Date Metadata

In a FedTLS federation, accurate and current metadata is essential for ensuring secure and reliable communication between members. This necessitates maintaining up-to-date metadata accessible by all members.

-   Federation Metadata: The federation operator publishes a JWS containing an aggregate of all entity metadata. This JWS serves as the source of truth for information about all members within the federation. Outdated information in the JWS can lead to issues like failed connections, discovery challenges, and potential security risks.
-   Local Metadata: Each member maintains a local metadata store containing information about other members within the federation. This information is retrieved from the federation's publicly accessible JWS. Outdated data in the local store can hinder a member's ability to discover and connect with other relevant entities.

The following outlines the procedures for keeping metadata up-to-date:

-   Federation Operator Role: The federation operator plays a crucial role in maintaining data integrity within the federation. Their responsibilities include:
    -   Defining regulations for metadata management that MUST include, at a minimum but not limited to, expiration and cache time management.
    -   Implementing mechanisms to update the published federation metadata, ensuring it adheres to the expiration time (exp, see (#metadata-signing)) and cache TTL (cache_ttl, see (#federation-metadata-claims)) specifications.

-   Member Responsibility: Members must follow the federation's metadata management regulations and refresh their local metadata store according to the defined expiration and cache regulations.

By adhering to these responsibilities, the Federation ensures that information remains valid for the defined timeframe and that caching mechanisms utilize up-to-date data effectively.


# Authentication

All communication established within the federation leverages mutual TLS authentication, as defined in [@!RFC8446]. This mechanism ensures the authenticity of both communicating parties, establishing a robust foundation for secure data exchange.


## Public Key Pinning

FedTLS implements public key pinning as specified in [@!RFC7469]. Public key pinning associates one or many unique public keys with each endpoint within the federation, stored in the federation metadata. During connection establishment, clients and servers validate the received certificate against the pre-configured public key pins retrieved from the federation metadata. 


### Benefits of Public Key Pinning

The decision to utilize public key pinning in the FedTLS framework was driven by several critical factors aimed at enhancing security and ensuring trust:


#### Interfederation Trust

In interfederation environments, where multiple federations need to trust each other, public key pinning remains effective. Each federation can pin the public keys of entities in other federations, ensuring trust across boundaries. Unlike private certificate chains, which can become complex and difficult to manage across multiple federations, public key pinning provides a straightforward mechanism for establishing trust. FedTLS interfederation addresses this challenge by aggregating metadata from all participating federations into a unified metadata repository. This shared metadata enables secure communication between entities in different federations, ensuring consistent key validation and robust cross-federation trust and security.


#### Fortifying Security Against Threats

Public key pinning is a critical defense against potential CA compromises [What does CA mean here? Certificates are self-signed.]. By directly linking a peer to a specific public key, it prevents attackers from issuing fraudulent certificates. This proactive approach dramatically improves system resilience against attacks.


#### Use of Self-Signed Certificates

The use of self-signed certificates within the federation leverages public key pinning to establish trust. By bypassing external s [CAs??], servers and clients rely on the federation's mechanisms to validate trust. Public key pinning ensures that only the specific, self-signed public key pins listed in the metadata are trusted.


#### Revocation

If any certificate in a certificate chain is compromised, the revocation process can be complex and slow within the Web PKI ecosystem. This complexity arises because not only the compromised certificate but potentially multiple certificates within
the chain might need to be revoked and reissued. Public key pinning mitigates this complexity by allowing clients to explicitly trust a specific public key, thereby reducing dependency on the entire certificate chain's integrity.

If a leaf certificate is compromised within a federation, the revocation process involves removing the pin associated with the compromised certificate and updating the metadata with a pin from a new certificate. This eliminates the need for traditional revocation mechanisms and focuses the trust relationship on the specific, updated public key.


## Pin Discovery and Preloading

Peers in the federation retrieve these unique public key pins, serving as pre-configured trust parameters, from the federation metadata. The federation MUST facilitate the discovery process, enabling peers to identify the relevant pins for each endpoint. Information such as organization, tags, and descriptions within the federation metadata aids in this discovery.

Before initiating any connection, both clients and servers preload the chosen pins in strict adherence to the guidelines outlined in section 2.7 of [@!RFC7469] [correct section?? I do not see the guidelines]. This preloading ensures connections only occur with endpoints possessing matching public keys, effectively blocking attempts to use fraudulent certificates.


## Verification of Received Certificates

Upon connection establishment, both endpoints (client and server) must either leverage public key pinning or validate the received certificate against the published pins. Additionally, the federation metadata contains issuer information, which implementations MAY optionally use to verify certificate issuers. This step remains at the discretion of each individual implementation.

In scenarios where a TLS session terminates independent of the application (e.g., via a reverse proxy), the termination point can utilize optional untrusted TLS client certificate authentication or validate the certificate issuer itself. Depending on the specific implementation, pin validation can then be deferred to the application itself, assuming the peer certificate is appropriately transferred (e.g., via an HTTP header).


## Failure to Validate

It is crucial to note that failure to validate a received certificate against the established parameters, whether through pinning or issuer verification, results [MUST result?] in immediate termination of the connection [connection MUST be rejected?]. This strict approach ensures only authorized and secure communication channels are established within the federation.


## Certificate Rotation:

To replace a certificate, whether due to expiration [does FedTLS use the expiration time of the certificate?] or other reasons, the following procedure must be followed: [in the steps below it is not fully clear if only the member that changes certificate that must do something or also other members]

1. Publishing New Metadata: When a certificate needs to be changed, federation members publish new metadata containing the pin (SHA256 thumbprint) of the new public key. This ensures that the new pin is available to all federation members.
1. Propagation Period: Allow time for the updated metadata to propagate throughout the federation before switching to the new certificate. This overlap period ensures that all nodes recognize the new pin and avoid connection issues.
1. Switching to the New Certificate: After ensuring the new metadata has propagated, members switch to the new certificate in their TLS stack.
1. Removing Old Pin: After successfully switching to the new certificate, members must publish updated metadata that excludes the old pin. This final step ensures that only the current public keys are trusted.


# Federation Metadata

Federation metadata is published as a JWS [@!RFC7515]. The payload contains statements
about federation members entities.

Metadata is used for authentication and service discovery. A client selects a server based on metadata claims (e.g., organization, tags). The client then use the selected server claims base_uri, pins and if needed issuers to establish a connection.

Upon receiving a connection, a server validates the received client certificate using the client's published pins. Server MAY also check other claims such as organization and tags to determine if the connections is accepted or terminated.


## Federation Metadata claims

This section defines the set of claims that can be included in metadata.

-   version (REQUIRED)

    Schema version follows semantic versioning (https://semver.org).

-   cache_ttl (OPTIONAL)

    Specifies the duration in seconds for caching downloaded federation metadata, allowing for independent caching outside of specific HTTP configurations, particularly useful when the communication mechanism isn't HTTP-based. In the event of a metadata publication outage, members can rely on cached metadata until it expires, as indicated by the exp claim in the JWS header (see (#metadata-signing)). Once expired, metadata MUST no longer be trusted to maintain federation security. If cache_ttl is not specified, metadata MUST be refreshed before the expiration time. [does that mean that the metadata can be used "cache_ttl" seconds after expiration time?]

-   Entities (REQUIRED)

    List of entities (see (#entities)).


### Entities

Metadata contains a list of entities that may be used for communication within the federation. Each entity describes one or more endpoints owned by a member. An entity has the following properties:

-   entity_id (REQUIRED)

    A URI that uniquely identifies the entity. This identifier MUST NOT collide with any other entity_id within the federation or with any other federation that the entity interacts with.

    Example: "https://example.com"

-   organization (OPTIONAL)

    A name identifying the organization that the entity's metadata represents. The federation operator MUST ensure a mechanism is in place to verify that the organization claim corresponds to the rightful owner of the information exchanged between nodes. This is crucial for the trust model, ensuring certainty about the identities of the involved parties. The federation operator SHOULD choose an approach that best suits the specific needs and trust model of the federation.

    Example: "Example Org".

-   issuers (REQUIRED)

    A list of certificate issuers allowed to issue certificates for the entity's endpoints MUST be maintained. For each issuer, the issuer's root CA certificate MUST be included in the x509certificate property (PEM-encoded). Certificate verification relies on public key pinning, with the list of allowed issuers used only when a certificate chain validation mechanism is unavoidable. For self-signed certificates, the certificate itself acts as its own issuer and MUST be listed as such in the metadata. [Are really CA relevant when self-signed certificates are used]

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
        
        The name of the cryptographic hash algorithm. Currently, the RECOMMENDED value is 'sha256'. As more secure algorithms are developed over time, federations should be ready to adopt these newer options for enhanced security.

        Example: "sha256"

    -   digest (REQUIRED)

        The public key of the end-entity certificate converted to a Subject Public Key Information (SPKI) fingerprint, as specified in section 2.4 of [@!RFC7469]. For clients, the digest MUST be globally unique for unambiguous identification. However, within the same entity_id object, the same digest MAY be assigned to multiple clients.

        Example: "+hcmCjJEtLq4BRPhrILyhgn98Lhy6DaWdpmsBAgOLCQ="

-   tags (OPTIONAL)

    A list of strings that describe the endpoint's capabilities.
    
    Tags are fundamental for discovery within a federation, aiding both servers and clients in identifying appropriate connections.

    -   Server Tags: Tags associated with servers are used by clients to discover servers offering the services they require. Clients can search for servers based on tags that indicate supported protocols or the type of data they handle, enabling discovery of compatible servers.

    -   Client Tags: Tags associated with clients are used by servers to identify clients with specific characteristics or capabilities. For instance, a server might only accept connections from clients that support particular protocols. By filtering incoming requests based on these tags, servers can identify suitable clients.

    Federation-Specific Considerations

    While tags are tied to individual federations and serve distinct purposes within each, several key considerations are crucial to ensure clarity and promote consistent tag usage:

    -   Well-Defined Scope: Each federation MUST establish a clear scope for its tags, detailing their intended use, allowed tag values, associated meanings, and any relevant restrictions. Maintaining a well-defined and readily accessible registry of approved tags is essential for the federation.

    -   Validation Mechanisms: Implementing validation mechanisms for tags is highly recommended. This may involve a dedicated operation or service verifying tag validity and compliance with the federation's regulations. Such validation ensures consistency within the federation by preventing the use of unauthorized or irrelevant tags.

    Pattern: `^[a-z0-9]{1,64}$`

    Example: `["scim", "xyzzy"]`


## Metadata Schema

The FedTLS metadata schema is defined in (#json-schema-for-fedtls-metadata). This schema specifies the format for describing entities involved in FedTLS and their associated information.

**Note:** The schema in Appendix A is folded due to line length limitations as specified in [@RFC8792].


## Example Metadata 

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

## Metadata Signing

The federation metadata is signed with JWS and published using JWS JSON Serialization according to the General JWS JSON Serialization Syntax defined in [@!RFC7515]. The Federation metadata signatures are RECOMMENDED to be created using the algorithm _ECDSA using P-256 and SHA-256_ ("ES256") as defined in [@RFC7518]. However, to accommodate evolving cryptographic standards, alternative algorithms MAY be used, provided they meet the security requirements of the federation.

The following federation metadata signature protected headers are REQUIRED:

*   `alg` (Algorithm)

    Identifies the algorithm used to generate the JWS signature [@!RFC7515], section 4.1.1.

*   `iat` (Issued At)

    Identifies the time on which the signature was issued. Its value MUST be a number containing a NumericDate value [@!RFC7519], section 4.1.6.

*   `exp` (Expiration Time)

    Identifies the expiration time on and after which the signature and federation metadata are no longer valid. The expiration time of the federation metadata MUST be set to the value of exp. Its value MUST be a number containing a NumericDate value [@!RFC7519], section 4.1.4.

*   `iss` (Issuer)

    A URI uniquely identifying the issuing federation, playing a critical role in establishing trust and securing interactions within the FedTLS framework. The iss claim differentiates federations, preventing ambiguity and ensuring entities are recognized within their intended context. Verification of the iss claim enables determining the origin of information and establishing trust with entities within the identified federation [@!RFC7519], section 4.1.1.

*   `kid` (Key Identifier)

    The key ID is used to identify the signing key in the key set used to sign the JWS [@!RFC7515], section 4.1.4.


## Example Signature Protected Header

The following is a non-normative example of a signature protected header.

~~~ json
{
    "alg": "ES256",
    "exp": 1707739718,
    "iat": 1706875718,
    "iss": "https://fedtls.example.com",
    "kid": "c2fb760e-f4b6-4f7e-b17a-7115d2826d51"
}
~~~


# Example Usage Scenarios

The examples in this section are non-normative.

The following example describes a scenario within the federation "Skolfederation" where FedTLS is already established. Both clients and servers are registered members of the federation. In this scenario, clients aim to manage cross-domain user accounts within the service. The standard used for account management is SS 12000:2018 (i.e., a SCIM extension).

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
  curl --cert client.pem --key client.key --pinnedpubkey 'sha256//0Ok
  2aNfcrCNDMhC2uXIdxBFOvMfEVtzlNVUT5pur0Dk=' https://host.example.com
~~~


# Deployments of the FedTLS Framework

The FedTLS framework has proven its practical value and robustness through successful deployments in several environments.


## Skolfederation Moa

Skolfederation Moa [reference??], a federation dedicated to securing digital educational resources, has adopted FedTLS to enable secure and seamless access for schools and municipalities across Sweden. By standardizing secure communication channels, Moa facilitates efficient and protected data exchange between diverse educational platforms and services.


## Swedish National Agency for Education

The Swedish National Agency for Education [reference??] leverages FedTLS within its digital national test platform to establish a robust authentication mechanism. The platform utilizes an API for client verification prior to secure data transfer to the agency's test service, ensuring the integrity and confidentiality of educational data.

## Sambruk's EGIL

Sambruk's EGIL [reference??], a platform providing digital services to municipalities, has successfully integrated the FedTLS framework. This deployment demonstrates the framework's adaptability to support a wide range of digital service infrastructures.

These deployments highlight the effectiveness of the FedTLS framework in enhancing security and interoperability within the educational sector.


# Security Considerations

## Security Risks and Trust Management

The security risks associated with the FedTLS framework are confined to each individual federation. Both the federation operator and federation members share the responsibility of maintaining trust and security within the federation. Proper handling and management of metadata, as well as thorough vetting of federation members, are crucial to sustaining this trust and security. Each federation operates within a trust framework, which includes its own security policies and procedures to ensure the integrity and reliability of the federation.


## TLS

The security considerations for TLS 1.3 [@!RFC8446] are detailed in Section 10, along with Appendices C, D, and E of RFC 8446.


## Federation Metadata Updates

Regularly updating the local copy of federation metadata is essential for accessing the latest information about active entities, current public key pins [@!RFC7469], and valid issuer certificates. The use of outdated metadata may expose systems to security risks, such as interaction with revoked entities or acceptance of manipulated data.


## Verifying the Federation Metadata Signature

Ensuring data integrity and security within the FedTLS framework relies on verifying the signature of downloaded federation metadata. This verification process confirms the data's origin, ensuring it comes from the intended source and has not been altered by unauthorized parties. By establishing the authenticity of the metadata, trust is maintained in the information it contains, including valid member public key pins and issuer certificates. To achieve a robust implementation, it is crucial to consider the security aspects outlined in [@!RFC7515]. Key points include handling algorithm selection, protecting against key compromise, and ensuring the integrity of the signature process.


## Time Synchronization

Maintaining synchronized clocks across all federation members is critical for the security of the FedTLS framework. Inaccurate timestamps can compromise the validity of digital signatures and certificates, hinder reliable log analysis, and potentially expose the system to time-based attacks. Therefore, all federation members MUST employ methods to ensure their system clocks are synchronized with a reliable time source.


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

<reference anchor='eIDAS' target='https://eidas.ec.europa.eu/'>
    <front>
        <title>eIDAS: electronic Identification, Authentication and trust Services</title>
        <author initials='' surname='' fullname='European Union'>
            <organization>European Commission</organization>
        </author>
        <date year='2014'/>
    </front>
</reference>

<reference anchor='eduGAIN' target='https://edugain.org'>
    <front>
        <title>eduGAIN: Interfederation service connecting research and education identity federations worldwide</title>
        <author initials='' surname='' fullname='eduGAIN'>
            <organization>GÉANT Association</organization>
        </author>
        <date year='2023'/>
    </front>
</reference>
