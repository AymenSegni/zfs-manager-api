from zfs_cluster_deployer import api
from zfs_cluster_deployer.application.Views.resources import InitialSetup, ZpoolClusterManager, ZFSManager, ZFSReplicate

api.add_resource(InitialSetup, "/")

api.add_resource(ZpoolClusterManager,
                 "/cluster/zpool",
                 "/cluster/zpool/<path:path>",
                 "/cluster/zpool/<path:path>/<name>")

api.add_resource(ZFSManager,
                 "/cluster/zfs",
                 "/cluster/zfs/<path:path>",
                 "/cluster/zfs/<path:path>/<name>")

api.add_resource(ZFSReplicate,
                 "/replicate",
                 "/replicate/<name>")