
from flask_restful import Resource


class BaseView(Resource):
    api_doc = {'zpool': {'get all pools': {'Method': "GET",
                                           'uri': "/cluster/zpool/all",
                                           'headers': {'Storage-Node': "name of the stotage node"}},
                         'get pool io': {'Method': "GET",
                                         'uri': "/cluster/zpool/iostat/<name>",
                                         'headers': {'Storage-Node': "name of the stotage node"}},
                         'get devices': {'Method': "GET",
                                         'uri': "/cluster/zpool/device",
                                         'headers': {'Storage-Node': "name of the stotage node"}},
                         'get pool status': {'Method': "GET",
                                             'uri': "/cluster/zpool/status/<name>",
                                             'headers': {'Storage-Node': "name of the stotage node"}},
                         'create new pool': {'Method': "POST",
                                             'uri': "/cluster/zpool",
                                             'params': {'name': "pool name",
                                                        'devices': ["list", "of", "devices"]},
                                             'headers': {'Storage-Node': "name of the stotage node"}},
                         'add device to pool': {'Method': "PUT",
                                                'uri': "/cluster/zpool",
                                                'params': {'name': "pool name",
                                                           'devices': ["list", "of", "devices"]},
                                                'headers': {'Storage-Node': "name of the stotage node"}},
                         'destroy pool': {'Method': "DELETE",
                                          'uri': "/cluster/zpool/one/<name>",
                                          'headers': {'Storage-Node': "name of the stotage node"}}},
               'zfs': {'get all datasets': {'Method': "GET",
                                            'uri': "/cluster/zfs/all",
                                            'headers': {'Storage-Node': "name of the stotage node"}},
                       'get one dataset': {'Method': "GET",
                                           'uri': "/cluster/zfs/one/<name>",
                                           'headers': {'Storage-Node': "name of the stotage node"}},
                       'create new dataset': {'Method': "POST",
                                              'uri': "/cluster/zfs",
                                              'params': {'name': "name of the dataset",
                                                         'pool_name': "name of the zfs pool",
                                                         'quota': "size of the dataset"},
                                              'headers': {'Storage-Node': "name of the stotage node"}},
                       'destroy dataset': {'Method': "DELETE",
                                           'uri': "/cluster/zfs",
                                           'params': {'name': "path/to/dataset",
                                                      'pool_name': "name of the pool"},
                                           'headers': {'Storage-Node': "name of the stotage node"}}},
               'replicate': {'replicate pool': {'Method': "PUT",
                                                'uri': "/replicate/zpool",
                                                'params': {'pool_name': "name of the pool",
                                                           'remote_ip': "secondary storage node"},
                                                'headers': {'Storage-Node': "name of the primary storage node"}},
                             'replicate dataset': {'Method': "PUT",
                                                   'uri': "/replicate/dataset",
                                                   'params': {'pool_name': "name of the pool",
                                                              'rep_host_id': "secondary storage node minion id",
                                                              'dataset': "dataset to replicate"},
                                                   'headers': {'Storage-Node': "name of the primary storage node"}}},
               'setup': {'initial zfs setup': {'Method': "PATCH",
                                               'uri': "/",
                                               'headers': {'Storage-Node': "name of the primary storage node"}},
                         'accept minion_id': {'Method': "POST",
                                              'uri': "/",
                                              'params': {'minion_id': "The minion id"}}}}

    def options(self):
        return self.api_doc