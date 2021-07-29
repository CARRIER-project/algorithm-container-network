import clize
import docker
from docker.errors import NotFound
from docker.models.networks import Network

_client = None


def get_client():
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


def get_subnet(network: Network):
    return network.attrs['IPAM']['Config'][0]['Subnet']


def network_exists(name):
    try:
        get_client().networks.get(name)
    except NotFound:
        return False
    return True


if __name__ == '__main__':
    clize.run(configure_network)
