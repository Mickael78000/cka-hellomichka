# Journal des incidents — cka-hellomichka

Index des incidents et post-mortems du cluster.

---

## Incidents documentés

| Date | Fichier | Résumé |
|---|---|---|
| 2026-05-29 | [cka-net-incident-worker-20260529-1140.md](cka-net-incident-worker-20260529-1140.md) | Incident réseau worker — bridge br0 hyperviseur |
| 2026-05-29 | [cka-genese-worker-20260529-1221.md](cka-genese-worker-20260529-1221.md) | Genèse et bootstrap du worker node |

---

## Incidents résolus en session (non documentés)

| Date | Résumé | Résolution |
|---|---|---|
| 2026-07-01 | Service `web` introuvable, endpoints manquants | Recréation du Service `nginx-app-svc` avec le bon selector |
| 2026-07-01 | Cloudflare tunnel `Unable to reach origin service` | Config `service:` pointait sur `30080` au lieu de `30081`, URL Markdown invalide dans `config.yml` |
| 2026-07-01 | ConfigMap YAML invalide (`could not find expected ':'`) | Indentation HTML incorrecte, recréé via `--from-file` |

---

## Format post-mortem recommandé

```markdown
# [DATE] — Titre de l'incident

## Résumé
## Timeline
## Cause racine
## Résolution
## Actions préventives
```
