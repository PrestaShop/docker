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

    def push(self):
        pass

    def exists(self, version):
        '''
        Test if a version is already on Docker Hub

        :param str: version
        :returns: If the tag exists
        :rtype: bool
        '''

        tags = self.docker_api.get_tags()
        for tag in tags:
            if tag['name'] == version:
                return True

        return False

    def get_versions(self):
        versions = {}
        for version in os.listdir(self.directory_path):
            versions = {**self.get_containers_versions(
                self.directory_path / version,
                version,
                versions
            )}
        return versions

    def get_containers_versions(self, path, version):
        versions = {}
        for container_version in os.listdir(path):
            versions[version + '-' + container_version] = os.path.join(
                path,
                container_version
            )
        return versions

    def parse_version(self, version):
        data = version.split('-', 1)
        if len(data) == 2:
            return {
                data[0] + '-' + data[1]: self.directory_path / data[0] / data[1]
            }

        return {**self.get_containers_versions(
            self.directory_path / data[0],
            data[0]
        )}
