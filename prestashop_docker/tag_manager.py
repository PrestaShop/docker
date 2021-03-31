import logging
from .stream import Stream

logger = logging.getLogger(__name__)


class TagManager():
    def __init__(self, docker_api, docker_client, version_manager, cache, quiet):
        '''
        Constructor

        @param docker_api: Customer docker API
        @type docker_api: DockerApi
        @param docker_client: Docker client
        @type docker_client: docker
        @param version_manager: Version manager
        @type version_manager: VersionManager
        @param cache: Use cache
        @type cache: bool
        @param quiet: Quiet mode
        @type quiet: bool
        '''
        self.docker_api = docker_api
        self.docker_client = docker_client
        self.stream = Stream(quiet)
        self.version_manager = version_manager
        self.cache = cache
        self.tags = None

    def build(self, version=None, force=False):
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

            if not force and self.exists(version):
                print('Image already exists')
                # Do not build images that already exists on Docker Hub
                continue

            log = self.docker_client.api.build(
                path=str(version_path),
                tag='prestashop/prestashop:' + version,
                rm=True,
                nocache=(not self.cache),
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

    def push(self, version=None, force=False):
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

            if not force and self.exists(version):
                continue

            log = self.docker_client.api.push(
                repository='prestashop/prestashop',
                tag=version,
                decode=True,
                stream=True
            )

            self.stream.display(log)

            aliases = self.version_manager.get_aliases()
            if version in aliases:
                for alias in aliases[version]:
                    print(
                        'Pushing tag {}'.format(alias)
                    )
                    log = self.docker_client.api.push(
                        repository='prestashop/prestashop',
                        tag=alias,
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

        if self.tags is None:
            self.tags = self.docker_api.get_tags()

        for tag in self.tags:
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

    def get_aliases(self, version):
        '''
        Get all aliases

        @param version: Version
        @type version: str
        '''
        versions = self.get_versions(version)
        aliases = self.version_manager.get_aliases()
        for version in versions:
            if version in aliases:
                print('Aliases for {}'.format(version))
                [print("\t{}".format(alias)) for alias in aliases[version]]
