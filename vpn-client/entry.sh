#!/bin/sh
# Iptables

# Routing


# Nat
iptables -F FORWARD
iptables -P FORWARD DROP
iptables -A FORWARD -i eth1 -o tun0 -j ACCEPT
iptables -A FORWARD -o eth1 -i tun0 -j ACCEPT

iptables -t nat -A POSTROUTING -o tun+ -j MASQUERADE
# Run vpn

echo "Starting vpn client..."

openvpn --config "$VPN_CONFIG" \
    --connect-retry-max 10 \
    --pull-filter ignore "route-ipv6" \
    --pull-filter ignore "ifconfig-ipv6" \
    --script-security 2 \
    --up-restart \
    --cd /data &
openvpn_child=$!

wait $openvpn_child