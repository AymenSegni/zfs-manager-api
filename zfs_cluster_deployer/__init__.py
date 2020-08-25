from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from tornado.log import logging, enable_pretty_logging

app = Flask(__name__)
app.config.from_object('zfs_cluster_deployer.config')
CONFIGS = app.config

DataBase = MongoEngine(app)

api = Api(app)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
enable_pretty_logging()

from zfs_cluster_deployer.application.Views import routes