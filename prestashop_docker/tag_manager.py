import docker
import os
import logging
from .stream_parser import StreamParser
from pathlib import Path

logger = logging.getLogger(__name__)


class TagManager():
    def __init__(self, directory_path, docker_api):
        self.directory_path = Path(directory_path)
        self.docker_api = docker_api
        self.docker_client = docker.from_env()
        self.stream_parser = StreamParser()

    def build(self, version=None):
        '''
        Build version on the current machine

        @param version: Optional version you want to build
        @type version: str
        '''
        versions = {}
        if version is None:
            versions = self.get_versions()
        else:
            versions = self.parse_version(version)

        for version, version_path in versions.items():
            print(
                'Building {}'.format(version)
            )

            if self.exists(version):
                continue

            log = self.docker_client.api.build(
                path=str(version_path),
                tag='prestashop/prestashop:' + version,
                rm=True,
                nocache=True,
                decode=True
            )

            self.stream_parser.display(log)

    def push(self, version=None):
        '''
        Push version on Docker Hub

        @param version: Optional version you want to build
        @type version: str
        '''
        versions = {}
        if version is None:
            versions = self.get_versions()
        else:
            versions = self.parse_version(version)
        for version in versions.keys():
            print(
                'Pushing {}'.format(version)
            )

            if self.exists(version):
                continue

            log = self.docker_client.api.push(
                repository='prestashop/prestashop',
                tag=version,
                decode=True,
                stream=True
            )

            self.stream_parser.display(log)

    def exists(self, version):
        '''
        Test if a version is already on Docker Hub

        @param version: The version you want to check
        @type version: str
        @return: True if tag exists
        @rtype: dict
        '''

        tags = self.docker_api.get_tags()
        for tag in tags:
            if tag['name'] == version:
                return True

        return False

    def get_versions(self):
        '''
        Test if a version is already on Docker Hub

        @return: Return list of versions
        @rtype: dict
        '''
        versions = {}
        for version in os.listdir(self.directory_path):
            versions = {**self.get_containers_versions(
                self.directory_path / version,
                version,
                versions
            )}
        return versions

    def get_containers_versions(self, path, version):
        '''
        Get containers versions

        :param path:
        '''
        versions = {}
        for container_version in os.listdir(path):
            versions[version + '-' + container_version] = os.path.join(
                path,
                container_version
            )
        return versions

    def parse_version(self, version):
        '''
        Parse version and return associated paths.

        1. Only with PrestaShop version
          - 1.7.6.8 => {'1.7.6.8-5.6-fpm': '/home/got/projects/prestashop/docker/images/1.7.6.8/5.6-fpm', '1.7.6.8-7.2-fpm': '/home/got/projects/prestashop/docker/images/1.7.6.8/7.2-fpm', '1.7.6.8-7.1-fpm': '/home/got/projects/prestashop/docker/images/1.7.6.8/7.1-fpm', '1.7.6.8-7.2-apache': '/home/got/projects/prestashop/docker/images/1.7.6.8/7.2-apache', '1.7.6.8-7.1-apache': '/home/got/projects/prestashop/docker/images/1.7.6.8/7.1-apache', '1.7.6.8-5.6-apache': '/home/got/projects/prestashop/docker/images/1.7.6.8/5.6-apache'}

        2. With specific version
          - 1.7.6.8-5.6-fpm => {'1.7.6.8-5.6-fpm': PosixPath('/home/got/projects/prestashop/docker/images/1.7.6.8/5.6-fpm')}

        @param version: The version you want
        @type version: str
        @return: A list with tags and their paths
        @rtype: dict
        '''

        data = version.split('-', 1)
        if len(data) == 2:
            return {
                data[0] + '-' + data[1]: self.directory_path / data[0] / data[1]
            }

        return {**self.get_containers_versions(
            self.directory_path / data[0],
            data[0]
        )}
