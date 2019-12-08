from setuptools import setup, find_packages

setup(
    name="roguelike",
    version="0.0.2",
    description="",

    author="Kijima Daigo",


    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[""],
    tests_require=['pytest', 'pytest-mock'],

    entry_points={
        'console_scripts': [
            'roguelike = roguelike.roguelike:Game',
        ]
    },
)
