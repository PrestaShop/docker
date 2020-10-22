from pyfakefs.fake_filesystem_unittest import TestCase
from prestashop_docker.tag_manager import TagManager
from unittest.mock import patch
from unittest.mock import MagicMock


class TagManagerTestCase(TestCase):
    @patch('prestashop_docker.docker_api.DockerApi')
    def setUp(self, docker_api):
        self.setUpPyfakefs()
        self.fs.create_dir('/tmp/images')

    def create_instance(self):
        return TagManager(
            '/tmp/images',
            MagicMock(return_value=None),
            MagicMock(return_value=None)
        )

    all_versions = {'1.7.6.8': ('5.6', '7.1'), 'nightly': ('7.1',)}

    @patch('prestashop_docker.tag_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_ps_version(self):
        tag_manager = self.create_instance()
        result = tag_manager.get_version_from_string('1.7.6.8')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6', '7.1'), 'container_version': None},
            result
        )

    @patch('prestashop_docker.tag_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_invalid_version(self):
        tag_manager = self.create_instance()
        result = tag_manager.get_version_from_string('1.7.6.42')
        self.assertIsNone(result)

    @patch('prestashop_docker.tag_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version(self):
        tag_manager = self.create_instance()
        result = tag_manager.get_version_from_string('1.7.6.8-5.6')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6',), 'container_version': None},
            result
        )

    @patch('prestashop_docker.tag_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version_and_type(self):
        tag_manager = self.create_instance()
        result = tag_manager.get_version_from_string('1.7.6.8-5.6-fpm')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6',), 'container_version': 'fpm'},
            result
        )
