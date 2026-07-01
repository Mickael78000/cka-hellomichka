#!/usr/bin/env python3
import subprocess
import re
from pathlib import Path
from html import escape

OUT = Path("cluster-web-page.generated.html")

def sh(cmd):
    return subprocess.check_output(cmd, text=True)

def parse_table(cmd):
    out = sh(cmd)
    return [l for l in out.splitlines() if l.strip()]

def nodes():
    lines = parse_table(["kubectl", "get", "nodes", "-o", "wide"])
    rows = []
    for line in lines[1:]:
        cols = re.split(r"\s{2,}", line.strip())
        if len(cols) >= 6:
            rows.append(tuple(cols[:6]))
    return rows

def pods():
    lines = parse_table(["kubectl", "get", "pods", "-n", "ingress-lab"])
    rows = []
    for line in lines[1:]:
        cols = re.split(r"\s{2,}", line.strip())
        if len(cols) >= 5:
            rows.append(tuple(cols[:5]))
    return rows

node_rows = nodes()
pod_rows = pods()

node_html = "\n".join(
    [
        (
            '<div class="card">'
            '<div class="node-role">node</div>'
            f'<div class="node-hostname">{escape(n)}</div>'
            f'<div class="node-ip">{escape(ip)}</div>'
            '<div class="node-specs">'
            f'<div class="spec-row"><span class="spec-key">Status</span><span class="spec-val">{escape(status)}</span></div>'
            f'<div class="spec-row"><span class="spec-key">Roles</span><span class="spec-val">{escape(roles)}</span></div>'
            f'<div class="spec-row"><span class="spec-key">Age</span><span class="spec-val">{escape(age)}</span></div>'
            f'<div class="spec-row"><span class="spec-key">K8s</span><span class="spec-val">{escape(version)}</span></div>'
            '</div></div>'
        )
        for n, status, roles, age, version, ip in node_rows
    ]
)

pod_html = "\n".join(
    [
        f'<tr><td class="stack-name">{escape(name)}</td><td>{escape(ready)}</td><td>{escape(status)}</td><td>{escape(restarts)}</td><td>{escape(age)}</td></tr>'
        for name, ready, status, restarts, age in pod_rows
    ]
)

html = f"""<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>lab.michka.dev - homelab cluster</title>
  <style>
    body {{ font-family: sans-serif; background: #0a0c0f; color: #e2e4e9; padding: 2rem; }}
    table {{ width: 100%; border-collapse: collapse; }}
    td, th {{ border-bottom: 1px solid #333; padding: .5rem; text-align: left; }}
    .card {{ border: 1px solid #333; padding: 1rem; margin: 1rem 0; border-radius: 8px; }}
    .node-role {{ text-transform: uppercase; color: #00d4c8; font-size: .8rem; }}
    .node-hostname {{ font-size: 1.2rem; font-weight: 700; }}
    .node-ip {{ color: #60a5fa; margin-bottom: .75rem; }}
    .spec-row {{ display: flex; justify-content: space-between; border-bottom: 1px solid #222; padding: .35rem 0; }}
    .spec-key {{ color: #8892a4; }}
    .spec-val {{ color: #e2e4e9; }}
    .stack-name {{ font-weight: 600; }}
  </style>
</head>
<body>
  <h1>Cluster snapshot</h1>
  <h2>Nodes</h2>
  {node_html}
  <h2>Pods in ingress-lab</h2>
  <table>
    <thead>
      <tr><th>Name</th><th>Ready</th><th>Status</th><th>Restarts</th><th>Age</th></tr>
    </thead>
    <tbody>
      {pod_html}
    </tbody>
  </table>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(OUT)
