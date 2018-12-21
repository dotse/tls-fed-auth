#!/usr/bin/env python3

"""Metadata verifier"""

import argparse
import logging
import json
from cryptojwt import b64d
from cryptojwt.jwk import key_from_jwk_dict
from cryptojwt.jws import JWS, BadSignature


def extract_headers(data: str) -> dict:
    """Extract JSON-encoded headers"""
    return json.loads(b64d(data.encode()).decode())


def main():
    """Main function"""

    parser = argparse.ArgumentParser(description='Metadata verifier')

    parser.add_argument('--trusted',
                        dest='trusted',
                        metavar='filename',
                        help='Trusted keys (JWKS)',
                        required=False)
    parser.add_argument('--input',
                        dest='input',
                        metavar='filename',
                        help='Metadata file input',
                        required=True)
    parser.add_argument('--output',
                        dest='metadata_output',
                        metavar='filename',
                        help='Metadata output',
                        required=False)
    parser.add_argument('--headers',
                        dest='headers_output',
                        metavar='filename',
                        help='Headers output',
                        required=False)
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help="Enable debugging")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    trusted_keys = []
    if args.trusted:
        with open(args.trusted) as input_file:
            jwks_dict = json.load(input_file)
            for jwk_dict in jwks_dict['keys']:
                trusted_keys.append(key_from_jwk_dict(jwk_dict, private=False))

    with open(args.input, 'rt') as input_file:
        metadata_file = input_file.read()

    protected_headers = []
    metadata_dict = json.loads(metadata_file)

    if args.trusted:
        jws = JWS()
        metadata = jws.verify_json(metadata_file, keys=trusted_keys)
    else:
        metadata = json.loads(b64d(metadata_dict['payload'].encode()).decode())

    for signatures in metadata_dict['signatures']:
        if 'protected' in signatures:
            protected_headers.append(extract_headers(signatures['protected']))

    if args.headers_output:
        with open(args.headers_output, 'wt') as output_file:
            print(json.dumps(protected_headers, indent=4), file=output_file)
    else:
        if args.trusted:
            print("# METADATA PROTECTED HEADERS (VERIFIED)")
        else:
            print("# METADATA PROTECTED HEADERS (NOT VERIFIED)")
        print(json.dumps(protected_headers, indent=4, sort_keys=True))

    if args.metadata_output:
        with open(args.metadata_output, 'wt') as output_file:
            print(json.dumps(metadata, indent=4), file=output_file)
    else:
        if args.trusted:
            print("# METADATA CONTENTS (VERIFIED)")
        else:
            print("# METADATA CONTENTS (NOT VERIFIED)")
        print(json.dumps(metadata, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
