#!/usr/bin/env python3

import sys
import argparse
import yaml
import json
import jsonschema


def main():
    """ Main function"""

    parser = argparse.ArgumentParser(description='Schema checker')
    parser.add_argument('schema',
                        nargs='+',
                        metavar='filename')
    parser.add_argument('--input',
                        metavar='filename')
    args = parser.parse_args()

    for filename in args.schema:
        with open(filename) as file:
            print("Checking schema", filename, file=sys.stderr)
            if filename.endswith('.json'):
                schema = json.load(file)
            elif filename.endswith('.yaml'):
                schema = yaml.load(file)
            else:
                raise Exception("Unknown schema format")

        jsonschema.Draft4Validator.check_schema(schema)

        if args.input:
            with open(args.input) as file:
                print("Checking input", args.input, file=sys.stderr)
                if args.input.endswith('.json'):
                    data = json.load(file)
                elif args.input.endswith('.yaml'):
                    data = yaml.load(file)
                else:
                    raise Exception("Unknown input format")
                jsonschema.validate(data, schema)


if __name__ == "__main__":
    main()
