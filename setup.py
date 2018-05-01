from setuptools import setup

setup(
    name="dockertasks",
    version="0.0.2",
    packages=['dockertasks'],
    description="Package for SUPPZ",
    long_description="",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='docker SUPPZ',
    url='http://github.com/ivister/runner',
    author="Andrey Alexeev",
    author_email="salexs95@yandex.ru",
    install_requires=['paramiko==2.4.1'],
    entry_points={
        'console_scripts':
            ['task_run=dockertasks.runner:main',
             'task_stop=dockertasks.stopper:main',
             'task_build=dockertasks.builder:main'
             ]
    }
)
