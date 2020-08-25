
import subprocess
import time
from salt.client import LocalClient
from zfs_cluster_deployer import CONFIGS
from zfs_cluster_deployer.app_exceptions import HTTPExceptions
from zfs_cluster_deployer import logger


class Utils(object):

    @classmethod
    def install_zfs(cls, data):
        client = LocalClient()
        subprocess.call(["mkdir",
                         "-p",
                         "/srv/salt"])
        subprocess.call(["mv",
                         "%(app_root)s/application/utils/install_zfs.sh" % {'app_root': CONFIGS['APP_ROOT']},
                         "/srv/salt/"])
        response = client.cmd(data['Storage-Node'],
                              "cmd.script",
                              ["salt://install_zfs.sh"])
        return response

    @classmethod
    def accept_minion(cls, data):
        minion_id = data['minion_id']
        flag = False
        time_out = time.time() + 60
        while not flag:
            minion_ids = cls.__get_unaccepted_keys()
            if minion_id in minion_ids:
                break
            if time.time() > time_out:
                HTTPExceptions.time_out_error("timed out checking for minion id")
        try:
            subprocess.call(['salt-key', '-a', '%s' % minion_id, '-y'])
            return {'minion_id': minion_id, 'status': "Accepted"}
        except Exception as e:
            HTTPExceptions.internal_server_error(message=e.message)

    @classmethod
    def __get_unaccepted_keys(cls):
        output = subprocess.check_output(['salt-key'])
        lines = output.split('\n')
        flag = False
        unaccepted_keys = []
        for line in lines:
            if line == "Rejected Keys:":
                break
            if flag:
                unaccepted_keys.append(line)
            if line == "Unaccepted Keys:":
                flag = True
        return unaccepted_keys