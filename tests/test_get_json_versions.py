import io
import json
import os
import tempfile
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch
import get_json_versions
from get_json_versions import (
    get_base_images,
    get_php_versions_for,
    get_ps_versions,
    get_unknown_php_versions,
    parse_php_versions,
)
from versions import VERSIONS as REAL_VERSIONS

VERSIONS = {
    '1.7.8.0': ('7.1', '7.4'),
    '8.2.x': ('7.4', '8.1'),
    'nightly': ('8.1', '8.5'),
}
BASE_IMAGES = ['8.5-fpm', '7.4-apache', '8.1-apache', '7.4-fpm', '8.1-fpm', '8.5-apache']


class GetJsonVersionsTestCase(TestCase):
    def test_parse_php_versions(self):
        self.assertIsNone(parse_php_versions(None))
        self.assertIsNone(parse_php_versions(' all '))
        self.assertEqual(['8.1', '8.4'], parse_php_versions('8.1, 8.4,'))

    def test_unknown_php_versions(self):
        self.assertEqual([], get_unknown_php_versions(['7.1', '8.5'], VERSIONS, BASE_IMAGES))
        self.assertEqual(['5.6', '8'], get_unknown_php_versions(['5.6', '8.1', '8'], VERSIONS, BASE_IMAGES))

    def test_ps_versions(self):
        self.assertEqual(['1.7.8.0', '8.2.x', 'nightly'], get_ps_versions(VERSIONS))
        self.assertEqual(['1.7.8.0', '8.2.x'], get_ps_versions(VERSIONS, ['7.4']))
        self.assertEqual(['nightly'], get_ps_versions(VERSIONS, ['8.5']))
        self.assertEqual([], get_ps_versions(VERSIONS, ['8.4']))

    def test_php_versions_for(self):
        self.assertEqual(['7.4', '8.1'], get_php_versions_for('8.2.x', VERSIONS))
        self.assertEqual(['8.1'], get_php_versions_for('8.2.x', VERSIONS, ['8.1', '8.5']))

    def test_base_images(self):
        self.assertEqual(sorted(BASE_IMAGES), get_base_images(BASE_IMAGES))
        self.assertEqual(['8.1-apache', '8.1-fpm', '8.5-apache', '8.5-fpm'], get_base_images(BASE_IMAGES, ['8.1', '8.5']))


class GetJsonVersionsCliTestCase(TestCase):
    def setUp(self):
        self.base_dir = tempfile.TemporaryDirectory()
        for image in BASE_IMAGES:
            os.mkdir(os.path.join(self.base_dir.name, image))
        # Files are not base images
        open(os.path.join(self.base_dir.name, '.DS_Store'), 'w').close()

    def tearDown(self):
        self.base_dir.cleanup()

    def run_cli(self, *args, versions=VERSIONS):
        output = io.StringIO()
        with patch('sys.argv', ['get_json_versions.py', *args]), \
                patch.object(get_json_versions, 'VERSIONS', versions), \
                patch.object(get_json_versions, 'BASE_IMAGES_DIR', self.base_dir.name), \
                redirect_stdout(output):
            get_json_versions.main()
        return output.getvalue().strip()

    def test_no_argument_lists_every_version_of_versions_file(self):
        # Output used by publish.yml, must not change
        self.assertEqual(json.dumps(list(REAL_VERSIONS)), self.run_cli(versions=REAL_VERSIONS))

    def test_all_is_same_as_no_filter(self):
        self.assertEqual(self.run_cli(), self.run_cli('--php', 'all'))
        self.assertEqual(self.run_cli('--base'), self.run_cli('--php', 'all', '--base'))
        self.assertEqual(self.run_cli('--php-for', '8.2.x'), self.run_cli('--php', 'all', '--php-for', '8.2.x'))

    def test_ps_versions_filtered_by_php(self):
        self.assertEqual(['1.7.8.0', '8.2.x'], json.loads(self.run_cli('--php', '7.4')))

    def test_base_images(self):
        self.assertEqual(sorted(BASE_IMAGES), json.loads(self.run_cli('--base')))
        self.assertEqual(['8.5-apache', '8.5-fpm'], json.loads(self.run_cli('--php', '8.5', '--base')))

    def test_php_versions_for(self):
        self.assertEqual('7.4 8.1', self.run_cli('--php-for', '8.2.x'))
        self.assertEqual('8.1', self.run_cli('--php', '8.1,8.5', '--php-for', '8.2.x'))

    def test_unknown_php_version_fails(self):
        with self.assertRaises(SystemExit) as context:
            self.run_cli('--php', '8.1,5.6')
        self.assertEqual('Unknown PHP versions: 5.6', context.exception.code)

    def test_blank_php_selection_fails(self):
        for selection in ('', ' ', ' , '):
            with self.assertRaises(SystemExit) as context:
                self.run_cli('--php', selection, '--base')
            self.assertEqual('No PHP version selected, use "all" to select every version', context.exception.code)

    def test_unknown_ps_version_fails(self):
        with self.assertRaises(SystemExit) as context:
            self.run_cli('--php-for', 'foo')
        self.assertEqual('Unknown PrestaShop version: foo', context.exception.code)
