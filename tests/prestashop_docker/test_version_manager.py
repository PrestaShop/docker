from pyfakefs.fake_filesystem_unittest import TestCase
from prestashop_docker.version_manager import VersionManager
from unittest.mock import patch
import semver
# Used for debug
# import pprint


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
        self.fs.create_dir('/tmp/images/9.0.x/8.1-fpm')
        self.fs.create_dir('/tmp/images/9.0.x/8.1-apache')
        self.fs.create_dir('/tmp/images/9.0.x/8.2-fpm')
        self.fs.create_dir('/tmp/images/9.0.x/8.2-apache')
        self.fs.create_dir('/tmp/images/9.0.x/8.3-fpm')
        self.fs.create_dir('/tmp/images/9.0.x/8.3-apache')
        self.fs.create_dir('/tmp/images/nightly/7.1-fpm')
        self.fs.create_dir('/tmp/images/nightly/7.1-apache')
        self.fs.create_dir('/tmp/images/nightly/7.2-fpm')
        self.fs.create_dir('/tmp/images/nightly/7.2-apache')
        self.fs.create_dir('/tmp/images/nightly/7.3-fpm')
        self.fs.create_dir('/tmp/images/nightly/7.3-apache')
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
        '1.7.6.24': ('5.6', '7.1', '7.2'),
        '1.7.6.x': ('5.6', '7.1', '7.2'),
        '1.7.7.0-rc.1': ('7.1', '7.2', '7.3'),
        '8.0.0': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.0.0-rc.1': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.1.0': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.1.3': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '8.1.x': ('7.2', '7.3', '7.4', '8.0', '8.1'),
        '9.0.x': ('8.1', '8.2', '8.3'),
        'nightly': ('7.1', '7.2', '7.3'),
    }

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_split_prestashop_version(self):
        result = self.version_manager.split_prestashop_version('8.0.0')
        self.assertEqual(
            {'version': '8.0.0', 'major': '8', 'minor': '0', 'patch': '0', 'prerelease': None},
            result
        )
        result = self.version_manager.split_prestashop_version('10.2.24')
        self.assertEqual(
            {'version': '10.2.24', 'major': '10', 'minor': '2', 'patch': '24', 'prerelease': None},
            result
        )
        result = self.version_manager.split_prestashop_version('9.0.x')
        self.assertEqual(
            {'version': '9.0.x', 'major': '9', 'minor': '0', 'patch': 'x', 'prerelease': None},
            result
        )
        result = self.version_manager.split_prestashop_version('1.7.4.3')
        self.assertEqual(
            {'version': '1.7.4.3', 'major': '1.7', 'minor': '4', 'patch': '3', 'prerelease': None},
            result
        )
        result = self.version_manager.split_prestashop_version('1.7.8.x')
        self.assertEqual(
            {'version': '1.7.8.x', 'major': '1.7', 'minor': '8', 'patch': 'x', 'prerelease': None},
            result
        )
        result = self.version_manager.split_prestashop_version('1.7.7.0-rc.1')
        self.assertEqual(
            {'version': '1.7.7.0', 'major': '1.7', 'minor': '7', 'patch': '0', 'prerelease': 'rc.1'},
            result
        )
        result = self.version_manager.split_prestashop_version('nightly')
        self.assertEqual(
            None,
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_last_patch_from_version(self):
        result = self.version_manager.get_last_patch_from_version('1.7.6.4')
        self.assertEqual(
            '24',
            result
        )
        result = self.version_manager.get_last_patch_from_version('8.0.0')
        self.assertEqual(
            '0',
            result
        )
        result = self.version_manager.get_last_patch_from_version('8.1.0')
        self.assertEqual(
            '3',
            result
        )
        result = self.version_manager.get_last_patch_from_version('8.1.3')
        self.assertEqual(
            '3',
            result
        )
        result = self.version_manager.get_last_patch_from_version('8.1.x')
        self.assertEqual(
            '3',
            result
        )
        result = self.version_manager.get_last_patch_from_version('9.0.x')
        self.assertEqual(
            None,
            result
        )
        result = self.version_manager.get_last_patch_from_version('nightly')
        self.assertEqual(
            None,
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_ps_version(self):
        # Existing patch versions deduce the branch version with a finishing x
        result = self.version_manager.get_version_from_string('1.7.6.8')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'branch_version': '1.7.6.x', 'php_versions': ('5.6', '7.1', '7.2'), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0')
        self.assertEqual(
            {'ps_version': '8.0.0', 'branch_version': '8.0.x', 'php_versions': ('7.2', '7.3', '7.4', '8.0', '8.1'), 'container_version': None},
            result
        )
        # Branch input return target version patch + 1
        result = self.version_manager.get_version_from_string('8.1.x')
        self.assertEqual(
            {'ps_version': '8.1.4', 'branch_version': '8.1.x', 'php_versions': ('7.2', '7.3', '7.4', '8.0', '8.1'), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('1.7.6.x')
        self.assertEqual(
            {'ps_version': '1.7.6.25', 'branch_version': '1.7.6.x', 'php_versions': ('5.6', '7.1', '7.2'), 'container_version': None},
            result
        )
        # Branch input with no other patch versions returns patch 0
        result = self.version_manager.get_version_from_string('9.0.x')
        self.assertEqual(
            {'ps_version': '9.0.0', 'branch_version': '9.0.x', 'php_versions': ('8.1', '8.2', '8.3'), 'container_version': None},
            result
        )
        # Nightly version uses develop as the branch
        result = self.version_manager.get_version_from_string('nightly')
        self.assertEqual(
            {'ps_version': 'nightly', 'branch_version': 'develop', 'php_versions': ('7.1', '7.2', '7.3'), 'container_version': None},
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
            {'ps_version': '1.7.6.8', 'branch_version': '1.7.6.x', 'php_versions': ('5.6',), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-7.2')
        self.assertEqual(
            {'ps_version': '8.0.0', 'branch_version': '8.0.x', 'php_versions': ('7.2',), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('9.0.x-8.2')
        self.assertEqual(
            {'ps_version': '9.0.0', 'branch_version': '9.0.x', 'php_versions': ('8.2',), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('nightly-7.2')
        self.assertEqual(
            {'ps_version': 'nightly', 'branch_version': 'develop', 'php_versions': ('7.2',), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_container_version_and_type(self):
        result = self.version_manager.get_version_from_string('1.7.6.8-5.6-fpm')
        self.assertEqual(
            {'ps_version': '1.7.6.8', 'branch_version': '1.7.6.x', 'php_versions': ('5.6',), 'container_version': 'fpm'},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-7.2-fpm')
        self.assertEqual(
            {'ps_version': '8.0.0', 'branch_version': '8.0.x', 'php_versions': ('7.2',), 'container_version': 'fpm'},
            result
        )
        result = self.version_manager.get_version_from_string('9.0.x-8.2-fpm')
        self.assertEqual(
            {'ps_version': '9.0.0', 'branch_version': '9.0.x', 'php_versions': ('8.2',), 'container_version': 'fpm'},
            result
        )
        result = self.version_manager.get_version_from_string('nightly-7.2-fpm')
        self.assertEqual(
            {'ps_version': 'nightly', 'branch_version': 'develop', 'php_versions': ('7.2',), 'container_version': 'fpm'},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_pre_release_and_without_container_version_and_type(self):
        result = self.version_manager.get_version_from_string('1.7.7.0-rc.1')
        self.assertEqual(
            {'ps_version': '1.7.7.0-rc.1', 'branch_version': '1.7.7.x', 'php_versions': ('7.1', '7.2', '7.3'), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-rc.1')
        self.assertEqual(
            {'ps_version': '8.0.0-rc.1', 'branch_version': '8.0.x', 'php_versions': ('7.2', '7.3', '7.4', '8.0', '8.1'), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_pre_release_and_php_version_and_without_container_version(self):
        result = self.version_manager.get_version_from_string('1.7.7.0-rc.1-7.3')
        self.assertEqual(
            {'ps_version': '1.7.7.0-rc.1', 'branch_version': '1.7.7.x', 'php_versions': ('7.3',), 'container_version': None},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-rc.1-7.3')
        self.assertEqual(
            {'ps_version': '8.0.0-rc.1', 'branch_version': '8.0.x', 'php_versions': ('7.3',), 'container_version': None},
            result
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_version_from_string_with_pre_release_and_php_version_and_with_container_version(self):
        result = self.version_manager.get_version_from_string('1.7.7.0-rc.1-7.3-apache')
        self.assertEqual(
            {'ps_version': '1.7.7.0-rc.1', 'branch_version': '1.7.7.x', 'php_versions': ('7.3',), 'container_version': 'apache'},
            result
        )
        result = self.version_manager.get_version_from_string('8.0.0-rc.1-7.3-apache')
        self.assertEqual(
            {'ps_version': '8.0.0-rc.1', 'branch_version': '8.0.x', 'php_versions': ('7.3',), 'container_version': 'apache'},
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
        self.assertEqual(
            {
                '9.0.x-8.1-apache': '/tmp/images/9.0.x/8.1-apache',
                '9.0.x-8.1-fpm': '/tmp/images/9.0.x/8.1-fpm',
                '9.0.x-8.2-apache': '/tmp/images/9.0.x/8.2-apache',
                '9.0.x-8.2-fpm': '/tmp/images/9.0.x/8.2-fpm',
                '9.0.x-8.3-apache': '/tmp/images/9.0.x/8.3-apache',
                '9.0.x-8.3-fpm': '/tmp/images/9.0.x/8.3-fpm',
            },
            self.version_manager.parse_version('9.0.x')
        )
        self.assertEqual(
            {
                'nightly-7.1-apache': '/tmp/images/nightly/7.1-apache',
                'nightly-7.1-fpm': '/tmp/images/nightly/7.1-fpm',
                'nightly-7.2-apache': '/tmp/images/nightly/7.2-apache',
                'nightly-7.2-fpm': '/tmp/images/nightly/7.2-fpm',
                'nightly-7.3-apache': '/tmp/images/nightly/7.3-apache',
                'nightly-7.3-fpm': '/tmp/images/nightly/7.3-fpm',
            },
            self.version_manager.parse_version('nightly')
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
        self.assertEqual(
            {
                '9.0.x-8.2-apache': '/tmp/images/9.0.x/8.2-apache',
                '9.0.x-8.2-fpm': '/tmp/images/9.0.x/8.2-fpm',
            },
            self.version_manager.parse_version('9.0.x-8.2')
        )
        self.assertEqual(
            {
                'nightly-7.2-apache': '/tmp/images/nightly/7.2-apache',
                'nightly-7.2-fpm': '/tmp/images/nightly/7.2-fpm',
            },
            self.version_manager.parse_version('nightly-7.2')
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
        self.assertEqual(
            {
                '9.0.x-8.2-apache': '/tmp/images/9.0.x/8.2-apache',
            },
            self.version_manager.parse_version('9.0.x-8.2-apache')
        )
        self.assertEqual(
            {
                'nightly-7.2-apache': '/tmp/images/nightly/7.2-apache',
            },
            self.version_manager.parse_version('nightly-7.2-apache')
        )

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_versions(self):
        manager_versions = self.version_manager.get_versions()
        expected_versions = {
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
            '1.7.6.24-5.6-fpm': '/tmp/images/1.7.6.24/5.6-fpm',
            '1.7.6.24-5.6-apache': '/tmp/images/1.7.6.24/5.6-apache',
            '1.7.6.24-7.1-fpm': '/tmp/images/1.7.6.24/7.1-fpm',
            '1.7.6.24-7.1-apache': '/tmp/images/1.7.6.24/7.1-apache',
            '1.7.6.24-7.2-fpm': '/tmp/images/1.7.6.24/7.2-fpm',
            '1.7.6.24-7.2-apache': '/tmp/images/1.7.6.24/7.2-apache',
            '1.7.6.x-5.6-fpm': '/tmp/images/1.7.6.x/5.6-fpm',
            '1.7.6.x-5.6-apache': '/tmp/images/1.7.6.x/5.6-apache',
            '1.7.6.x-7.1-fpm': '/tmp/images/1.7.6.x/7.1-fpm',
            '1.7.6.x-7.1-apache': '/tmp/images/1.7.6.x/7.1-apache',
            '1.7.6.x-7.2-fpm': '/tmp/images/1.7.6.x/7.2-fpm',
            '1.7.6.x-7.2-apache': '/tmp/images/1.7.6.x/7.2-apache',
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
            '8.1.x-7.2-fpm': '/tmp/images/8.1.x/7.2-fpm',
            '8.1.x-7.2-apache': '/tmp/images/8.1.x/7.2-apache',
            '8.1.x-7.3-fpm': '/tmp/images/8.1.x/7.3-fpm',
            '8.1.x-7.3-apache': '/tmp/images/8.1.x/7.3-apache',
            '8.1.x-7.4-fpm': '/tmp/images/8.1.x/7.4-fpm',
            '8.1.x-7.4-apache': '/tmp/images/8.1.x/7.4-apache',
            '8.1.x-8.0-fpm': '/tmp/images/8.1.x/8.0-fpm',
            '8.1.x-8.0-apache': '/tmp/images/8.1.x/8.0-apache',
            '8.1.x-8.1-fpm': '/tmp/images/8.1.x/8.1-fpm',
            '8.1.x-8.1-apache': '/tmp/images/8.1.x/8.1-apache',
            '9.0.x-8.1-fpm': '/tmp/images/9.0.x/8.1-fpm',
            '9.0.x-8.1-apache': '/tmp/images/9.0.x/8.1-apache',
            '9.0.x-8.2-fpm': '/tmp/images/9.0.x/8.2-fpm',
            '9.0.x-8.2-apache': '/tmp/images/9.0.x/8.2-apache',
            '9.0.x-8.3-fpm': '/tmp/images/9.0.x/8.3-fpm',
            '9.0.x-8.3-apache': '/tmp/images/9.0.x/8.3-apache',
            'nightly-7.1-fpm': '/tmp/images/nightly/7.1-fpm',
            'nightly-7.1-apache': '/tmp/images/nightly/7.1-apache',
            'nightly-7.2-fpm': '/tmp/images/nightly/7.2-fpm',
            'nightly-7.2-apache': '/tmp/images/nightly/7.2-apache',
            'nightly-7.3-fpm': '/tmp/images/nightly/7.3-fpm',
            'nightly-7.3-apache': '/tmp/images/nightly/7.3-apache',
        }
        # Useful for debug
        # pprint.pp(manager_versions)
        # pprint.pp(expected_versions)
        # diff = list(set(manager_versions) - set(expected_versions))
        # print(diff)

        self.assertEqual(expected_versions, manager_versions)

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_ps_versions_aliases(self):
        expected_versions_aliases = {
            '1.7': {
                'version': semver.VersionInfo(7, 6, 24), 'value': '1.7.6.24'
            },
            '1.7.5': {
                'version': semver.VersionInfo(7, 5, 1), 'value': '1.7.5.1'
            },
            '1.7.5.1': {
                'version': semver.VersionInfo(7, 5, 1), 'value': '1.7.5.1'
            },
            'latest': {
                'version': semver.VersionInfo(8, 1, 3), 'value': '8.1.3'
            },
            '1.7.6': {
                'version': semver.VersionInfo(7, 6, 24), 'value': '1.7.6.24'
            },
            '1.7.6.4': {
                'version': semver.VersionInfo(7, 6, 4), 'value': '1.7.6.4'
            },
            '1.7.6.5': {
                'version': semver.VersionInfo(7, 6, 5), 'value': '1.7.6.5'
            },
            '1.7.6.8': {
                'version': semver.VersionInfo(7, 6, 8), 'value': '1.7.6.8'
            },
            '1.7.6.24': {
                'version': semver.VersionInfo(7, 6, 24), 'value': '1.7.6.24'
            },
            '1.7.6.x': {
                'value': '1.7.6.x'
            },
            '1.7.7.0-rc.1': {
                'value': '1.7.7.0-rc.1'
            },
            '8': {
                'version': semver.VersionInfo(8, 1, 3), 'value': '8.1.3'
            },
            '8.0': {
                'version': semver.VersionInfo(8, 0, 0), 'value': '8.0.0'
            },
            '8.0.0': {
                'version': semver.VersionInfo(8, 0, 0), 'value': '8.0.0'
            },
            '8.0.0-rc.1': {
                'value': '8.0.0-rc.1'
            },
            '8.1': {
                'version': semver.VersionInfo(8, 1, 3), 'value': '8.1.3'
            },
            '8.1.0': {
                'version': semver.VersionInfo(8, 1, 0), 'value': '8.1.0'
            },
            '8.1.3': {
                'version': semver.VersionInfo(8, 1, 3), 'value': '8.1.3'
            },
            '8.1.x': {
                'value': '8.1.x'
            },
            '9.0.x': {
                'value': '9.0.x'
            },
            'nightly': {
                'value': 'nightly'
            },
        }
        manager_versions_aliases = self.version_manager.get_ps_versions_aliases()
        # Useful for debug
        # pprint.pp(manager_versions_aliases)
        # pprint.pp(expected_versions_aliases)

        self.assertEqual(expected_versions_aliases, manager_versions_aliases)

    @patch('prestashop_docker.version_manager.VERSIONS', all_versions)
    def test_get_aliases(self):
        expected_aliases = {
            '1.7.6.24-5.6-apache': ['1.7-5.6', '1.7.6-5.6', '1.7.6.24-5.6'],
            '1.7.6.24-7.1-apache': ['1.7-7.1', '1.7.6-7.1', '1.7.6.24-7.1'],
            '1.7.6.24-7.2-apache': [
                '1.7-7.2',
                '1.7',
                '1.7-apache',
                '1.7.6-7.2',
                '1.7.6',
                '1.7.6-apache',
                '1.7.6.24-7.2',
                '1.7.6.24',
                '1.7.6.24-apache',
            ],
            '1.7.6.24-7.2-fpm': ['1.7-fpm', '1.7.6-fpm', '1.7.6.24-fpm'],
            '1.7.6.8-5.6-apache': ['1.7.6.8-5.6'],
            '1.7.6.8-7.1-apache': ['1.7.6.8-7.1'],
            '1.7.6.8-7.2-apache': ['1.7.6.8-7.2', '1.7.6.8', '1.7.6.8-apache'],
            '1.7.6.8-7.2-fpm': ['1.7.6.8-fpm'],
            '1.7.6.x-5.6-apache': ['1.7.6.x-5.6'],
            '1.7.6.x-7.1-apache': ['1.7.6.x-7.1'],
            '1.7.6.x-7.2-apache': ['1.7.6.x-7.2', '1.7.6.x', '1.7.6.x-apache'],
            '1.7.6.x-7.2-fpm': ['1.7.6.x-fpm'],
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
            '8.1.x-7.2-apache': ['8.1.x-7.2'],
            '8.1.x-7.3-apache': ['8.1.x-7.3'],
            '8.1.x-7.4-apache': ['8.1.x-7.4'],
            '8.1.x-8.0-apache': ['8.1.x-8.0'],
            '8.1.x-8.1-apache': ['8.1.x-8.1', '8.1.x', '8.1.x-apache'],
            '8.1.x-8.1-fpm': ['8.1.x-fpm'],
            '9.0.x-8.1-apache': ['9.0.x-8.1'],
            '9.0.x-8.2-apache': ['9.0.x-8.2'],
            '9.0.x-8.3-apache': ['9.0.x-8.3', '9.0.x', '9.0.x-apache'],
            '9.0.x-8.3-fpm': ['9.0.x-fpm'],
            'nightly-7.1-apache': ['nightly-7.1'],
            'nightly-7.2-apache': ['nightly-7.2'],
            'nightly-7.3-apache': ['nightly-7.3', 'nightly', 'nightly-apache'],
            'nightly-7.3-fpm': ['nightly-fpm'],
        }
        manager_aliases = self.version_manager.get_aliases()
        # Useful for debug
        # print('### manager')
        # pprint.pp(manager_aliases)
        # print('### expected')
        # pprint.pp(expected_aliases)
        # diff = list(set(manager_aliases) - set(expected_aliases))
        # print(diff)

        self.assertEqual(
            expected_aliases,
            manager_aliases,
        )
