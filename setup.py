from setuptools import setup, find_packages

from io import open
from setuptools import setup
from cpcbasic import __version__ as version

VERSION = version
DESCRIPTION = 'SDK for Programing Basic in SO Windows, Linux and OSX'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="CPCBasic",
        version=VERSION,
        author="Destroyer",
        author_email="<destroyer.dcf@gmail.com>",
        description=DESCRIPTION,
        long_description=''.join(open('README.md', encoding='utf-8').readlines()),
        long_description_content_type='text/markdown',
        license="GPL",
        url="https://github.com/destroyer-dcf/cpcbasic",
        project_urls={
            "Bug Tracker": "https://github.com/destroyer-dcf/cpcbasic/issues",
        },
        keywords=['executable'],
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'jinja2',
            'ipaddress',
            'tabulate',
            'cerberus',
            'tqdm==4.64.1',
            'requests',
            'click',
            'prompt_toolkit'
        ],
        python_requires='>=3.6',
        classifiers=[
            'License :: OSI Approved :: GNU General Public License (GPL)',   
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
        ],
        entry_points={
            'console_scripts': [
                'cpcbasic=cpcbasic.__main__:main',
                'cpc=cpcbasic.__main__:main',
                'basic=cpcbasic.__main__:main',
            ],
        },
)