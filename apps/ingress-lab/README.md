# ingress-lab

Namespace Kubernetes contenant le Deployment nginx qui sert https://lab.michka.dev.

## Contenu

| Fichier | Description |
|---|---|
| `nginx-app.yaml` | Deployment 3 replicas nginx:1.27, probes HTTP sur `/`, volumeMount ConfigMap |
| `nginx-app-svc.yaml` | Service NodePort 30081 |
| `nginx-app-html-configmap.yaml` | ConfigMap contenant `index.html` |
| `cluster-web-page.html` | Source HTML de la page (à éditer) |
| `generate_cluster_page.py` | Génère un HTML à jour depuis `kubectl get nodes/pods` |
| `update-cluster-page.sh` | Script tout-en-un : génère, applique ConfigMap, restart Deployment |

## Déployer

```bash
kubectl apply -f apps/ingress-lab/
```

## Mettre à jour la page

```bash
./update-cluster-page.sh
```

## Vérifier

```bash
kubectl get pods -n ingress-lab
kubectl get endpoints -n ingress-lab nginx-app-svc
curl -si https://lab.michka.dev | head -3
```
