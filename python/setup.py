from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='redcanary',
    version='0.4',
    python_requires='>=3.6',
    packages=find_packages(),
    url='https://github.com/redcanaryco/openapi',
    license='MIT',
    author='Red Canary',
    author_email='opensource@redcanary.com',
    description='Python client for Red Canary open API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
