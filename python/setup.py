from setuptools import setup, find_packages

setup(
    name='redcanary',
    version='0.3',
    packages=find_packages(),
    url='https://github.com/redcanaryco/openapi/tree/v2',
    license='',
    author='Keith McCammon',
    author_email='keith@redcanary.co',
    description='Python client for Red Canary open API.',
    install_requires=[
        'requests[security]',
        'django-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'redcanary=redcanary.__main__:main'
        ]
    },
    test_suite='test',
    tests_require=[
    ]
)
