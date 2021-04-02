from setuptools import setup, find_packages

setup(
    name='redcanary',
    version='0.4',
    packages=find_packages(),
    url='https://github.com/redcanaryco/openapi/tree/master',
    license='',
    author='Red Canary',
    author_email='support@redcanary.co',
    description='Python client for Red Canary open API.',
    install_requires=[
        'requests'
    ]
)
