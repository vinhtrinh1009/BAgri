import cmd
import subprocess
import time

from exceptions import (
    OperationError,
)

DEFAULT_TIMEOUT = 500


def apply(file_path, kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("apply")

        cmd.append("-f")

        cmd.append(file_path)

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise OperationError(f"Fail to apply {file_path}")


def delete(file_path, kube_config_path=None):
    cmd = []

    cmd.append("kubectl")

    if kube_config_path:
        cmd.append(f"--kubeconfig={kube_config_path}")

    cmd.append("delete")

    cmd.append("-f")

    cmd.append(file_path)

    result = subprocess.run(cmd)

def delete_namespace(file_path, kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("delete")

        cmd.append("-f")

        cmd.append(file_path)

        cmd.append("--namespace=default")

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise OperationError(f"Fail to delete {file_path}")

def delete_secret(secret_name, kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("delete")
        cmd.append("secret")

        cmd.append(secret_name)

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise OperationError(f"Fail to delete secret {secret_name}")

def get_deployment(deployment_name, kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")
        cmd.append("get")
        cmd.append("deployments")

        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        check = result.stdout.decode("utf-8")
        x = check.find(deployment_name)
        return x
    except Exception as e:
        raise OperationError(f"Fail to get deployment {deployment_name}")

def get_secret(secret_name, kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")
        cmd.append("get")
        cmd.append("secrets")

        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        check = result.stdout.decode("utf-8")
        x = check.find(secret_name)
        return x
    except Exception as e:
        raise OperationError(f"Fail to get deployment {secret_name}")

def rollout(name, type="deployment", kube_config_path=None, timeout=500):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("rollout")

        cmd.append("status")

        cmd.append(type)

        cmd.append(name)

        result = subprocess.run(cmd, check=True, timeout=timeout)

    except Exception as e:
        raise OperationError(f"Fail to rollout {name} after {timeout} seconds")


def multiple_rollout(names, type="deployment", kube_config_path=None, timeout=300):
    for name in names:
        rollout(
            name=name, type=type, kube_config_path=kube_config_path, timeout=timeout
        )

def create_nginx_ingress(kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("apply")

        cmd.append("-f")

        cmd.append(
            "https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/do/deploy.yaml"
        )

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise OperationError(f"Fail to create Nginx Ingress")

def get_ingress_ip(ingress_name, kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("get")

        cmd.append("ingress")

        cmd.append(ingress_name)

        cmd.append("-o")

        cmd.append('jsonpath=\'{.status.loadBalancer.ingress[0].ip}\'')

        ingress_ip = ""

        time_start = time.time()

        while time.time() - time_start <= DEFAULT_TIMEOUT:

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )

            if result.returncode == 0:
                ingress_ip = result.stdout.decode('utf-8')

                if ingress_ip[0] == '\'':
                    return_ip = ingress_ip[1:-1]
                    if return_ip:
                        return return_ip
            
            time.sleep(5)

        raise OperationError(f"Fail to get Ingress Ip")

    except Exception as e:
        raise OperationError(f"Fail to get Ingress Ip")

