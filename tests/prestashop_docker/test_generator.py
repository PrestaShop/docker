from pyfakefs.fake_filesystem_unittest import TestCase
from prestashop_docker.generator import Generator
from os import path


class GeneratorTestCase(TestCase):
    generator = None

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir('/tmp/images')
        self.fs.create_file(
            'Dockerfile.model',
            contents='''
            PS_URL: $ps_url
            PS_VERSION: $ps_version
            CONTAINER_VERSION: $container_version
            '''
        )
        self.fs.create_file(
            'Dockerfile-nightly.model',
            contents='''
            PS_VERSION: $ps_version
            CONTAINER_VERSION: $container_version
            '''
        )

        self.generator = Generator(
            '/tmp/images',
            open('Dockerfile.model').read(),
            open('Dockerfile-nightly.model').read()
        )

    def test_create_directory(self):
        self.assertFalse(path.exists('/tmp/images/test'))
        self.generator.create_directory('/tmp/images/test')
        self.assertTrue(path.exists('/tmp/images/test'))

    def test_generate_image(self):
        dockerfile = '/tmp/images/1.7.8/7.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '1.7.8',
            '7.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://www.prestashop.com/download/old/'
                'prestashop_1.7.8.zip',
                content
            )
            self.assertIn('PS_VERSION: 1.7.8', content)
            self.assertIn('CONTAINER_VERSION: 7.4-alpine', content)

    def test_generate_image_80(self):
        dockerfile = '/tmp/images/8.0/7.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '8.0',
            '7.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://github.com/PrestaShop/PrestaShop/releases/download/8.0/'
                'prestashop_8.0.zip',
                content
            )
            self.assertIn('PS_VERSION: 8.0', content)
            self.assertIn('CONTAINER_VERSION: 7.4-alpine', content)

    def test_generate_nightly_image(self):
        dockerfile = '/tmp/images/nightly/7.2-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            'nightly',
            '7.2-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertNotIn(
                'PS_URL',
                content
            )
            self.assertIn('PS_VERSION: nightly', content)
            self.assertIn('CONTAINER_VERSION: 7.2-alpine', content)

    def test_generate_all(self):
        files = (
            '/tmp/images/7.0/7.3-apache/Dockerfile',
            '/tmp/images/7.0/7.3-fpm/Dockerfile',
            '/tmp/images/7.0/7.2-apache/Dockerfile',
            '/tmp/images/7.0/7.2-fpm/Dockerfile',
            '/tmp/images/8.0/7.1-apache/Dockerfile',
            '/tmp/images/8.0/7.1-fpm/Dockerfile',
            '/tmp/images/8.0/5.6-apache/Dockerfile',
            '/tmp/images/8.0/5.6-fpm/Dockerfile',
        )
        for f in files:
            self.assertFalse(path.exists(f))

        self.generator.generate_all(
            {
                '7.0': ('7.2', '7.3'),
                '8.0': ('7.1', '5.6'),
            }
        )

        for f in files:
            self.assertTrue(path.exists(f), msg='{} doesn''t exists'.format(f))
