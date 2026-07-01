# cka-hellomichka

> Homelab Kubernetes cluster — bare metal, kubeadm, Cloudflare Tunnel

[![cluster](https://img.shields.io/badge/cluster-cka--hellomichka-00d4c8)]
https://lab.michka.dev)
[![k8s](https://img.shields.io/badge/kubernetes-v1.34.8-blue)]
[![CNI](https://img.shields.io/badge/CNI-Calico_VXLAN-purple)]
[![tunnel](https://img.shields.io/badge/tunnel-Cloudflare-orange)]

## Vue d'ensemble

Cluster Kubernetes kubeadm auto-hébergé, exposé sur Internet via Cloudflare Tunnel.  
Réseau Calico VXLAN, mesh Tailscale, zéro dépendance cloud pour le plan de contrôle.

## Nodes

| Hostname | Rôle | IP | OS |
|---|---|---|---|
| hellomichka-a8 | control-plane | 192.168.1.52 | Ubuntu 24.04 LTS |
| cka-worker-01 | worker (VM KVM) | 192.168.1.12 | Ubuntu 24.04 LTS |

L'hyperviseur KVM tourne sur `ml-hellomichka` (`192.168.1.11`).

## Structure du repo

```
cka-hellomichka/
├── apps/                   # Workloads Kubernetes
│   └── ingress-lab/        # Namespace ingress-lab
├── cluster/                # Bootstrap cluster (kubeadm, Calico, netplan)
├── docs/                   # Incidents, post-mortems, décisions
└── netplan-backup/         # Backup configs réseau
```

## Liens utiles

- Page cluster live : https://lab.michka.dev
- GitHub : https://github.com/Mickael78000
- Portfolio : https://www.chains-of-vertu.xyz/

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Runbook opérations](docs/RUNBOOK.md)
- [Incidents](docs/INCIDENTS.md)
- [Setup ingress-lab](docs/ingress-lab-setup.md)
