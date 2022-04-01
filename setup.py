from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as req_file:
    requirements = list(filter(None, req_file.read().split("\n")))

__version__ = None
with open("yamlhparams/version.py") as version_file:
    exec(version_file.read())
if __version__ is None:
    raise ValueError("Did not find __version__ in version.py file.")

setup(
    name='yamlhparams',
    version=__version__,
    description='A small extension to the ruamel.yaml CommentedMap YAML parser intended for roundtrip loading, '
                'manipulation and saving of hyperparameters stored in YAML files while (optionally) performing '
                'basic version control against a separate Python package.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Mathias Perslev',
    author_email='map@di.ku.dk',
    url='https://github.com/perslev/yamlhparams',
    packages=find_packages(),
    package_dir={'yamlhparams': 'yamlhparams'},
    include_package_data=True,
    install_requires=requirements,
    license_files=('LICENSE.txt',),
    classifiers=['Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11']
)
