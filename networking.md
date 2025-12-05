Inital peer discovery:
  - Central Server with endpoints (implementation of headscale)
  - peer registers on startup and polls for updates
  - "registry tunnel"  a WireGuard interface on a public server
     that can see NATed peers' external ip:port via wg show dump
  - On topology change, server notifies all peers    

VPN-Connection
  - encryption via Wireguard
  - client receives peer list from coordination server
  - Applies changes via wg set wg0 peer <pubkey>
    allowed-ips <ips> endpoint <ip:port>
  - PersistentKeepalive=25 keeps NAT mappings alive for inbound connections

DNS-Layer
  - Same client writes peer hostnames to a hosts file: 10.0.0.2 alice-laptop.wg
  - CoreDNS serves this file with reload 5s for automatic updates
  - ystemd-resolved routes *.wg queries to CoreDNS via resolvectl domain wg0 ~wg

Simplest starting point: Use Headscale as your coordination server (it's battle-tested),
 write a lightweight agent that syncs its peer list to CoreDNS hosts format,
 and wire up resolved for split DNS. You get 90% of MagicDNS functionality without
 implementing the coordination protocol yourself.
