"""
  Author:  BK Blockchain
  Project: ipfs_service
  Created: 09/22/19 10:13
  Purpose: ALL CONFIG VARIABLES FOR IPFS SERVICE PROJECT
"""

import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    DATABASE_DIR = "{}/{}".format(basedir, "db")
    HOST = "127.0.0.1"
    PORT = 9000


class IpfsConfig(Config):
    IPFS_PORT = "/ip4/127.0.0.1/tcp/5001/http"

