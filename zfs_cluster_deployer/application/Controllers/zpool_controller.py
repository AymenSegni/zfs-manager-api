
from zfs_cluster_deployer.application.Controllers import BaseController, LocalClient
from zfs_cluster_deployer.app_exceptions import HTTPExceptions
from zfs_cluster_deployer import logger


class ZpoolController(BaseController):
    @classmethod
    def zpool_create(cls, data):
        local = LocalClient()
        args = [data['name']]
        for device in data['devices']:
            args.append(device)
        logger.info("Creating zfs pool: %(pool_name)s in node: %(node)s" % {'pool_name': data['name'],
                                                                         'node': data['Storage-Node']})
        response = local.cmd(data['Storage-Node'], 'zpool.create', args, kwarg={'force': True})
        if not response:
            HTTPExceptions.time_out_error("Could not create pool due to time out error")
        return response

    @classmethod
    def zpool_list(cls, storage_node):
        local = LocalClient()
        response = local.cmd(storage_node, 'zpool.list')
        return response

    @classmethod
    def zpool_add(cls, data):
        local = LocalClient()
        args = [data['name']]
        for device in data['devices']:
            args.append(device)
        response = local.cmd(data['Storage-Node'], 'zpool.add', args)
        return response

    @classmethod
    def zpool_iostat(cls, storage_node, name=None):
        local = LocalClient()
        response = local.cmd(storage_node, 'zpool.iostat', [name])
        return response

    @classmethod
    def zpool_status(cls, storage_node, name=None):
        local = LocalClient()
        response = local.cmd(storage_node, 'zpool.status', [name])
        return response

    @classmethod
    def zpool_destroy(cls, storage_node, name):
        local = LocalClient()
        response = local.cmd(storage_node, 'zpool.destroy', [name])
        return response