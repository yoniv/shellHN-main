from setuptools import setup

setup(
    name="shellHN",
    version='0.1',
    py_modules=['shell_hn'],
    install_requires=[
        'Click',
        'requests',
        'aiohttp',
        'html2text',
        'aiohttp',
        'asyncio',
        'logging',
    ],
    entry_points='''
        [console_scripts]
        hn=shell_hn:shell
    ''',
)