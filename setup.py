import re
from os.path import join, dirname

from setuptools import setup


with open(join(dirname(__file__), 'sysmon.py'), "r", encoding="utf-8") as f:
    version = re.match('.*__version__ = \'(.*?)\'', f.read(), re.S).group(1)


dependencies = [
    'easycli',
    'psutil'
]


setup(
    name='sysmon',
    version=version,
    py_modules=['sysmon'],
    install_requires=dependencies,
    include_package_data=True,
    license='MIT License',
    entry_points={
        'console_scripts': [
            'sysmon = sysmon:Sysmon.quickstart',
        ]
    }
)
