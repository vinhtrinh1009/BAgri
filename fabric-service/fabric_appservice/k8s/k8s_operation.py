import subprocess, time

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
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("delete")

        cmd.append("-f")

        cmd.append(file_path)

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        # raise OperationError(f"Fail to delete {file_path}")
        None


def rollout(name, type="deployment", kube_config_path=None, timeout=DEFAULT_TIMEOUT):
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


def apply_with_rollout(
    file_path, name, type="deployment", kube_config_path=None, timeout=DEFAULT_TIMEOUT
):
    apply(file_path=file_path, kube_config_path=kube_config_path)
    rollout(name=name, type=type, kube_config_path=kube_config_path, timeout=timeout)


def multiple_apply_with_rollout(
    file_paths, names, type="deployment", kube_config_path=None, timeout=DEFAULT_TIMEOUT
):
    for file_path in file_paths:
        apply(file_path=file_path, kube_config_path=kube_config_path)

    for name in names:
        rollout(
            name=name, type=type, kube_config_path=kube_config_path, timeout=timeout
        )


def delete_all(kube_config_path=None):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("delete")

        cmd.append("all")

        cmd.append("--all")

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise OperationError(f"Fail to delete all")


def create_docker_registry_secret(
    username,
    password,
    secret_name,
    server="https://registry.gitlab.com",
    kube_config_path=None,
):
    try:
        cmd = []

        cmd.append("kubectl")

        if kube_config_path:
            cmd.append(f"--kubeconfig={kube_config_path}")

        cmd.append("create")

        cmd.append("secret")

        cmd.append("docker-registry")

        cmd.append(secret_name)

        cmd.append(f"--docker-server={server}")

        cmd.append(f"--docker-username={username}")

        cmd.append(f"--docker-password={password}")

        result = subprocess.run(cmd, check=True)

    except Exception as e:
        raise OperationError(f"Fail to create Docker Registry Secret")


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
