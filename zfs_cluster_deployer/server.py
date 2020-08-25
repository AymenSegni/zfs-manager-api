from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from zfs_cluster_deployer import logger, app


def main(port=8888):
    http_server = HTTPServer(WSGIContainer(app))
    http_server.bind(port)
    try:
        http_server.start(1)
        IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("Shutting down the server... Good Bye!")
        exit(0)

if __name__ == '__main__':
    main()