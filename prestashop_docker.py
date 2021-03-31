#!/usr/bin/env python

import docker
from versions import VERSIONS
from prestashop_docker.generator import Generator
from prestashop_docker.tag_manager import TagManager
from prestashop_docker.docker_api import DockerApi
from prestashop_docker.version_manager import VersionManager
from os import path
import argparse
import logging


def get_parser():
    parser = argparse.ArgumentParser(description='PrestaShop Docker manager.')
    parser.add_argument('--debug', action='store_const', const=True, help='Use Debug', default=False)
    parser.add_argument('--quiet', action='store_const', const=True, help='Use Debug', default=False)
    parser.add_argument('--cache', action='store_const', const=True, help='Enable cache', default=False)

    return parser


def get_subparser(parser):
    return parser.add_subparsers(
        dest='subcommand',
        metavar='[subcommand]'
    )


def get_tag_parser(subparser):
    tag_parser = subparser.add_parser(
        'tag',
        help='Tag managment'
    )
    tag_subparser = tag_parser.add_subparsers(
        dest='tag_subcommand'
    )

    exist_parser = tag_subparser.add_parser(
        'exists',
        help='Check if tag exists on Docker Hub'
    )
    exist_parser.add_argument('version', type=str, help='Version name')

    build_parser = tag_subparser.add_parser(
        'build',
        help='Build container and create docker tag'
    )
    build_parser.add_argument('version', type=str, help='Version name', nargs='?')
    build_parser.add_argument('--force', action='store_const', const=True, help='Force build even if image already exists on Docker hub', default=False)

    push_parser = tag_subparser.add_parser(
        'push',
        help='Push docker tags'
    )
    push_parser.add_argument('version', type=str, help='Version name', nargs='?')
    push_parser.add_argument('--force', action='store_const', const=True, help='Force build even if image already exists on Docker hub', default=False)

    aliases_parser = tag_subparser.add_parser(
        'aliases',
        help='Get aliases'
    )
    aliases_parser.add_argument('version', type=str, help='Version name', nargs='?')

    return tag_parser


def get_generate_parser(subparser):
    generate_parser = subparser.add_parser(
        'generate',
        help='Generate Dockerfile'
    )

    return generate_parser


def main():
    parser = get_parser()
    subparser = get_subparser(parser)
    tag_parser = get_tag_parser(subparser)
    get_generate_parser(subparser)

    args = parser.parse_args()

    logging.basicConfig()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.subcommand == 'generate':
        generator = Generator(
            path.join(path.dirname(path.realpath(__file__)), 'images'),
            open('./Dockerfile.model').read(),
            open('./Dockerfile-nightly.model').read()
        )
        generator.generate_all(VERSIONS)
    elif args.subcommand == 'tag':
        tag_manager = TagManager(
            DockerApi(args.cache, args.debug),
            docker.from_env(),
            VersionManager(path.join(path.dirname(path.realpath(__file__)), 'images')),
            args.cache,
            args.quiet
        )
        if args.tag_subcommand is None:
            tag_parser.print_help()
        else:
            if args.tag_subcommand == 'exists':
                if tag_manager.exists(args.version):
                    exit(0)
                else:
                    exit(1)
            elif args.tag_subcommand == 'build':
                tag_manager.build(args.version, args.force)
            elif args.tag_subcommand == 'push':
                tag_manager.push(args.version, args.force)
            elif args.tag_subcommand == 'aliases':
                tag_manager.get_aliases(args.version)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
