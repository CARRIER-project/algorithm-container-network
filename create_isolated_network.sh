#!/usr/bin/env sh


  isolated:
    internal: True
    ipam:
      config:
        - subnet: "172.16.238.0/24"
        - gateway: openvpn-client