from setuptools import setup

setup(
    name='redcanary',
    version='0.2a',
    packages=['redcanary'],
    url='https://github.com/redcanaryco/openapi/tree/v2',
    license='',
    author='Keith McCammon',
    author_email='keith@redcanary.co',
    description='Python client for Red Canary open API.',
    install_requires=[
    'requests',
    'django-dotenv'],
    tests_require=[
    ]
)
