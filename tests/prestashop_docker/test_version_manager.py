from pyfakefs.fake_filesystem_unittest import TestCase
from prestashop_docker.version_manager import VersionManager
from unittest.mock import patch


class VersionManagerTestCase(TestCase):
    @patch('prestashop_docker.docker_api.DockerApi')
    def setUp(self, docker_api):
        self.setUpPyfakefs()
        self.fs.create_dir('/tmp/images')
        self.fs.create_dir('/tmp/images/1.7.6.8/5.6-fpm')
        self.fs.create_dir('/tmp/images/1.7.6.8/5.6-apache')
        self.fs.create_dir('/tmp/images/1.7.6.8/7.1-fpm')
        self.fs.create_dir('/tmp/images/1.7.6.8/7.1-apache')
        self.fs.create_dir('/tmp/images/nightly/7.1-fpm')
        self.fs.create_dir('/tmp/images/nightly/7.1-apache')
        self.version_manager = self.create_instance()

    def create_instance(self):
        return VersionManager(
            '/tmp/images'
        )

    all_versions = {'1.7.6.8': ('5.6', '7.1'), 'nightly': ('7.1',)}

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_ps_version(self):
        result = self.version_manager.get_version_from_string('1.7.6.8')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6', '7.1'), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_invalid_version(self):
        result = self.version_manager.get_version_from_string('1.7.6.42')
        self.assertIsNone(result)

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version(self):
        result = self.version_manager.get_version_from_string('1.7.6.8-5.6')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6',), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version_and_type(self):
        result = self.version_manager.get_version_from_string('1.7.6.8-5.6-fpm')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6',), 'container_version': 'fpm'},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_parse_version_with_invalid_version(self):
        with self.assertRaises(ValueError):
            self.version_manager.parse_version('0.0.0.1')

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_parse_version_with_valid_version(self):
        self.assertEqual(
            {
                '1.7.6.8-5.6-apache': '/tmp/images/1.7.6.8/5.6-apache',
                '1.7.6.8-5.6-fpm': '/tmp/images/1.7.6.8/5.6-fpm',
                '1.7.6.8-7.1-apache': '/tmp/images/1.7.6.8/7.1-apache',
                '1.7.6.8-7.1-fpm': '/tmp/images/1.7.6.8/7.1-fpm'
            },
            self.version_manager.parse_version('1.7.6.8')
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_parse_version_with_valid_version_and_php_version(self):
        self.assertEqual(
            {
                '1.7.6.8-5.6-apache': '/tmp/images/1.7.6.8/5.6-apache',
                '1.7.6.8-5.6-fpm': '/tmp/images/1.7.6.8/5.6-fpm',
            },
            self.version_manager.parse_version('1.7.6.8-5.6')
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_parse_version_with_valid_version_php_version_and_container(self):
        self.assertEqual(
            {
                '1.7.6.8-5.6-apache': '/tmp/images/1.7.6.8/5.6-apache',
            },
            self.version_manager.parse_version('1.7.6.8-5.6-apache')
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_versions(self):
        self.assertEqual(
            {
                '1.7.6.8-5.6-apache': '/tmp/images/1.7.6.8/5.6-apache',
                '1.7.6.8-5.6-fpm': '/tmp/images/1.7.6.8/5.6-fpm',
                '1.7.6.8-7.1-apache': '/tmp/images/1.7.6.8/7.1-apache',
                '1.7.6.8-7.1-fpm': '/tmp/images/1.7.6.8/7.1-fpm',
                'nightly-7.1-apache': '/tmp/images/nightly/7.1-apache',
                'nightly-7.1-fpm': '/tmp/images/nightly/7.1-fpm'
            },
            self.version_manager.get_versions(),
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_aliases(self):
        self.assertEqual(
            {
                '1.7': '1.7.6.8-7.1-apache',
                '1.7-apache': '1.7.6.8-7.1-apache',
                '1.7-fpm': '1.7.6.8-7.1-fpm',
                '1.7-5.6': '1.7.6.8-5.6-apache',
                '1.7-7.1': '1.7.6.8-7.1-apache',
                'nightly': 'nightly-7.1-apache',
                'nightly-apache': 'nightly-7.1-apache',
                'nightly-fpm': 'nightly-7.1-fpm',
                'nightly-7.1': 'nightly-7.1-apache',

            },
            self.version_manager.get_aliases(),
        )
