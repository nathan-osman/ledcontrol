from distutils.core import setup

import ledcontrol

setup(
    name='ledcontrol',
    version=ledcontrol.__version__,
    description='Controls LED devices using the usbled Linux kernel module',
    author='Nathan Osman',
    author_email='admin@quickmediasolutions.com',
    url='https://github.com/nathan-osman/ledcontrol',
    license='MIT',
    packages=['ledcontrol'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Topic :: System :: Hardware'
    ],
)
