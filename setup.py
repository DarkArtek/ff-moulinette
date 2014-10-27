from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='ff-moulinette',
    version='0.1',

    description='A simple character sheet crawler for Final Fantasy XIV characters.',
    long_description=readme,

    author='Pierre Sudron',
    author_email='contact@giant-teapot.org',

    include_package_data = True,
    package_data = {
        '':  ['LICENSE'],
    },
    license='MIT',

    packages=find_packages()
)