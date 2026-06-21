# setup.py
from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'nao_dance_pkg'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'worlds'),
            glob(os.path.join('worlds', '*.wbt'))),
        (os.path.join('share', package_name, 'controllers'),
            glob(os.path.join('controllers', '*'))),
        (os.path.join('share', package_name, 'resource'),
            glob(os.path.join('resource', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Fatima Jadoon',
    maintainer_email='fatima@university.ac.uk',
    description='NAO humanoid robot dance routine',
    license='MIT',
    tests_require=['pytest'],
    entry_points={'console_scripts': []},
)
