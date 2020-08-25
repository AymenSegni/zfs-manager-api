
from flask_restful import reqparse
from zfs_cluster_deployer.app_exceptions import HTTPExceptions
from zfs_cluster_deployer.application.Views import BaseView
from zfs_cluster_deployer.application.Controllers.zpool_controller import ZpoolController
from zfs_cluster_deployer.application.Controllers.zfs_controller import ZFSController
from zfs_cluster_deployer.application.utils import Utils


class InitialSetup(BaseView):
    def patch(self):
        params = reqparse.RequestParser()
        params.add_argument('Storage-Node', type=str, location="headers", required=True)
        data = params.parse_args()
        return Utils.install_zfs(data)

    def post(self):
        params = reqparse.RequestParser()
        params.add_argument('minion_id', type=str, required=True)
        data = params.parse_args()
        return Utils.accept_minion(data)


class ZpoolClusterManager(BaseView):
    def options(self):
        return self.api_doc['zpool']

    def get(self, path=None, name=None):
        params = reqparse.RequestParser()
        params.add_argument('Storage-Node', location="headers", type=str, required=True)
        storage_node = params.parse_args()['Storage-Node']
        if path:
            if path == "device":
                return ZpoolController.get_devices(storage_node)
            elif path == "iostat":
                if not name:
                    HTTPExceptions.missing_parameter("pool name is missing")
                return ZpoolController.zpool_iostat(storage_node, name)
            elif path == "status":
                if not name:
                    HTTPExceptions.missing_parameter("pool name is missing")
                return ZpoolController.zpool_status(storage_node, name)
            elif path == "all":
                return ZpoolController.zpool_list(storage_node)
        else:
            HTTPExceptions.method_not_allowed()

    def post(self, path=None, name=None):
        params = reqparse.RequestParser()
        params.add_argument('name', type=str, required=True)
        params.add_argument('devices', type=str, action="append", required=True)
        params.add_argument('Storage-Node', location="headers", required=True)
        data = params.parse_args()
        return ZpoolController.zpool_create(data)

    def put(self, path=None, name=None):
        params = reqparse.RequestParser()
        params.add_argument('name', type=str, required=True)
        params.add_argument('devices', type=str, action="append", required=True)
        params.add_argument('Storage-Node', location="headers", required=True)
        data = params.parse_args()
        return ZpoolController.zpool_add(data)

    def delete(self, path=None, name=None):
        if path:
            params = reqparse.RequestParser()
            params.add_argument('Storage-Node', location="headers", type=str, required=True)
            storage_node = params.parse_args()['Storage-Node']
            if path == "one":
                if name:
                    return ZpoolController.zpool_destroy(storage_node, name)
                else:
                    return HTTPExceptions.method_not_allowed("Mass delete is not supported, please specify a pool name")
            else:
                HTTPExceptions.not_found()
        else:
            HTTPExceptions.method_not_allowed()


class ZFSManager(BaseView):
    def options(self):
        return self.api_doc['zfs']

    def get(self, path=None, name=None):
        params = reqparse.RequestParser()
        params.add_argument('Storage-Node', location="headers", type=str, required=True)
        storage_node = params.parse_args()['Storage-Node']
        if path:
            if path == "one":
                if not name:
                    HTTPExceptions.missing_parameter("pool name is missing")
                else:
                    return ZFSController.zfs_list(storage_node, name)
            elif path == "all":
                return ZFSController.zfs_list(storage_node)
        else:
            HTTPExceptions.not_found()

    def post(self, path=None, name=None):
        params = reqparse.RequestParser()
        params.add_argument('Storage-Node', location="headers", type=str, required=True)
        params.add_argument('name', type=str, required=True)
        params.add_argument('pool_name', type=str, required=True)
        params.add_argument('quota', type=str, required=True)
        data = params.parse_args()
        return ZFSController.zfs_create(data)

    def put(self):
        pass

    def delete(self, path=None, name=None):
        params = reqparse.RequestParser()
        params.add_argument('Storage-Node', location="headers", type=str, required=True)
        params.add_argument('name', type=str, required=True)
        params.add_argument('pool_name', type=str, required=True)
        data = params.parse_args()
        return ZFSController.zfs_destroy(data)


class ZFSReplicate(BaseView):
    def options(self):
        return self.api_doc['replicate']

    def put(self, name):
        params = reqparse.RequestParser()
        params.add_argument('Storage-Node', location="headers", type=str, required=True)
        params.add_argument('pool_name', type=str, required=True)
        params.add_argument('rep_host_id', type=str, required=True)
        if name == "zpool":
            data = params.parse_args()
            return ZFSController.zfs_replicate_pool(data)
        elif name == "dataset":
            params.add_argument('dataset', type=str, required=True)
            data = params.parse_args()
            return ZFSController.zfs_replicate_dataset(data)