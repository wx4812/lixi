from setuptools import setup
import os
from glob import glob

package_name = 'turtle_maze'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@example.com',
    description='Week 14: turtlesim maze remote control via WebSocket',
    license='MIT',
    entry_points={
        'console_scripts': [
            'bridge  = turtle_maze.turtlesim_web_bridge:main',
            'explore = turtle_maze.explorer:main',
        ],
    },
)
