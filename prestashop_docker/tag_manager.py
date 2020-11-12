import logging
from .stream import Stream

logger = logging.getLogger(__name__)


class TagManager():
    def __init__(self, docker_api, docker_client, version_manager):
        '''
        Constructor

        @param docker_api: Customer docker API
        @type docker_api: DockerApi
        @param docker_client: Docker client
        @type docker_client: docker
        @param version_manager: Version manager
        @type version_manager: VersionManager
        '''
        self.docker_api = docker_api
        self.docker_client = docker_client
        self.stream = Stream()
        self.version_manager = version_manager

    def build(self, version=None):
        '''
        Build version on the current machine

        @param version: Optional version you want to build
        @type version: str
        '''
        versions = self.get_versions(version)

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
            self.stream.display(log)

            aliases = self.version_manager.get_aliases()
            if version in aliases:
                for alias in aliases[version]:
                    print(
                        'Create tag {}'.format(alias)
                    )
                    self.docker_client.api.tag(
                        'prestashop/prestashop:' + version,
                        'prestashop/prestashop',
                        alias
                    )

    def push(self, version=None):
        '''
        Push version on Docker Hub

        @param version: Optional version you want to build
        @type version: str
        '''
        versions = self.get_versions(version)

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

            self.stream.display(log)

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

    def get_versions(self, version):
        '''
        Version checker

        @param version: Version
        @type version: str
        @return: List of versions
        @rtype: dict
        '''
        if version is None:
            return self.version_manager.get_versions()

        return self.version_manager.parse_version(version)
