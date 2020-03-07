import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lexc_parser',
    version='0.0.1',
    author='Robert Reynolds',
    author_email='ReynoldsRJR@gmail.com',
    cmdclass={'install': PostInstallCommand},
    description='Object-oriented approach to filtering, modifying, or extracting information from lexc.',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/reynoldsnlp/lexc_parser',
    packages=setuptools.find_packages(),
    package_dir={'lexc_parser': 'lexc_parser'},
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
