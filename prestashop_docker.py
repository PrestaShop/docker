#!/usr/bin/env python

from versions import VERSIONS
from prestashop_docker.generator import Generator
from prestashop_docker.tag_manager import TagManager
from os import path
import argparse


def main():
    parser = argparse.ArgumentParser(description='PrestaShop Docker manager.')
    parser.add_argument(
        'cmd',
        nargs='?',
        default=None,
        choices=['generate', 'tag']
    )
    args = parser.parse_args()

    if args.cmd == 'generate':
        generator = Generator(
            path.join(path.dirname(path.realpath(__file__)), 'images'),
            open('./Dockerfile.model').read(),
            open('./Dockerfile-nightly.model').read()
        )
        generator.generate_all(VERSIONS)
    elif args.cmd == 'tag':
        tag_manager = TagManager()
        tag_manager.create()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
