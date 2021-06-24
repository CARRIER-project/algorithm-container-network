# algorithm-container-network
Experimental setup for peer-to-peer network for algorithm containers with port forwarding

![port forwarding diagram](./port-forwarding-diagram.jpg)

## How to run
```bash
docker-compose up -d
```

## Notes
In order to enable the vpn client to access the vpn server you have to do a hack in the 
openvpn-client container.
```shell
docker-compose exec openvpn-client

echo VPN_SERVER_HOST VPN_SERVER_IP >> /etc/hosts
```

## References
* [How to share networks between docker containers](https://forums.docker.com/t/how-to-set-up-containers-with-vpn-client-installed-each-connecting-to-another-vpn-server/97549)