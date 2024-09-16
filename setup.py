"""
Author: Aymen Segni
Date: 12/11/17
"""
from setuptools import setup
setup(
    name="zfs_cluster_deployer",
    version="0",
    author="Aymen Segni",
    author_email="myemail",
    description="ZFS cluster manager api",
    install_requires=["Flask==0.10.1",
                      "Flask-RESTful==0.3.5",
                      "Werkzeug==0.10.4",
                      "flask-mongoengine==0.7.1",
                      "mongoengine==0.10.0",
                      "psutil==3.0.1",
                      "pymongo==3.0.3",
                      "requests==2.7.0",
                      "tornado==4.2"]
)
