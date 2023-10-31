from network_operation import calNodePort
import subprocess
import os
import shutil

from exceptions import (
    OperationError,
)


def enroll_org_ca_admin(
    network_config,
    network_folder,
    nodeIp,
    org_index,
    username="admin",
    password="adminpw",
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]

        os.makedirs(
            f"{network_folder}/crypto-config/peerOrganizations/{org_name}.{network_name}.com",
            exist_ok=True,
        )

        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/peerOrganizations/{org_name}.{network_name}.com",
        )

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(
            f"https://{username}:{password}@{nodeIp}:{calNodePort.calPeerCaNodePort(org_index)}"
        )

        cmd.append("--caname")
        cmd.append(f"ca-org-{org_name}")

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orgs/{org_name}/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        print(e)
        raise OperationError(
            f"Fail to Enroll CA Admin for organization of index {org_index}"
        )


def create_org_NodeOUS(
    network_config,
    network_folder,
    org_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]

        string = f"""NodeOUs:
    Enable: true
    ClientOUIdentifier:
        Certificate: cacerts/ca.{org_name}.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: client
    PeerOUIdentifier:
        Certificate: cacerts/ca.{org_name}.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: peer
    AdminOUIdentifier:
        Certificate: cacerts/ca.{org_name}.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: admin
    OrdererOUIdentifier:
        Certificate: cacerts/ca.{org_name}.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: orderer
"""

        dest_folder = f"{network_folder}/crypto-config/peerOrganizations/{org_name}.{network_name}.com/msp"
        os.makedirs(dest_folder, exist_ok=True)

        file_config = open(f"{dest_folder}/config.yaml", "w+")
        file_config.write(string)
        file_config.close()
    except Exception as e:
        raise OperationError(
            f"Fail to Create NodeOUS for organization of index {org_index}"
        )


def register_org_entity(
    network_config, network_folder, org_index, type, name, password
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/peerOrganizations/{org_name}.{network_name}.com",
        )

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("register")

        cmd.append("--caname")
        cmd.append(f"ca-org-{org_name}")

        cmd.append("--id.name")
        cmd.append(name)

        cmd.append("--id.secret")
        cmd.append(password)

        cmd.append("--id.type")
        cmd.append(type)

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orgs/{org_name}/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        raise OperationError(
            f"Fail to Register {type} {name} for organization of index {org_index}"
        )


