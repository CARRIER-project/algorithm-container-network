#!/bin/sh
# Iptables

# Routing


# Nat


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