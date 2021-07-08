# algorithm-container-network
Experimental setup for peer-to-peer network for algorithm containers with port forwarding

![port forwarding diagram](./port-forwarding-diagram.jpg)

## How to run
```bash
docker-compose up -d
```

## Notes
### Additional server configuration
Blocking internet for vpn clients:
```shell
iptables -F FORWARD
iptables -P FORWARD DROP
iptables -A FORWARD -i tun+ -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o tun+ -j ACCEPT
```
Configuring routing in algorithm container namespace from host.

```shell
pid=$(docker container inspect $container_id -f '{{.State.Pid}}')
mkdir -p /var/run/netns/
ln -sfT /proc/$pid/ns/net /var/run/netns/$container_id

ip netns exec $container_id ip a

ip netns exec $container_id ip route replace default via $gateway

```




## Openvpn server requirements
- `blockLan = false`
- `clientToClient = true`

## References
* [How to share networks between docker containers](https://forums.docker.com/t/how-to-set-up-containers-with-vpn-client-installed-each-connecting-to-another-vpn-server/97549)