def gen_peer_msp(
    network_config,
    network_folder,
    nodeIp,
    org_index,
    peer_index,
    hosts,
    username,
    password,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/peerOrganizations/{org_name}.{network_name}.com",
        )

        org_folder = os.path.join(
            network_folder,
            "crypto-config",
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        folder = os.path.join(
            org_folder,
            "peers",
            f"peer{peer_index}.{org_name}.{network_name}.com",
        )

        os.makedirs(folder, exist_ok=True)

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(
            f"https://{username}:{password}@{nodeIp}:{calNodePort.calPeerCaNodePort(org_index)}"
        )

        cmd.append("--caname")
        cmd.append(f"ca-org-{org_name}")

        cmd.append("-M")

        msp_folder = os.path.join(
            folder,
            "msp",
        )
        cmd.append(msp_folder)

        for host in hosts:
            cmd.append("--csr.hosts")
            cmd.append(host)

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orgs/{org_name}/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                f"cp {org_folder}/msp/config.yaml {msp_folder}/config.yaml",
            ],
            shell=True,
            check=True,
        )

        subprocess.run(
            [
                f"mv {msp_folder}/cacerts/* {msp_folder}/cacerts/ca.{org_name}.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"mv {msp_folder}/signcerts/* {msp_folder}/signcerts/peer{peer_index}.{org_name}.{network_name}.com-cert.pem"
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"mv {msp_folder}/keystore/* {msp_folder}/keystore/priv_sk"],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(
            f"Fail to Generate MSP for peer {peer_index} of organization of index {org_index}"
        )


def gen_peer_tls(
    network_config,
    network_folder,
    nodeIp,
    org_index,
    peer_index,
    hosts,
    username,
    password,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]
        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/peerOrganizations/{org_name}.{network_name}.com",
        )

        folder = os.path.join(
            network_folder,
            "crypto-config",
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
            "peers",
            f"peer{peer_index}.{org_name}.{network_name}.com",
        )

        os.makedirs(folder, exist_ok=True)

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(
            f"https://{username}:{password}@{nodeIp}:{calNodePort.calPeerCaNodePort(org_index)}"
        )

        cmd.append("--caname")
        cmd.append(f"ca-org-{org_name}")

        cmd.append("-M")

        tls_folder = os.path.join(
            folder,
            "tls",
        )
        cmd.append(tls_folder)

        cmd.append("--enrollment.profile")
        cmd.append("tls")

        for host in hosts:
            cmd.append("--csr.hosts")
            cmd.append(host)

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orgs/{org_name}/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                f"cp {tls_folder}/tlscacerts/* {tls_folder}/ca.crt",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"cp {tls_folder}/signcerts/* {tls_folder}/server.crt",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"cp {tls_folder}/keystore/* {tls_folder}/server.key"],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(
            f"Fail to Generate TLS for peer {peer_index} of organization of index {org_index}"
        )


def copy_tls_ca_cert_for_org(
    network_config,
    network_folder,
    org_index,
):
    try:
        network_name = network_config["name"]
        org_name = network_config["blockchain_peer_config"]["organizations"][org_index][
            "name"
        ]

        folder = os.path.join(
            network_folder,
            "crypto-config",
            "peerOrganizations",
            f"{org_name}.{network_name}.com",
        )

        os.makedirs(os.path.join(folder, "msp", "tlscacerts"), exist_ok=True)
        os.makedirs(os.path.join(folder, "tlsca"), exist_ok=True)
        os.makedirs(os.path.join(folder, "ca"), exist_ok=True)

        subprocess.run(
            [
                f"cp {folder}/peers/peer0.{org_name}.{network_name}.com/tls/tlscacerts/* {folder}/msp/tlscacerts/ca.crt",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"cp {folder}/peers/peer0.{org_name}.{network_name}.com/tls/tlscacerts/* {folder}/tlsca/tlsca.{org_name}.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"cp {folder}/peers/peer0.{org_name}.{network_name}.com/msp/cacerts/* {folder}/ca/ca.{org_name}.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )

        subprocess.run(
            [
                f"mv {folder}/msp/cacerts/* {folder}/msp/cacerts/ca.{org_name}.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(
            f"Fail to Copy Certificates for organization of index {org_index}"
        )


def gen_user_msp(
    network_config,
    network_folder,
    nodeIp,
    nodePort,
    org_name,
    org_type,
    username,
    password,
):
    try:
        network_name = network_config["name"]

        if org_type == "peer":
            dns_name = f"{org_name}.{network_name}.com"
            caname = f"ca-org-{org_name}"
        else:
            dns_name = f"{network_name}.com"
            caname = f"ca-{org_name}"

        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/{org_type}Organizations/{dns_name}",
        )

        org_folder = os.path.join(
            network_folder,
            "crypto-config",
            f"{org_type}Organizations",
            dns_name,
        )

        folder = os.path.join(
            org_folder, "users", f"{username.capitalize()}@{dns_name}"
        )

        os.makedirs(folder, exist_ok=True)

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(f"https://{username}:{password}@{nodeIp}:{nodePort}")

        cmd.append("--caname")
        cmd.append(caname)

        cmd.append("-M")

        msp_folder = os.path.join(
            folder,
            "msp",
        )
        cmd.append(msp_folder)

        cmd.append("--tls.certfiles")
        if org_type == "peer":
            cmd.append(f"{network_folder}/cas/orgs/{org_name}/tls-cert.pem")
        else:
            cmd.append(f"{network_folder}/cas/{org_name}/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                f"cp {org_folder}/msp/config.yaml {folder}/msp/config.yaml",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"mv {msp_folder}/cacerts/* {msp_folder}/cacerts/ca.{dns_name}-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"mv {msp_folder}/signcerts/* {msp_folder}/signcerts/{username.capitalize()}@{dns_name}-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"mv {msp_folder}/keystore/* {msp_folder}/keystore/priv_sk"],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(
            f"Fail to Generate MSP for {username} of organization {org_name}"
        )


def gen_admin_msp(
    network_config,
    network_folder,
    nodeIp,
    nodePort,
    org_name,
    org_type,
    username,
    password,
):
    try:
        network_name = network_config["name"]
        if org_type == "peer":
            dns_name = f"{org_name}.{network_name}.com"
            caname = f"ca-org-{org_name}"
        else:
            dns_name = f"{network_name}.com"
            caname = f"ca-{org_name}"
        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/{org_type}Organizations/{dns_name}",
        )

        org_folder = os.path.join(
            network_folder,
            "crypto-config",
            f"{org_type}Organizations",
            dns_name,
        )

        folder = os.path.join(org_folder, "users", f"Admin@{dns_name}")

        os.makedirs(folder, exist_ok=True)

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(f"https://{username}:{password}@{nodeIp}:{nodePort}")

        cmd.append("--caname")
        cmd.append(caname)

        cmd.append("-M")

        msp_folder = os.path.join(
            folder,
            "msp",
        )
        cmd.append(msp_folder)

        cmd.append("--tls.certfiles")
        if org_type == "peer":
            cmd.append(f"{network_folder}/cas/orgs/{org_name}/tls-cert.pem")
        else:
            cmd.append(f"{network_folder}/cas/{org_name}/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                f"cp {org_folder}/msp/config.yaml {folder}/msp/config.yaml",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"mv {msp_folder}/cacerts/* {msp_folder}/cacerts/ca.{dns_name}-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"mv {msp_folder}/signcerts/* {msp_folder}/signcerts/Admin@{dns_name}-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"mv {msp_folder}/keystore/* {msp_folder}/keystore/priv_sk"],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(
            f"Fail to Generate MSP for Admin of organization {org_name}"
        )


def enroll_orderer_ca_admin(
    network_config,
    network_folder,
    nodeIp,
    username="admin",
    password="adminpw",
):
    try:
        network_name = network_config["name"]

        os.makedirs(
            f"{network_folder}/crypto-config/ordererOrganizations/{network_name}.com",
            exist_ok=True,
        )

        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/ordererOrganizations/{network_name}.com",
        )

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(
            f"https://{username}:{password}@{nodeIp}:{calNodePort.calOrdererCaNodePort()}"
        )

        cmd.append("--caname")
        cmd.append(f"ca-orderer")

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orderer/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        raise OperationError(f"Fail to Enroll CA Admin for Orderer organization")


def create_orderer_NodeOUS(
    network_config,
    network_folder,
):
    try:
        network_name = network_config["name"]

        string = f"""NodeOUs:
    Enable: true
    ClientOUIdentifier:
        Certificate: cacerts/ca.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: client
    PeerOUIdentifier:
        Certificate: cacerts/ca.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: peer
    AdminOUIdentifier:
        Certificate: cacerts/ca.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: admin
    OrdererOUIdentifier:
        Certificate: cacerts/ca.{network_name}.com-cert.pem
        OrganizationalUnitIdentifier: orderer
"""

        dest_folder = f"{network_folder}/crypto-config/ordererOrganizations/{network_name}.com/msp"
        os.makedirs(dest_folder, exist_ok=True)

        file_config = open(f"{dest_folder}/config.yaml", "w+")
        file_config.write(string)
        file_config.close()
    except Exception as e:
        raise OperationError(f"Fail to Create NodeOUS for Orderer organization")


def register_orderer_entity(network_config, network_folder, type, name, password):
    try:
        network_name = network_config["name"]

        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/ordererOrganizations/{network_name}.com",
        )

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("register")

        cmd.append("--caname")
        cmd.append(f"ca-orderer")

        cmd.append("--id.name")
        cmd.append(name)

        cmd.append("--id.secret")
        cmd.append(password)

        cmd.append("--id.type")
        cmd.append(type)

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orderer/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)
    except Exception as e:
        raise OperationError(f"Fail to Register {type} {name} for Orderer organization")


def gen_orderer_msp(
    network_config,
    network_folder,
    nodeIp,
    hosts,
    username,
    password,
):
    try:
        network_name = network_config["name"]

        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/ordererOrganizations/{network_name}.com",
        )

        org_folder = os.path.join(
            network_folder,
            "crypto-config",
            "ordererOrganizations",
            f"{network_name}.com",
        )

        folder = os.path.join(
            org_folder,
            "orderers",
            f"orderer.{network_name}.com",
        )

        os.makedirs(folder, exist_ok=True)

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(
            f"https://{username}:{password}@{nodeIp}:{calNodePort.calOrdererCaNodePort()}"
        )

        cmd.append("--caname")
        cmd.append(f"ca-orderer")

        cmd.append("-M")

        msp_folder = os.path.join(
            folder,
            "msp",
        )
        cmd.append(msp_folder)

        for host in hosts:
            cmd.append("--csr.hosts")
            cmd.append(host)

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orderer/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                f"cp {org_folder}/msp/config.yaml {msp_folder}/config.yaml",
            ],
            shell=True,
            check=True,
        )

        subprocess.run(
            [
                f"mv {msp_folder}/cacerts/* {msp_folder}/cacerts/ca.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"mv {msp_folder}/signcerts/* {msp_folder}/signcerts/orderer.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"mv {msp_folder}/keystore/* {msp_folder}/keystore/priv_sk"],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(f"Fail to Generate MSP for orderer organization")


def gen_orderer_tls(
    network_config,
    network_folder,
    nodeIp,
    hosts,
    username,
    password,
):
    try:
        network_name = network_config["name"]

        env = dict(
            **os.environ,
            FABRIC_CA_CLIENT_HOME=f"{network_folder}/crypto-config/ordererOrganizations/{network_name}.com",
        )

        folder = os.path.join(
            network_folder,
            "crypto-config",
            "ordererOrganizations",
            f"{network_name}.com",
            "orderers",
            f"orderer.{network_name}.com",
        )

        os.makedirs(folder, exist_ok=True)

        cmd = []

        cmd.append("fabric-ca-client")
        cmd.append("enroll")

        cmd.append("-u")
        cmd.append(
            f"https://{username}:{password}@{nodeIp}:{calNodePort.calOrdererCaNodePort()}"
        )

        cmd.append("--caname")
        cmd.append(f"ca-orderer")

        cmd.append("-M")

        tls_folder = os.path.join(
            folder,
            "tls",
        )
        cmd.append(tls_folder)

        cmd.append("--enrollment.profile")
        cmd.append("tls")

        for host in hosts:
            cmd.append("--csr.hosts")
            cmd.append(host)

        cmd.append("--tls.certfiles")
        cmd.append(f"{network_folder}/cas/orderer/tls-cert.pem")

        subprocess.run(cmd, check=True, env=env)

        subprocess.run(
            [
                f"cp {tls_folder}/tlscacerts/* {tls_folder}/ca.crt",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"cp {tls_folder}/signcerts/* {tls_folder}/server.crt",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"cp {tls_folder}/keystore/* {tls_folder}/server.key"],
            shell=True,
            check=True,
        )

        dest_folder = os.path.join(
            folder,
            "msp",
            "tlscacerts",
        )

        os.makedirs(
            dest_folder,
            exist_ok=True,
        )

        subprocess.run(
            [
                f"cp {tls_folder}/tlscacerts/* {dest_folder}/tlsca.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(f"Fail to Generate TLS for Orderer")


def copy_tls_ca_cert_for_orderer(
    network_config,
    network_folder,
):
    try:
        network_name = network_config["name"]

        folder = os.path.join(
            network_folder,
            "crypto-config",
            "ordererOrganizations",
            f"{network_name}.com",
        )

        os.makedirs(os.path.join(folder, "msp", "tlscacerts"), exist_ok=True)
        os.makedirs(os.path.join(folder, "tlsca"), exist_ok=True)
        os.makedirs(os.path.join(folder, "ca"), exist_ok=True)

        subprocess.run(
            [
                f"cp {folder}/orderers/orderer.{network_name}.com/tls/tlscacerts/* {folder}/msp/tlscacerts/ca.crt",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"cp {folder}/orderers/orderer.{network_name}.com/tls/tlscacerts/* {folder}/tlsca/tlsca.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )
        subprocess.run(
            [
                f"cp {folder}/orderers/orderer.{network_name}.com/msp/cacerts/* {folder}/ca/ca.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )

        subprocess.run(
            [
                f"mv {folder}/msp/cacerts/* {folder}/msp/cacerts/ca.{network_name}.com-cert.pem",
            ],
            shell=True,
            check=True,
        )

    except Exception as e:
        raise OperationError(f"Fail to Copy Certificates for Orderer")


def gen_certificates_by_network_config(network_config, network_folder, nodeIp):
    orgs = network_config["blockchain_peer_config"]["organizations"]

    org_index = 0
    for org in orgs:
        enroll_org_ca_admin(
            network_config=network_config,
            network_folder=network_folder,
            nodeIp=nodeIp,
            org_index=org_index,
        )

        create_org_NodeOUS(
            network_config=network_config,
            network_folder=network_folder,
            org_index=org_index,
        )

        for peer_index in range(org["number_peer"]):
            register_org_entity(
                network_config=network_config,
                network_folder=network_folder,
                org_index=org_index,
                type="peer",
                name=f"peer{peer_index}",
                password=f"peer{peer_index}pw",
            )

        register_org_entity(
            network_config=network_config,
            network_folder=network_folder,
            org_index=org_index,
            type="client",
            name=f"user1",
            password=f"user1pw",
        )

        register_org_entity(
            network_config=network_config,
            network_folder=network_folder,
            org_index=org_index,
            type="admin",
            name=f"{org['name']}admin",
            password=f"{org['name']}adminpw",
        )

        for peer_index in range(org["number_peer"]):
            gen_peer_msp(
                network_config=network_config,
                network_folder=network_folder,
                nodeIp=nodeIp,
                org_index=org_index,
                peer_index=peer_index,
                hosts=[f"peer{peer_index}.{org['name']}.{network_config['name']}.com"],
                username=f"peer{peer_index}",
                password=f"peer{peer_index}pw",
            )
            gen_peer_tls(
                network_config=network_config,
                network_folder=network_folder,
                nodeIp=nodeIp,
                org_index=org_index,
                peer_index=peer_index,
                hosts=[
                    f"peer{peer_index}.{org['name']}.{network_config['name']}.com",
                    nodeIp,
                    "localhost",
                ],
                username=f"peer{peer_index}",
                password=f"peer{peer_index}pw",
            )

        copy_tls_ca_cert_for_org(
            network_config=network_config,
            network_folder=network_folder,
            org_index=org_index,
        )

        gen_user_msp(
            network_config=network_config,
            network_folder=network_folder,
            nodeIp=nodeIp,
            nodePort=calNodePort.calPeerCaNodePort(org_index),
            org_name=org["name"],
            org_type="peer",
            username=f"user1",
            password=f"user1pw",
        )

        gen_admin_msp(
            network_config=network_config,
            network_folder=network_folder,
            nodeIp=nodeIp,
            nodePort=calNodePort.calPeerCaNodePort(org_index),
            org_name=org["name"],
            org_type="peer",
            username=f"{org['name']}admin",
            password=f"{org['name']}adminpw",
        )

        org_index += 1

    enroll_orderer_ca_admin(
        network_config=network_config, network_folder=network_folder, nodeIp=nodeIp
    )

    create_orderer_NodeOUS(network_config=network_config, network_folder=network_folder)

    register_orderer_entity(
        network_config=network_config,
        network_folder=network_folder,
        type="orderer",
        name="orderer",
        password="ordererpw",
    )

    register_orderer_entity(
        network_config=network_config,
        network_folder=network_folder,
        type="admin",
        name="ordererAdmin",
        password="ordererAdminpw",
    )

    gen_orderer_msp(
        network_config=network_config,
        network_folder=network_folder,
        nodeIp=nodeIp,
        hosts=[f"orderer.{network_config['name']}.com", nodeIp, "localhost"],
        username="orderer",
        password="ordererpw",
    )

    gen_orderer_tls(
        network_config=network_config,
        network_folder=network_folder,
        nodeIp=nodeIp,
        hosts=[f"orderer.{network_config['name']}.com", nodeIp, "localhost"],
        username="orderer",
        password="ordererpw",
    )

    copy_tls_ca_cert_for_orderer(
        network_config=network_config, network_folder=network_folder
    )

    gen_admin_msp(
        network_config=network_config,
        network_folder=network_folder,
        nodeIp=nodeIp,
        nodePort=calNodePort.calOrdererCaNodePort(),
        org_name="orderer",
        org_type="orderer",
        username=f"ordererAdmin",
        password=f"ordererAdminpw",
    )


def gen_certificates_for_peer(
    network_config,
    network_folder,
    nodeIp,
    org_index,
    peer_index,
    peer_hosts,
):

    org = network_config["blockchain_peer_config"]["organizations"][org_index]

    enroll_org_ca_admin(
        network_config=network_config,
        network_folder=network_folder,
        nodeIp=nodeIp,
        org_index=org_index,
    )

    register_org_entity(
        network_config=network_config,
        network_folder=network_folder,
        org_index=org_index,
        type="peer",
        name=f"peer{peer_index}",
        password=f"peer{peer_index}pw",
    )

    gen_peer_msp(
        network_config=network_config,
        network_folder=network_folder,
        nodeIp=nodeIp,
        org_index=org_index,
        peer_index=peer_index,
        hosts=peer_hosts,
        username=f"peer{peer_index}",
        password=f"peer{peer_index}pw",
    )

    gen_peer_tls(
        network_config=network_config,
        network_folder=network_folder,
        nodeIp=nodeIp,
        org_index=org_index,
        peer_index=peer_index,
        hosts=peer_hosts,
        username=f"peer{peer_index}",
        password=f"peer{peer_index}pw",
    )
