#!/usr/bin/env python3

"""JWK Key Generator"""

import os
import sys
import argparse
import json

from Cryptodome.PublicKey import RSA
from jwkest import b64e
from jwkest.ecc import P256
from jwkest.ecc import P384
from jwkest.ecc import P521
from jwkest.jwk import ECKey
from jwkest.jwk import RSAKey
from jwkest.jwk import SYMKey


def main():
    """ Main function"""
    parser = argparse.ArgumentParser(description='JWK Key Generation Utility')

    parser.add_argument('--kid',
                        dest='kid',
                        metavar='key_id',
                        help='Key ID',
                        default='')
    parser.add_argument('--kty',
                        dest='kty',
                        metavar='type',
                        help='Key type',
                        required=True,
                        choices=['RSA', 'EC', 'SYM'])
    parser.add_argument('--size',
                        dest='keysize',
                        metavar='size',
                        help='Key size',
                        type=int)
    parser.add_argument('--crv',
                        dest='crv',
                        metavar='curve',
                        help='EC curve',
                        choices=['P-256', 'P-384', 'P-521'],
                        default='P-256')
    args = parser.parse_args()

    if args.kty.upper() == 'RSA':
        if args.keysize is None:
            args.keysize = 2048
        rsa_key = RSA.generate(args.keysize)
        jwk = RSAKey(key=rsa_key, kid=args.kid)
    elif args.kty.upper() == 'EC':
        if args.crv == 'P-256':
            (priv, pub) = P256.key_pair()
        elif args.crv == 'P-384':
            (priv, pub) = P384.key_pair()
        elif args.crv == 'P-521':
            (priv, pub) = P521.key_pair()
        else:
            print("Unknown curve: {0}".format(args.crv), file=sys.stderr)
            exit(1)
        jwk = ECKey(x=pub[0], y=pub[1], d=priv, crv=args.crv, kid=args.kid)
    elif args.kty.upper() == 'SYM':
        if args.keysize is None:
            args.keysize = 32
        randomkey = os.urandom(args.keysize)
        jwk = SYMKey(key=randomkey, kid=args.kid)
    else:
        print("Unknown key type: {0}".format(args.kty), file=sys.stderr)
        exit(1)

    jwk_dict = jwk.serialize(private=True)
    print(json.dumps(jwk_dict, sort_keys=True, indent=4))
    print("SHA-256: " + b64e(jwk.thumbprint('SHA-256')).decode(), file=sys.stderr)


if __name__ == "__main__":
    main()
