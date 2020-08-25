
from zfs_cluster_deployer.application.Controllers import BaseController, LocalClient
from zfs_cluster_deployer import logger


class ZFSController(BaseController):
    @classmethod
    def zfs_list(cls, storage_node, name=None):
        local = LocalClient()
        args = []
        if name:
            args.append(name)
        response = local.cmd(storage_node, 'zfs.list', args)
        r = {}
        if "datasets" in response[storage_node]:
            pool_name = ""
            for line in response[storage_node]['datasets']:
                l = [item for item in line.split(" ") if item]
                logger.info(l)
                if l[0].find("NAME") == -1:
                    if l[0].find("/") == -1:
                        pool_name = l[0]
                        r[pool_name] = {'used': l[1],
                                        'available': l[2],
                                        'refer': l[3],
                                        'mountpoint': l[4],
                                        'datasets': []}
                    else:
                        r[pool_name]['datasets'].append({'name': "/".join(l[0].split("/")[1:]),
                                                         'used': l[1],
                                                         'available': l[2],
                                                         'refer': l[3],
                                                         'mountpoint': l[4]})
        return r if r else response

    @classmethod
    def zfs_create(cls, data):
        local = LocalClient()
        resp1 = local.cmd(data['Storage-Node'],
                          'zfs.create',
                          ["%(pool_name)s/%(name)s" % {'name': data['name'],
                                                       'pool_name': data['pool_name']}])
        resp2 = cls.zfs_set_quota(data)
        return [resp1, resp2]

    @classmethod
    def zfs_set_quota(cls, data):
        local = LocalClient()
        args = 'zfs set quota=%(quota)sG %(pool_name)s/%(name)s' % {'quota': data['quota'],
                                                                    'pool_name': data['pool_name'],
                                                                    'name': data['name']}
        response = local.cmd(data['Storage-Node'], 'cmd.run', [args])
        return response

    @classmethod
    def zfs_destroy(cls, data):
        local = LocalClient()
        cmd = "zfs destroy -r %(pool_name)s/%(name)s" % {'pool_name': data['pool_name'],
                                                         'name': data['name']}
        response = local.cmd(data['Storage-Node'], 'cmd.run', [cmd])
        return response

    @classmethod
    def zfs_replicate_pool(cls, data):
        local = LocalClient()
        snapshot = cls.get_snapshot(data['Storage-Node'], data['pool_name']) + 1
        res1 = local.cmd(data['Storage-Node'],
                         'cmd.run',
                         ["zfs snapshot -r %(pool_name)s@%(snapshot)d" % {'pool_name': data['pool_name'],
                                                                          'snapshot': snapshot}])
        send = "zfs send -R -i %(pool_name)s@%(old_snapshot)d %(pool_name)s@%(snapshot)d"
        if snapshot == 0:
            send = "zfs send -R %(pool_name)s@%(snapshot)d"
        recv = "ssh %(remote_ip)s zfs receive -F %(pool_name)s"
        cmd = "%s | %s" % (send % {'pool_name': data['pool_name'],
                                   'old_snapshot': snapshot - 1,
                                   'snapshot': snapshot},
                           recv % {'pool_name': data['pool_name'],
                                   'remote_ip': data['remote_ip']})
        res2 = local.cmd(data['Storage-Node'], 'cmd.run', [cmd])
        cls.set_snapshot(data['Storage-Node'], data['pool_name'], snapshot)
        return [res1, res2]

    @classmethod
    def zfs_replicate_dataset(cls, data):
        client = LocalClient()
        cls._delete_all_snapshots(data['Storage-Node'])
        cls._delete_all_snapshots(data['rep_host_id'])
        rep_host_ip = cls._get_ipaddr(data['rep_host_id'])
        make_snapshot = "zfs snapshot %(pool_name)s/%(dataset)s@current" % {'pool_name': data['pool_name'],
                                                                                   'dataset': data['dataset']}
        res1 = client.cmd(data['Storage-Node'], "cmd.run", [make_snapshot])
        send = "zfs send %(pool_name)s/%(dataset)s@current"
        recv = "ssh %(remote_ip)s zfs receive -F %(pool_name)s/%(dataset)s"
        cmd = "%s | %s" % (send % {'pool_name': data['pool_name'],
                                   'dataset': data['dataset']},
                           recv % {'pool_name': data['pool_name'],
                                   'remote_ip': rep_host_ip,
                                   'dataset': data['dataset']})
        res2 = client.cmd(data['Storage-Node'], "cmd.run", [cmd])
        return [res1, res2]