from setuptools import setup, find_packages

setup(
    name="roguelike",
    version="0.0.2",
    install_requires=[""],
    py_modules=[
        'roguelike',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    tests_require=['pytest', 'pytest-mock'],
)