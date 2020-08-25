
from salt.client import LocalClient
import cPickle as cp
from zfs_cluster_deployer import logger


class BaseController(object):
    @classmethod
    def get_devices(cls, storage_node):
        local = LocalClient()
        response = local.cmd(storage_node, 'cmd.run', ["fdisk -l | grep Error"])
        return response

    @classmethod
    def __write_data(cls, data):
        with open("/var/run/zfs_snapshots.pck", 'wb') as fpck:
            cp.dump(data, fpck)

    @classmethod
    def __read_data(cls):
        data = None
        try:
            with open("/var/run/zfs_snapshots.pck", 'rb') as fpck:
                data = cp.load(fpck)
        except Exception as e:
            logger.error(e)
        return data

    @classmethod
    def get_snapshot(cls, storage_node, pool_name, dataset=None):
        data = cls.__read_data()
        if not data:
            return -1
        else:
            if dataset:
                try:
                    return data[storage_node][pool_name][dataset]
                except KeyError:
                    return -1
                except Exception as e:
                    logger.error(e)
            else:
                try:
                    return data[storage_node][pool_name]["rc_snapshot"]
                except KeyError:
                    return -1
                except Exception as e:
                    logger.error(e)

    @classmethod
    def set_snapshot(cls, storage_node, pool_name, snapshot, dataset=None):
        data = cls.__read_data()
        if not data:
            data = {}
        if dataset:
            data[storage_node][pool_name][dataset] = snapshot
        else:
            data[storage_node] = {pool_name: {'rc_snapshot': snapshot}}
        cls.__write_data(data)

    @classmethod
    def _delete_all_snapshots(cls, minion_id):
        client = LocalClient()
        cmd = "zfs list -H -t snapshot -o name | xargs -I {} zfs destroy {}"
        response = client.cmd(minion_id, "cmd.run", [cmd])
        return response

    @classmethod
    def _get_ipaddr(cls, minion_id):
        client = LocalClient()
        response = client.cmd(minion_id, "network.ip_addrs", [])
        return response[minion_id][0]