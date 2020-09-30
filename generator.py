m#!/usr/bin/env python

from versions import VERSIONS
from generator import Generator
from os import path


if __name__ == '__main__':
    generator = Generator(
        path.join(path.dirname(path.realpath(__file__)), 'images'),
        open('./Dockerfile.model').read(),
        open('./Dockerfile-nightly.model').read()
    )
    generator.generate_all(VERSIONS)
