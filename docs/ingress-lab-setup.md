# Setup ingress-lab — nginx avec ConfigMap et Cloudflare Tunnel

**Date** : 2026-07-01  
**Namespace** : `ingress-lab`  
**URL** : https://lab.michka.dev

---

## Objectif

Déployer une page web statique servie par nginx (3 replicas), dont le contenu
est géré via un ConfigMap Kubernetes, exposé via Cloudflare Tunnel.

---

## Composants

| Fichier | Type K8s | Rôle |
|---|---|---|
| `nginx-app.yaml` | Deployment | 3 replicas nginx:1.27 avec probes et volumeMount |
| `nginx-app-svc.yaml` | Service | NodePort 30081 |
| `nginx-app-html-configmap.yaml` | ConfigMap | Contient `index.html` |
| `cluster-web-page.html` | — | Source HTML originale |
| `generate_cluster_page.py` | — | Génère l'HTML depuis kubectl |
| `update-cluster-page.sh` | — | Met à jour ConfigMap + rollout |

---

## Déploiement initial

```bash
# 1. Créer le namespace
kubectl create namespace ingress-lab

# 2. Générer le ConfigMap depuis le fichier HTML
kubectl -n ingress-lab create configmap nginx-app-html \
  --from-file=index.html=cluster-web-page.html \
  --dry-run=client -o yaml > nginx-app-html-configmap.yaml

# 3. Appliquer tous les manifestes
kubectl apply -f apps/ingress-lab/

# 4. Vérifier
kubectl get pods -n ingress-lab
kubectl get endpoints -n ingress-lab nginx-app-svc
```

---

## Architecture de montage

```
ConfigMap nginx-app-html
  └─▶ volume html
        └─▶ volumeMount subPath: index.html
              └─▶ /usr/share/nginx/html/index.html
                    └─▶ nginx sert la page sur :80
                          └─▶ readinessProbe / livenessProbe httpGet /
```

---

## Mettre à jour la page

```bash
python3 generate_cluster_page.py
./update-cluster-page.sh
```

> ⚠️ Le fichier `cluster-web-page.generated.html` est dans `.gitignore`.
> Seul `cluster-web-page.html` (source) est versionné.

---

## Workaround Cloudflare Tunnel

Le tunnel pointe sur `192.168.1.52:30081` (control-plane) au lieu de
`192.168.1.12:30081` (worker) en raison d'un problème de bridge `br0`
sur l'hyperviseur. Voir [INCIDENTS.md](INCIDENTS.md).
