# algorithm-container-network
Experimental setup for peer-to-peer network for algorithm containers with port forwarding

![port forwarding diagram](./port-forwarding-diagram.jpg)

## How to run
```bash
docker-compose up -d
```

## Notes
### Additional configuration
#### Blocking internet on vpn client container
Blocking internet for vpn clients (this will run automatically on vpn client):
```shell
iptables -F FORWARD
iptables -P FORWARD DROP
iptables -A FORWARD -i tun+ -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o tun+ -j ACCEPT
```

#### Default namespace configuration
The bridge networks of the docker containers are linked to network interfaces in the default 
network namespace of the host (but by a different name). 



On docker host, configure exception to docker bridge network isolation:
```shell
iptables -I DOCKER-USER 1 -d $vpn_subnet -i $isolated_bridge -j ACCEPT
iptables -I DOCKER-USER 1 -s $vpn_subnet -o $isolated_bridge -j ACCEPT
```


```shell
docker run --network $isolated_network --cap-add=NET_ADMIN alpine \
          ip netns exec $container_id ip route replace default via $gateway
```

Forward traffic from vpn client to algorithm container. Configure on vpn client per algorithm:
TODO: make rule as specific as possible
```shell
iptables -t nat -A PREROUTING -i tun0 -p tcp \
  --dport $vpn_client_port -j DNAT --to $isolated_algorithm_ip:$algorithm_port
```

## Openvpn server requirements
- `blockLan = false`
- `clientToClient = true`

## References
* [How to share networks between docker containers](https://forums.docker.com/t/how-to-set-up-containers-with-vpn-client-installed-each-connecting-to-another-vpn-server/97549)
* [Container namespaces: deep dive into container networking](https://platform9.com/blog/container-namespaces-deep-dive-container-networking/)