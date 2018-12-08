#!/usr/bin/env python

from typing import Any, List
import glob
import os

from setuptools import find_packages, setup


ROOT_DIR = 'electricitymap-wrapper-api'
SRC_DIR = 'src'
REQS_DIR = 'requirements'


def get_version() -> str:
    with open('version') as f:
        version = f.read().rsplit(':', 1)[-1]
    return version


def get_readme() -> str:
    with open('README.md') as f:
        readme = f.read()
    return readme


def get_authors() -> str:
    with open('authors') as f:
        authors = [line.strip() for line in f if not line.strip().startswith('#')]
    return ', '.join(authors)


def get_package_data() -> List[str]:
    include_stmt = 'include'
    with open('MANIFEST.in') as f:
        includes = [line[len(include_stmt):].strip() for line in f if line.startswith(include_stmt)]
    return includes


def get_modules(src_folder: str) -> List[str]:
    return [os.path.splitext(os.path.basename(path))[0] for path in glob.glob(os.path.join(src_folder, '*.py'))]


def get_dependencies(requirements_folder: str, requirements_file: str) -> List[str]:
    with open(os.path.join(requirements_folder, requirements_file)) as f:
        return _flatten([_process_dependency_line(requirements_folder, req) for req in f])


def _process_dependency_line(requirements_folder: str, line: str) -> List[str]:
    clean_line = line.strip()
    if not clean_line or clean_line.startswith('#'):
        return []
    elif clean_line.startswith('-r'):
        requirements_file = clean_line[2:].strip()
        return get_dependencies(requirements_folder, requirements_file)
    else:
        return [clean_line]


def _flatten(list_of_lists: List[List[Any]]) -> List[Any]:
    return [value for inner_list in list_of_lists for value in inner_list]


setup(
    name=ROOT_DIR,
    version=get_version(),
    description="Wrapper around electricitymap-contrib to expose its functionality in a more Pythonic way.",
    long_description=get_readme(),
    author=get_authors(),
    author_email='michiel@vanherwegen.com',
    url='https://github.com/mvherweg/{}'.format(ROOT_DIR),
    packages=find_packages(SRC_DIR),
    package_dir={'': SRC_DIR},
    package_data={'': get_package_data()},
    include_package_data=True,
    py_modules=get_modules(SRC_DIR),
    zip_safe=True,
    install_requires=get_dependencies(REQS_DIR, 'core.txt'),
    tests_require=get_dependencies(REQS_DIR, 'test.txt')
)