#!/usr/bin/env python3

"""Metadata signer"""

import argparse
import json
import logging
import time

from cryptojwt.jws.jws import JWS
from cryptojwt.jwx import key_from_jwk_dict


def main():
    """Main function"""

    parser = argparse.ArgumentParser(description='Metadata signer')

    parser.add_argument('--signer',
                        dest='signer',
                        metavar='filename',
                        help='Signer keys (JWK)',
                        required=True)
    parser.add_argument('--alg',
                        dest='alg',
                        metavar='algorithm',
                        help='Algorithm',
                        default='ES256',
                        required=False)
    parser.add_argument('--input',
                        dest='input',
                        metavar='filename',
                        help='Input file',
                        required=True)
    parser.add_argument('--output',
                        dest='output',
                        metavar='filename',
                        help='Output filen',
                        required=False)
    parser.add_argument('--lifetime',
                        dest='lifetime',
                        metavar='seconds',
                        help='Signature lifetime',
                        default=86400,
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

    signer_keys = []
    if args.signer:
        with open(args.signer) as input_file:
            jwks_dict = json.load(input_file)
            for jwk_dict in jwks_dict['keys']:
                signer_keys.append(key_from_jwk_dict(jwk_dict, private=True))

    with open(args.input, 'rt') as input_file:
        metadata = json.load(input_file)

    now = int(time.time())
    protected_headers = {
        'alg': args.alg,
        'crit': ['exp'],
        'iat': now,
        'nbf': now,
        'exp': now + args.lifetime
    }
    unprotected_headers = {}
    message = json.dumps(metadata, sort_keys=True)
    headers = [(protected_headers, unprotected_headers)]
    jws = JWS(msg=message, alg=args.alg)
    signed_metadata = jws.sign_json(keys=signer_keys, headers=headers, flatten=False)

    if args.output:
        with open(args.output, 'wt') as output_file:
            print(signed_metadata, file=output_file)
    else:
        print(signed_metadata)


if __name__ == "__main__":
    main()
