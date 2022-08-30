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
        self.fs.create_dir('/tmp/images/8.0.0/7.2-apache')
        self.fs.create_dir('/tmp/images/8.0.0/7.2-fpm')
        self.fs.create_dir('/tmp/images/8.0.0/8.0-apache')
        self.fs.create_dir('/tmp/images/8.0.0/8.0-fpm')
        self.fs.create_dir('/tmp/images/8.1.0/7.2-apache')
        self.fs.create_dir('/tmp/images/8.1.0/7.2-fpm')
        self.fs.create_dir('/tmp/images/8.1.3/7.2-apache')
        self.fs.create_dir('/tmp/images/8.1.3/7.2-fpm')
        self.fs.create_dir('/tmp/images/nightly/7.1-fpm')
        self.fs.create_dir('/tmp/images/nightly/7.1-apache')
        self.version_manager = self.create_instance()

    def create_instance(self):
        return VersionManager(
            '/tmp/images'
        )

    all_versions = {
        '1.7.5.1': ('5.6', '5.4'),
        '1.7.5.0': ('5.6', '5.4'),
        '1.7.6.4': ('5.6', '7.1'),
        '1.7.6.5': ('5.6', '7.1'),
        '1.7.6.8': ('5.6', '7.1', '7.2'),
        '1.7.7.0-rc.1': ('7.1', '7.2', '7.3'),
        '8.0.0': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.0.0-rc.1': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.1.0': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.1.3': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        'nightly': ('7.1',)
    }

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_ps_version(self):
        result = self.version_manager.get_version_from_string('1.7.6.8')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6', '7.1', '7.2'), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0')
        self.assertEqual(
            {'ps_version': '8.0.0', 'php_versions': ('7.2', '7.3', '7.4', '8.0', '8.1'), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_invalid_version(self):
        result = self.version_manager.get_version_from_string('1.7.6.42')
        self.assertIsNone(result)
        result = self.version_manager.get_version_from_string('8.0.42')
        self.assertIsNone(result)

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version(self):
        result = self.version_manager.get_version_from_string('1.7.6.8-5.6')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6',), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-7.2')
        self.assertEqual(
            {'ps_version': '8.0.0', 'php_versions': ('7.2',), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version_and_type(self):
        result = self.version_manager.get_version_from_string('1.7.6.8-5.6-fpm')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'php_versions': ('5.6',), 'container_version': 'fpm'},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-7.2-fpm')
        self.assertEqual(
            {'ps_version': '8.0.0', 'php_versions': ('7.2',), 'container_version': 'fpm'},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_pre_release_and_without_container_version_and_type(self):
        result = self.version_manager.get_version_from_string('1.7.7.0-rc.1')
        self.assertEqual(
            {'ps_version': '1.7.7.0-rc.1', 'php_versions': ('7.1', '7.2', '7.3'), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-rc.1')
        self.assertEqual(
            {'ps_version': '8.0.0-rc.1', 'php_versions': ('7.2', '7.3', '7.4', '8.0', '8.1'), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_pre_release_and_php_version_and_without_container_version(self):
        result = self.version_manager.get_version_from_string('1.7.7.0-rc.1-7.3')
        self.assertEqual(
            {'ps_version': '1.7.7.0-rc.1', 'php_versions': ('7.3',), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-rc.1-7.3')
        self.assertEqual(
            {'ps_version': '8.0.0-rc.1', 'php_versions': ('7.3',), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_pre_release_and_php_version_and_with_container_version(self):
        result = self.version_manager.get_version_from_string('1.7.7.0-rc.1-7.3-apache')
        self.assertEqual(
            {'ps_version': '1.7.7.0-rc.1', 'php_versions': ('7.3',), 'container_version': 'apache'},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-rc.1-7.3-apache')
        self.assertEqual(
            {'ps_version': '8.0.0-rc.1', 'php_versions': ('7.3',), 'container_version': 'apache'},
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
        self.assertEqual(
            {
                '8.0.0-7.2-apache': '/tmp/images/8.0.0/7.2-apache',
                '8.0.0-7.2-fpm': '/tmp/images/8.0.0/7.2-fpm',
                '8.0.0-8.0-apache': '/tmp/images/8.0.0/8.0-apache',
                '8.0.0-8.0-fpm': '/tmp/images/8.0.0/8.0-fpm'
            },
            self.version_manager.parse_version('8.0.0')
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
        self.assertEqual(
            {
                '8.1.0-7.2-apache': '/tmp/images/8.1.0/7.2-apache',
                '8.1.0-7.2-fpm': '/tmp/images/8.1.0/7.2-fpm',
            },
            self.version_manager.parse_version('8.1.0-7.2')
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_parse_version_with_valid_version_php_version_and_container(self):
        self.assertEqual(
            {
                '1.7.6.8-5.6-apache': '/tmp/images/1.7.6.8/5.6-apache',
            },
            self.version_manager.parse_version('1.7.6.8-5.6-apache')
        )
        self.assertEqual(
            {
                '8.1.3-7.2-apache': '/tmp/images/8.1.3/7.2-apache',
            },
            self.version_manager.parse_version('8.1.3-7.2-apache')
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_versions(self):
        print(self.version_manager.get_versions())
        self.assertEqual(
            {
                '1.7.5.0-5.6-fpm': '/tmp/images/1.7.5.0/5.6-fpm',
                '1.7.5.0-5.6-apache': '/tmp/images/1.7.5.0/5.6-apache',
                '1.7.5.0-5.4-fpm': '/tmp/images/1.7.5.0/5.4-fpm',
                '1.7.5.0-5.4-apache': '/tmp/images/1.7.5.0/5.4-apache',
                '1.7.5.1-5.6-fpm': '/tmp/images/1.7.5.1/5.6-fpm',
                '1.7.5.1-5.6-apache': '/tmp/images/1.7.5.1/5.6-apache',
                '1.7.5.1-5.4-fpm': '/tmp/images/1.7.5.1/5.4-fpm',
                '1.7.5.1-5.4-apache': '/tmp/images/1.7.5.1/5.4-apache',
                '1.7.6.4-5.6-fpm': '/tmp/images/1.7.6.4/5.6-fpm',
                '1.7.6.4-5.6-apache': '/tmp/images/1.7.6.4/5.6-apache',
                '1.7.6.4-7.1-fpm': '/tmp/images/1.7.6.4/7.1-fpm',
                '1.7.6.4-7.1-apache': '/tmp/images/1.7.6.4/7.1-apache',
                '1.7.6.5-5.6-fpm': '/tmp/images/1.7.6.5/5.6-fpm',
                '1.7.6.5-5.6-apache': '/tmp/images/1.7.6.5/5.6-apache',
                '1.7.6.5-7.1-fpm': '/tmp/images/1.7.6.5/7.1-fpm',
                '1.7.6.5-7.1-apache': '/tmp/images/1.7.6.5/7.1-apache',
                '1.7.6.8-5.6-fpm': '/tmp/images/1.7.6.8/5.6-fpm',
                '1.7.6.8-5.6-apache': '/tmp/images/1.7.6.8/5.6-apache',
                '1.7.6.8-7.1-fpm': '/tmp/images/1.7.6.8/7.1-fpm',
                '1.7.6.8-7.1-apache': '/tmp/images/1.7.6.8/7.1-apache',
                '1.7.6.8-7.2-fpm': '/tmp/images/1.7.6.8/7.2-fpm',
                '1.7.6.8-7.2-apache': '/tmp/images/1.7.6.8/7.2-apache',
                '1.7.7.0-rc.1-7.1-fpm': '/tmp/images/1.7.7.0-rc.1/7.1-fpm',
                '1.7.7.0-rc.1-7.1-apache': '/tmp/images/1.7.7.0-rc.1/7.1-apache',
                '1.7.7.0-rc.1-7.2-fpm': '/tmp/images/1.7.7.0-rc.1/7.2-fpm',
                '1.7.7.0-rc.1-7.2-apache': '/tmp/images/1.7.7.0-rc.1/7.2-apache',
                '1.7.7.0-rc.1-7.3-fpm': '/tmp/images/1.7.7.0-rc.1/7.3-fpm',
                '1.7.7.0-rc.1-7.3-apache': '/tmp/images/1.7.7.0-rc.1/7.3-apache',
                '8.0.0-7.2-fpm': '/tmp/images/8.0.0/7.2-fpm',
                '8.0.0-7.2-apache': '/tmp/images/8.0.0/7.2-apache',
                '8.0.0-7.3-fpm': '/tmp/images/8.0.0/7.3-fpm',
                '8.0.0-7.3-apache': '/tmp/images/8.0.0/7.3-apache',
                '8.0.0-7.4-fpm': '/tmp/images/8.0.0/7.4-fpm',
                '8.0.0-7.4-apache': '/tmp/images/8.0.0/7.4-apache',
                '8.0.0-8.0-fpm': '/tmp/images/8.0.0/8.0-fpm',
                '8.0.0-8.0-apache': '/tmp/images/8.0.0/8.0-apache',
                '8.0.0-8.1-fpm': '/tmp/images/8.0.0/8.1-fpm',
                '8.0.0-8.1-apache': '/tmp/images/8.0.0/8.1-apache',
                '8.0.0-rc.1-7.2-fpm': '/tmp/images/8.0.0-rc.1/7.2-fpm',
                '8.0.0-rc.1-7.2-apache': '/tmp/images/8.0.0-rc.1/7.2-apache',
                '8.0.0-rc.1-7.3-fpm': '/tmp/images/8.0.0-rc.1/7.3-fpm',
                '8.0.0-rc.1-7.3-apache': '/tmp/images/8.0.0-rc.1/7.3-apache',
                '8.0.0-rc.1-7.4-fpm': '/tmp/images/8.0.0-rc.1/7.4-fpm',
                '8.0.0-rc.1-7.4-apache': '/tmp/images/8.0.0-rc.1/7.4-apache',
                '8.0.0-rc.1-8.0-fpm': '/tmp/images/8.0.0-rc.1/8.0-fpm',
                '8.0.0-rc.1-8.0-apache': '/tmp/images/8.0.0-rc.1/8.0-apache',
                '8.0.0-rc.1-8.1-fpm': '/tmp/images/8.0.0-rc.1/8.1-fpm',
                '8.0.0-rc.1-8.1-apache': '/tmp/images/8.0.0-rc.1/8.1-apache',
                '8.1.0-7.2-fpm': '/tmp/images/8.1.0/7.2-fpm',
                '8.1.0-7.2-apache': '/tmp/images/8.1.0/7.2-apache',
                '8.1.0-7.3-fpm': '/tmp/images/8.1.0/7.3-fpm',
                '8.1.0-7.3-apache': '/tmp/images/8.1.0/7.3-apache',
                '8.1.0-7.4-fpm': '/tmp/images/8.1.0/7.4-fpm',
                '8.1.0-7.4-apache': '/tmp/images/8.1.0/7.4-apache',
                '8.1.0-8.0-fpm': '/tmp/images/8.1.0/8.0-fpm',
                '8.1.0-8.0-apache': '/tmp/images/8.1.0/8.0-apache',
                '8.1.0-8.1-fpm': '/tmp/images/8.1.0/8.1-fpm',
                '8.1.0-8.1-apache': '/tmp/images/8.1.0/8.1-apache',
                '8.1.0-7.2-fpm': '/tmp/images/8.1.0/7.2-fpm',
                '8.1.3-7.2-fpm': '/tmp/images/8.1.3/7.2-fpm',
                '8.1.3-7.2-apache': '/tmp/images/8.1.3/7.2-apache',
                '8.1.3-7.3-fpm': '/tmp/images/8.1.3/7.3-fpm',
                '8.1.3-7.3-apache': '/tmp/images/8.1.3/7.3-apache',
                '8.1.3-7.4-fpm': '/tmp/images/8.1.3/7.4-fpm',
                '8.1.3-7.4-apache': '/tmp/images/8.1.3/7.4-apache',
                '8.1.3-8.0-fpm': '/tmp/images/8.1.3/8.0-fpm',
                '8.1.3-8.0-apache': '/tmp/images/8.1.3/8.0-apache',
                '8.1.3-8.1-fpm': '/tmp/images/8.1.3/8.1-fpm',
                '8.1.3-8.1-apache': '/tmp/images/8.1.3/8.1-apache',
                'nightly-7.1-fpm': '/tmp/images/nightly/7.1-fpm',
                'nightly-7.1-apache': '/tmp/images/nightly/7.1-apache'

            },

            self.version_manager.get_versions(),
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_aliases(self):
        self.assertEqual(
            {
                '1.7.6.8-5.6-apache': ['1.7-5.6', '1.7.6-5.6', '1.7.6.8-5.6'],
                '1.7.6.8-7.1-apache': ['1.7-7.1', '1.7.6-7.1', '1.7.6.8-7.1'],
                '1.7.6.8-7.2-apache': [
                    '1.7-7.2',
                    '1.7',
                    '1.7-apache',
                    '1.7.6-7.2',
                    '1.7.6',
                    '1.7.6-apache',
                    '1.7.6.8-7.2',
                    '1.7.6.8',
                    '1.7.6.8-apache',
                ],
                '1.7.6.8-7.2-fpm': ['1.7-fpm', '1.7.6-fpm', '1.7.6.8-fpm'],
                '1.7.5.1-5.6-apache': [
                    '1.7.5-5.6',
                    '1.7.5',
                    '1.7.5-apache',
                    '1.7.5.1-5.6',
                    '1.7.5.1',
                    '1.7.5.1-apache',
                ],
                '1.7.5.1-5.4-apache': ['1.7.5-5.4', '1.7.5.1-5.4'],
                '1.7.5.1-5.6-fpm': ['1.7.5-fpm', '1.7.5.1-fpm'],
                '1.7.6.4-5.6-apache': ['1.7.6.4-5.6'],
                '1.7.6.4-7.1-apache': ['1.7.6.4-7.1', '1.7.6.4', '1.7.6.4-apache'],
                '1.7.6.4-7.1-fpm': ['1.7.6.4-fpm'],
                '1.7.6.5-5.6-apache': ['1.7.6.5-5.6'],
                '1.7.6.5-7.1-apache': ['1.7.6.5-7.1', '1.7.6.5', '1.7.6.5-apache'],
                '1.7.6.5-7.1-fpm': ['1.7.6.5-fpm'],
                '1.7.7.0-rc.1-7.1-apache': ['1.7.7.0-rc.1-7.1'],
                '1.7.7.0-rc.1-7.2-apache': ['1.7.7.0-rc.1-7.2'],
                '1.7.7.0-rc.1-7.3-apache': [
                    '1.7.7.0-rc.1-7.3',
                    '1.7.7.0-rc.1',
                    '1.7.7.0-rc.1-apache',
                ],
                '1.7.7.0-rc.1-7.3-fpm': ['1.7.7.0-rc.1-fpm'],
                '8.0.0-7.2-apache': ['8.0-7.2', '8.0.0-7.2'],
                '8.0.0-7.3-apache': ['8.0-7.3', '8.0.0-7.3'],
                '8.0.0-7.4-apache': ['8.0-7.4', '8.0.0-7.4'],
                '8.0.0-8.0-apache': ['8.0-8.0', '8.0.0-8.0'],
                '8.0.0-8.1-apache': [
                    '8.0-8.1',
                    '8.0',
                    '8.0-apache',
                    '8.0.0-8.1',
                    '8.0.0',
                    '8.0.0-apache'
                ],
                '8.0.0-8.1-fpm': ['8.0-fpm', '8.0.0-fpm'],
                '8.0.0-rc.1-7.2-apache': ['8.0.0-rc.1-7.2'],
                '8.0.0-rc.1-7.3-apache': ['8.0.0-rc.1-7.3'],
                '8.0.0-rc.1-7.4-apache': ['8.0.0-rc.1-7.4'],
                '8.0.0-rc.1-8.0-apache': ['8.0.0-rc.1-8.0'],
                '8.0.0-rc.1-8.1-apache': [
                    '8.0.0-rc.1-8.1',
                    '8.0.0-rc.1',
                    '8.0.0-rc.1-apache'
                ],
                '8.0.0-rc.1-8.1-fpm': ['8.0.0-rc.1-fpm'],
                '8.1.0-7.2-apache': ['8.1.0-7.2'],
                '8.1.0-7.3-apache': ['8.1.0-7.3'],
                '8.1.0-7.4-apache': ['8.1.0-7.4'],
                '8.1.0-8.0-apache': ['8.1.0-8.0'],
                '8.1.0-8.1-apache': ['8.1.0-8.1', '8.1.0', '8.1.0-apache'],
                '8.1.0-8.1-fpm': ['8.1.0-fpm'],
                '8.1.3-7.2-apache': ['8-7.2', '8.1-7.2', '8.1.3-7.2'],
                '8.1.3-7.3-apache': ['8-7.3', '8.1-7.3', '8.1.3-7.3'],
                '8.1.3-7.4-apache': ['8-7.4', '8.1-7.4', '8.1.3-7.4'],
                '8.1.3-8.0-apache': ['8-8.0', '8.1-8.0', '8.1.3-8.0'],
                '8.1.3-8.1-apache': [
                    'latest',
                    '8-8.1',
                    '8',
                    '8-apache',
                    '8.1-8.1',
                    '8.1',
                    '8.1-apache',
                    '8.1.3-8.1',
                    '8.1.3',
                    '8.1.3-apache',
                ],
                '8.1.3-8.1-fpm': ['8-fpm', '8.1-fpm', '8.1.3-fpm'],
                'nightly-7.1-apache': ['nightly-7.1', 'nightly', 'nightly-apache'],
                'nightly-7.1-fpm': ['nightly-fpm'],
            },
            self.version_manager.get_aliases(),
        )
