"""Container detection utilities"""
from os import path


def is_running_in_container():
    """
    Check if the application is running in a container (Docker/Kubernetes)
    
    Returns:
        bool: True if running in container, False otherwise
    """
    return (
        path.exists("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
        or path.exists("/.dockerenv")
        or (
            path.isfile("/proc/self/cgroup")
            and (
                any("kubepods" in line for line in open("/proc/self/cgroup"))
                or any("docker" in line for line in open("/proc/self/cgroup"))
            )
        )
    )

