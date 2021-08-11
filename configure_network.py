from typing import List, Union, Dict

import docker
from docker.errors import NotFound
from docker.models.networks import Network
import json

_client = None

# FIXME: This image can only be found if the dockerfile in the folder `network-config/` has been
#  built with the  appropriate tag.
_NETWORK_CONFIG_IMAGE = 'network-config'
_HOST = 'host'


def _get_client() -> docker.client.DockerClient:
    global _client

    if not _client:
        _client = docker.from_env()
    return _client


def create_network(name):
    client = _get_client()

    if network_exists(name):
        raise Exception('Network already exists!')

    network = client.networks.create(name, internal=True)
    subnet = network.attrs['IPAM']['Config'][0]['Subnet']

    return subnet


def find_isolated_bridge(container_id: str):
    """
    Retrieve the linked network interface in the host namespace for network interface eth0 in the
    container namespace.

    :param container_id: container id of the docker container connected to an isolated network.
    :return: the name of the network interface in the host namespace
    """
    # Get network config from isolated container namespace
    container = _get_client().containers.get(container_id=container_id)
    _, isolated_interface = container.exec_run(['ip', '--json', 'addr', 'show', 'dev', 'eth0'])

    isolated_interface = json.loads(isolated_interface)

    link_index = _get_link_index(isolated_interface)

    # Get network config from host namespace
    host_interfaces = _get_client().containers.run(_NETWORK_CONFIG_IMAGE,
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
    if isinstance(if_json, list):
        if_json = if_json[-1]
    return int(if_json['link_index'])


def configure_host_namespace(vpn_subnet: str, isolated_bridge: str):
    """
    By default the internal bridge networks are configured to prohibit packet forwarding between
    networks. Create an exception to this rule for forwarding traffic between the bridge and vpn
    network.

    :param vpn_subnet:
    :param isolated_bridge:
    :return:
    """
    command = f'sh -c "iptables -I DOCKER-USER 1 -d {vpn_subnet} -i {isolated_bridge} -j ACCEPT ' \
              f'; iptables -I DOCKER-USER 1 -s {vpn_subnet} -o {isolated_bridge} -j ACCEPT "'

    _get_client().containers.run(_NETWORK_CONFIG_IMAGE,
                                 network='host',
                                 cap_add='NET_ADMIN',
                                 command=command)


def get_subnet(network: Network):
    return network.attrs['IPAM']['Config'][0]['Subnet']


def network_exists(name):
    try:
        _get_client().networks.get(name)
    except NotFound:
        return False
    return True
