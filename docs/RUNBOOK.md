# Runbook — cka-hellomichka

Procédures opérationnelles courantes du cluster.

---

## Vérifier l'état du cluster

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get svc -n ingress-lab
kubectl get endpoints -n ingress-lab nginx-app-svc
```

---

## Mettre à jour la page web du cluster

La page https://lab.michka.dev est servie par un Deployment nginx dont le contenu
est monté depuis un ConfigMap.

```bash
cd ~
python3 generate_cluster_page.py

kubectl -n ingress-lab create configmap nginx-app-html \
  --from-file=index.html=cluster-web-page.generated.html \
  --dry-run=client -o yaml > nginx-app-html-configmap.yaml

kubectl apply -f nginx-app-html-configmap.yaml
kubectl rollout restart deployment/nginx-app -n ingress-lab
kubectl rollout status deployment/nginx-app -n ingress-lab
```

Ou en une commande avec le script :

```bash
./update-cluster-page.sh
```

---

## Vérifier le tunnel Cloudflare

```bash
# Sur ml-hellomichka (192.168.1.11)
systemctl status cloudflared
journalctl -u cloudflared -f

# Tester le backend
curl -si http://192.168.1.52:30081 | head -5

# Tester via le tunnel
curl -si https://lab.michka.dev | head -5
```

Config tunnel : `/etc/cloudflared/config.yml`

---

## Redémarrer le tunnel Cloudflare

```bash
# Sur ml-hellomichka
systemctl restart cloudflared
journalctl -u cloudflared -n 30
```

---

## Déployer / redéployer ingress-lab

```bash
kubectl apply -f apps/ingress-lab/
kubectl rollout status deployment/nginx-app -n ingress-lab
```

---

## Redémarrer un déploiement

```bash
kubectl rollout restart deployment/nginx-app -n ingress-lab
kubectl rollout status deployment/nginx-app -n ingress-lab
```

---

## Vérifier les probes

```bash
kubectl describe pod -n ingress-lab -l app=nginx-app | grep -A 10 'Liveness\|Readiness'
```

---

## Accéder à un pod nginx

```bash
kubectl exec -it -n ingress-lab deploy/nginx-app -- bash
# Vérifier le fichier monté
cat /usr/share/nginx/html/index.html | head -5
```

---

## Reconstruire le cluster from scratch

Voir [`cluster/kubeadm-init.yaml`](../cluster/kubeadm-init.yaml) et la documentation
[`docs/cka-genese-worker-20260529-1221.md`](cka-genese-worker-20260529-1221.md).
