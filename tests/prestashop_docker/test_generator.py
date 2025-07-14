import json
from pyfakefs.fake_filesystem_unittest import TestCase
from prestashop_docker.generator import Generator
from prestashop_docker.distribution_api import DistributionApi
from os import path


class GeneratorTestCase(TestCase):
    generator = None

    def setUp(self):
        fake_data = json.loads(open('tests/prestashop_docker/prestashop_versions.json').read())
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
        self.fs.create_file(
            'Dockerfile-branch.model',
            contents='''
            CONTAINER_VERSION: $container_version
            RUN apt -y install git
            ENV PS_BRANCH=$branch_version
            ENV NODE_VERSION=$node_version
            '''
        )

        self.generator = Generator(
            DistributionApi(fake_data),
            '/tmp/images',
            open('Dockerfile.model').read(),
            open('Dockerfile-nightly.model').read(),
            open('Dockerfile-branch.model').read()
        )

    def test_create_directory(self):
        self.assertFalse(path.exists('/tmp/images/test'))
        self.generator.create_directory('/tmp/images/test')
        self.assertTrue(path.exists('/tmp/images/test'))

    def test_generate_image(self):
        dockerfile = '/tmp/images/1.7.8.0/7.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '1.7.8.0',
            '7.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://api.prestashop-project.org/assets/prestashop/1.7.8.0/'
                'prestashop.zip',
                content
            )
            self.assertIn('PS_VERSION: 1.7.8.0', content)
            self.assertIn('CONTAINER_VERSION: 7.4-alpine', content)

    def test_generate_image_1788(self):
        dockerfile = '/tmp/images/1.7.8.8/7.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '1.7.8.8',
            '7.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://api.prestashop-project.org/assets/prestashop/1.7.8.8/'
                'prestashop.zip',
                content
            )
            self.assertIn('PS_VERSION: 1.7.8.8', content)
            self.assertIn('CONTAINER_VERSION: 7.4-alpine', content)

    def test_generate_image_1789(self):
        dockerfile = '/tmp/images/1.7.8.9/7.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '1.7.8.9',
            '7.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://api.prestashop-project.org/assets/prestashop/1.7.8.9/'
                'prestashop.zip',
                content
            )
            self.assertIn('PS_VERSION: 1.7.8.9', content)
            self.assertIn('CONTAINER_VERSION: 7.4-alpine', content)

    def test_generate_image_80(self):
        dockerfile = '/tmp/images/8.0.0/7.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '8.0.0',
            '7.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://api.prestashop-project.org/assets/prestashop/8.0.0/'
                'prestashop.zip',
                content
            )
            self.assertIn('PS_VERSION: 8.0.0', content)
            self.assertIn('CONTAINER_VERSION: 7.4-alpine', content)

    def test_generate_image_900(self):
        dockerfile = '/tmp/images/9.0.0/8.4-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '9.0.0',
            '8.4-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertIn(
                'PS_URL: https://api.prestashop-project.org/assets/prestashop-classic/9.0.0-3.0/'
                'prestashop.zip',
                content
            )
            self.assertIn('PS_VERSION: 9.0.0', content)
            self.assertIn('CONTAINER_VERSION: 8.4-alpine', content)

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

    def test_generate_nightly_90x_image(self):
        dockerfile = '/tmp/images/9.0.x/8.1-alpine/Dockerfile'
        self.assertFalse(path.exists(dockerfile))
        self.generator.generate_image(
            '9.0.x',
            '8.1-alpine'
        )
        self.assertTrue(path.exists(dockerfile))

        with open(dockerfile) as f:
            content = f.read()
            self.assertNotIn(
                'PS_URL',
                content
            )

            self.assertIn('PS_VERSION: 9.0.x', content)
            self.assertIn('CONTAINER_VERSION: 8.1-alpine', content)

    # def test_generate_branch_image(self):
    #     dockerfile = '/tmp/images/9.0.x/8.1-alpine/Dockerfile'
    #     self.assertFalse(path.exists(dockerfile))
    #     self.generator.generate_image(
    #         '9.0.x',
    #         '8.1-alpine'
    #     )
    #     self.assertTrue(path.exists(dockerfile))

    #     with open(dockerfile) as f:
    #         content = f.read()
    #         self.assertNotIn(
    #             'PS_URL',
    #             content
    #         )
    #         self.assertIn('CONTAINER_VERSION: 8.1-alpine', content)
    #         self.assertIn('RUN apt -y install git', content)
    #         self.assertIn('ENV PS_BRANCH=9.0.x', content)
    #         self.assertIn('ENV NODE_VERSION=v20.17.0', content)

    def test_generate_all(self):
        files = (
            '/tmp/images/1.7.8.8/7.3-apache/Dockerfile',
            '/tmp/images/1.7.8.8/7.3-fpm/Dockerfile',
            '/tmp/images/1.7.8.8/7.2-apache/Dockerfile',
            '/tmp/images/1.7.8.8/7.2-fpm/Dockerfile',
            '/tmp/images/8.0.0/7.2-apache/Dockerfile',
            '/tmp/images/8.0.0/7.2-fpm/Dockerfile',
            '/tmp/images/8.0.0/8.1-apache/Dockerfile',
            '/tmp/images/8.0.0/8.1-fpm/Dockerfile',
            '/tmp/images/9.0.x/8.1-apache/Dockerfile',
            '/tmp/images/9.0.x/8.1-fpm/Dockerfile',
            '/tmp/images/9.0.x/8.2-apache/Dockerfile',
            '/tmp/images/9.0.x/8.2-fpm/Dockerfile',
            '/tmp/images/9.0.x/8.3-apache/Dockerfile',
            '/tmp/images/9.0.x/8.3-fpm/Dockerfile',
            '/tmp/images/nightly/8.1-apache/Dockerfile',
            '/tmp/images/nightly/8.1-fpm/Dockerfile',
            '/tmp/images/nightly/8.2-apache/Dockerfile',
            '/tmp/images/nightly/8.2-fpm/Dockerfile',
            '/tmp/images/nightly/8.3-apache/Dockerfile',
            '/tmp/images/nightly/8.3-fpm/Dockerfile',
        )
        for f in files:
            self.assertFalse(path.exists(f))

        self.generator.generate_all(
            {
                '1.7.8.8': ('7.2', '7.3'),
                '8.0.0': ('7.2', '8.1'),
                '9.0.x': ('8.1', '8.2', '8.3'),
                'nightly': ('8.1', '8.2', '8.3'),
            }
        )

        for f in files:
            self.assertTrue(path.exists(f), msg='{} doesn''t exists'.format(f))
