from typing import List, Union, Dict

import clize
import docker
from docker.errors import NotFound
from docker.models.networks import Network
import json

_client = None

_DEFAULT_BASE_IMAGE = 'algorithm-base'
_HOST = 'host'


def get_client() -> docker.client.DockerClient:
    global _client

    if not _client:
        _client = docker.from_env()
    return _client


def create_network(name):
    client = get_client()

    if network_exists(name):
        raise Exception('Network already exists!')

    network = client.networks.create(name, internal=True)
    subnet = network.attrs['IPAM']['Config'][0]['Subnet']

    return subnet


def find_isolated_bridge(container_id: str):
    # Get network config from isolated container namespace
    container = get_client().containers.get(container_id=container_id)
    _, isolated_interface = container.exec_run(['ip', '--json', 'addr', 'show', 'dev', 'eth0'])

    isolated_interface = json.loads(isolated_interface)

    if_config = _flatten_if_config(isolated_interface)
    link_index = _get_link_index(if_config)

    # Get network config from host namespace
    host_interfaces = get_client().containers.run(_DEFAULT_BASE_IMAGE,
                                                  network=_HOST,
                                                  command=['ip', '--json', 'addr'])

    host_interfaces = json.loads(host_interfaces)

    linked_interface = _get_if(host_interfaces, link_index)

    bridge_interface = linked_interface['master']

    return bridge_interface


def _get_if(interfaces, index) -> Union[Dict, None]:
    """
    Get interface configuration based on interface index

    :param index:
    :return:
    """

    for interface in interfaces:
        if int(interface['ifindex']) == index:
            return interface

    return None


def _get_link_index(if_json: Union[Dict, List]) -> int:
    return int(if_json['link_index'])


def configure_host_namespace(vpn_subnet: str, isolated_bridge: str):
    command = f'iptables -I DOCKER-USER 1 -d {vpn_subnet} -i {isolated_bridge} -j ACCEPT &&'
    f'iptables -I DOCKER-USER 1 -s $vpn_subnet -o $isolated_bridge -j ACCEPT'

    get_client().containers.run(_DEFAULT_BASE_IMAGE,
                                network='host',
                                cap_add='NET_ADMIN',
                                command=command)


def get_subnet(network: Network):
    return network.attrs['IPAM']['Config'][0]['Subnet']


def network_exists(name):
    try:
        get_client().networks.get(name)
    except NotFound:
        return False
    return True


if __name__ == '__main__':
    clize.run(create_network)
