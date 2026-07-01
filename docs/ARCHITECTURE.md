# Architecture du cluster cka-hellomichka

## Topologie réseau

```
Internet
  └─▶ Cloudflare anycast (TLS · WAF · QUIC)
        └─▶ cloudflared (ml-hellomichka · 192.168.1.11)
              └─▶ kube-proxy NodePort (hellomichka-a8 · 192.168.1.52:30081)
                    └─▶ Pod nginx (ingress-lab · cka-worker-01)
```

> **Note workaround** : le trafic transite par le control-plane (`192.168.1.52`) en raison
> d'un problème de bridge `br0` sur l'hyperviseur. La cible finale est `192.168.1.12:30081`
> (worker direct). Dérogation documentée, workaround temporaire.

## Nodes

| Hostname | Rôle | IP LAN | IP Tailscale | Type |
|---|---|---|---|---|
| hellomichka-a8 | control-plane | 192.168.1.52 | 100.121.186.6 | bare metal |
| cka-worker-01 | worker | 192.168.1.12 | — | VM KVM |
| ml-hellomichka | hyperviseur | 192.168.1.11 | 100.117.114.43 | bare metal |

## Stack technique

| Composant | Technologie | Version | Statut |
|---|---|---|---|
| Orchestration | Kubernetes (kubeadm) | v1.34.8 | ✅ actif |
| CNI / réseau pods | Calico VXLAN | v3.29 | ✅ actif |
| Virtualisation | KVM / libvirt | — | ✅ actif |
| Tunnel Internet | Cloudflare Tunnel (cloudflared) | 2026.6.0 | ✅ actif |
| Mesh VPN | Tailscale | — | ✅ actif |
| Exposition | NodePort 30081 | — | ⚠️ workaround |
| Ingress controller | ingress-nginx | — | 🔜 à déployer |
| OS | Ubuntu 24.04 LTS | Noble | ✅ actif |

## Namespaces actifs

| Namespace | Contenu |
|---|---|
| `ingress-lab` | nginx-app Deployment (3 replicas), Service NodePort, ConfigMap HTML |
| `kube-system` | API server, etcd, scheduler, Calico, kube-proxy |

## Accès

- **SSH direct LAN** : `ssh root@192.168.1.52`
- **SSH via Tailscale** : `ssh root@100.121.186.6`
- **kubectl** : configuré sur `hellomichka-a8` et `ml-hellomichka`
- **Page cluster** : https://lab.michka.dev
