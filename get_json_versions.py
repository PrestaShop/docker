#!/usr/bin/env python

import argparse
import json
import os
import sys
from versions import VERSIONS

BASE_IMAGES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'base', 'images')


def parse_php_versions(value):
    if value is None or value.strip() == 'all':
        return None
    return [php.strip() for php in value.split(',') if php.strip()]


def get_unknown_php_versions(php_versions, versions, base_images):
    known = {php for phps in versions.values() for php in phps}
    known |= {image.split('-')[0] for image in base_images}
    return [php for php in php_versions if php not in known]


def get_ps_versions(versions, php_versions=None):
    return [
        ps_version for ps_version, phps in versions.items()
        if php_versions is None or set(phps) & set(php_versions)
    ]


def get_php_versions_for(ps_version, versions, php_versions=None):
    return [php for php in versions[ps_version] if php_versions is None or php in php_versions]


def get_base_images(base_images, php_versions=None):
    return sorted(
        image for image in base_images
        if php_versions is None or image.split('-')[0] in php_versions
    )


def main():
    parser = argparse.ArgumentParser(description='List images to publish, as JSON.')
    parser.add_argument('--php', help='Comma separated PHP versions to filter on, or "all"', default=None)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--base', action='store_true', help='List base images instead of PrestaShop versions')
    group.add_argument('--php-for', metavar='PS_VERSION', help='Print the PHP versions to build for this PrestaShop version')
    args = parser.parse_args()

    base_images = [d for d in os.listdir(BASE_IMAGES_DIR) if os.path.isdir(os.path.join(BASE_IMAGES_DIR, d))]
    php_versions = parse_php_versions(args.php)
    if php_versions is not None:
        if not php_versions:
            sys.exit('No PHP version selected, use "all" to select every version')
        unknown = get_unknown_php_versions(php_versions, VERSIONS, base_images)
        if unknown:
            sys.exit('Unknown PHP versions: {}'.format(', '.join(unknown)))

    if args.base:
        print(json.dumps(get_base_images(base_images, php_versions)))
    elif args.php_for:
        if args.php_for not in VERSIONS:
            sys.exit('Unknown PrestaShop version: {}'.format(args.php_for))
        print(' '.join(get_php_versions_for(args.php_for, VERSIONS, php_versions)))
    else:
        print(json.dumps(get_ps_versions(VERSIONS, php_versions)))


if __name__ == '__main__':
    main()
