def calPeerNodePort(org_index, peer_index):
    return 30000 + (org_index + 1)*100 + (peer_index + 1)

def calPeerCaNodePort(org_index):
    return 30000 + (org_index + 1)*100

def calOrdererNodePort():
    return 30000 + 7

def calOrdererCaNodePort():
    return 30000 + 4

def calExplorerPort():
    return 30000 + 8
