iptables -F FORWARD
iptables -P FORWARD DROP
iptables -A FORWARD -i tun+ -o tun+ -j ACCEPT
