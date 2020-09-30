#!/usr/bin/env python

from versions import VERSIONS
from prestashop_docker.generator import Generator
from os import path
import argparse


def main():
    parser = argparse.ArgumentParser(description='PrestaShop Docker manager.')
    parser.add_argument('cmd', nargs='?', default=None, choices=['generate', 'tag'])
    args = parser.parse_args()

    if args.cmd is None:
        parser.print_help()
    else:
        if args.cmd == 'generate':
            generator = Generator(
                path.join(path.dirname(path.realpath(__file__)), 'images'),
                open('./Dockerfile.model').read(),
                open('./Dockerfile-nightly.model').read()
            )
            generator.generate_all(VERSIONS)


if __name__ == '__main__':
    main()
