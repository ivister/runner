from setuptools import setup

setup(
    name="dtask",
    version="0.0.3",
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
            [  # 'dtask_run=dockertasks.runner:main',
               # 'dtask_stop=dockertasks.stopper:main',
             'dtask_build=dockertasks.builder:main',
             'dtask_loadim=dockertasks.runner:load_image',  # TODO load image from file
             'dtask_crnet=dockertasks.runner:create_network',  # TODO check
             'dtask_crhf=dockertasks.runner:create_hostsfile',  # TODO create hostsfile
             'dtask_remhf=dockertasks.stopper:remove_hostsfile',  # TODO remove hostfile
             'dtask_remimage=dockertasks.stopper:remove_docker_image',  # TODO remove image
             'dtask_runcont=dockertasks.runner:run_image',  # TODO runcont
             'dtask_stopcont=dockertasks.stopper:stop_cont',  # TODO stop cont
             'dtask_remcont=dockertasks.stopper:remove_cont',  # TODO remove cont
             'dtask_remnet=dockertasks.stopper:remove_net',  #
             ]
    }
)
