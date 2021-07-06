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
iptables -P FORWARD DROP
iptables -A FORWARD -i tun+ -o tun+ -j ACCEPT
```
## Openvpn server requirements
- `blockLan = false`
- `clientToClient = true`

## References
* [How to share networks between docker containers](https://forums.docker.com/t/how-to-set-up-containers-with-vpn-client-installed-each-connecting-to-another-vpn-server/97549)