"""
Author: Aymen Segni
Date: 12/11/17
"""
import sys
from zfs_cluster_deployer.server import main

try:
    port = sys.argv[1]
except IndexError:
    port = 8888

if __name__ == "__main__":
    main(port)
