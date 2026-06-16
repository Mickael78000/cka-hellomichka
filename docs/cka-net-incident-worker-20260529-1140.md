# Capture worker hellomichka-a8
Date : 2026-05-29T11:40:16+02:00 / hôte hellomichka-A8 192.168.1.52

## A. UFW du worker — a-t-il les mêmes règles CNI que le control-plane ?
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp (OpenSSH)           ALLOW IN    Anywhere                  
22/tcp                     ALLOW IN    Anywhere                  
22/tcp (OpenSSH (v6))      ALLOW IN    Anywhere (v6)             
22/tcp (v6)                ALLOW IN    Anywhere (v6)             

## B. Interface VXLAN flannel.1 du worker
6: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default 
    link/ether aa:f8:c8:a8:69:42 brd ff:ff:ff:ff:ff:ff promiscuity 0  allmulti 0 minmtu 68 maxmtu 65535 
    vxlan id 1 local 192.168.1.52 dev enp1s0 srcport 0 0 dstport 8472 nolearning ttl auto ageing 300 udpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 64000 gso_max_segs 64 tso_max_size 64000 tso_max_segs 64 gro_max_size 65536 
flannel.1        UNKNOWN        10.42.1.0/32 fe80::a8f8:c8ff:fea8:6942/64 
cni0             UP             10.42.1.1/24 fe80::8020:62ff:fe0a:1bbf/64 
## C. Routes vers le réseau de pods
10.42.0.0/24 via 10.42.0.0 dev flannel.1 onlink 
10.42.1.0/24 dev cni0 proto kernel scope link src 10.42.1.1 
## D. Table FDB du VXLAN (apprentissage MAC du VTEP distant)
6e:fd:f4:bf:07:b6 dst 192.168.1.103 self permanent
## E. subnet.env flannel sur le worker
FLANNEL_NETWORK=10.42.0.0/16
FLANNEL_SUBNET=10.42.1.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
## F. RETOUR worker -> control-plane : ping le pod web (10.42.0.16)

--- 10.42.0.16 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1015ms

## G. Le control-plane est-il joignable en VXLAN 8472 depuis le worker ?
Connection to 192.168.1.103 8472 port [udp/*] succeeded!
## H. Logs flannel/réseau récents du worker
May 06 11:05:08 hellomichka-A8 k3s[72179]: I0506 11:05:08.917297   72179 vxlan_network.go:265] Received Subnet Event with VxLan: BackendType: vxlan, PublicIP: 192.168.1.103, PublicIPv6: (nil), BackendData: {"VNI":1,"VtepMAC":"6e:fd:f4:bf:07:b6"}, BackendV6Data: (nil)
May 09 21:06:00 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:00+02:00" level=info msg="Starting flannel with backend vxlan"
May 09 21:06:00 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:00+02:00" level=info msg="Flannel found PodCIDR assigned for node hellomichka-a8"
May 09 21:06:00 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:00+02:00" level=info msg="The interface enp1s0 with ipv4 address 192.168.1.52 will be used by flannel"
May 09 21:06:00 hellomichka-A8 k3s[2559]: I0509 21:06:00.967596    2559 kube.go:537] Starting kube subnet manager
May 09 21:06:01 hellomichka-A8 k3s[2559]: I0509 21:06:01.968607    2559 vxlan.go:128] VXLAN config: VNI=1 Port=0 GBP=false Learning=false DirectRouting=false
May 09 21:06:01 hellomichka-A8 k3s[2559]: I0509 21:06:01.973033    2559 kube.go:704] List of node(hellomichka-a8) annotations: map[string]string{"alpha.kubernetes.io/provided-node-ip":"192.168.1.52,2a02:8424:61e9:4301:3e5d:9a70:87cd:77ae", "flannel.alpha.coreos.com/backend-data":"{\"VNI\":1,\"VtepMAC\":\"aa:f8:c8:a8:69:42\"}", "flannel.alpha.coreos.com/backend-type":"vxlan", "flannel.alpha.coreos.com/kube-subnet-manager":"true", "flannel.alpha.coreos.com/public-ip":"192.168.1.52", "k3s.io/hostname":"hellomichka-A8", "k3s.io/internal-ip":"192.168.1.52", "k3s.io/node-args":"[\"agent\"]", "k3s.io/node-config-hash":"GZQRQFYBZ66LXQ3S6LFQY4P2PRVRTRP4R33MPNQYKYP5CT5JRQWA====", "k3s.io/node-env":"{\"K3S_TOKEN\":\"********\",\"K3S_URL\":\"https://100.117.114.43:6443\"}", "node.alpha.kubernetes.io/ttl":"0", "volumes.kubernetes.io/controller-managed-attach-detach":"true"}
May 09 21:06:01 hellomichka-A8 k3s[2559]: I0509 21:06:01.973062    2559 vxlan.go:199] Interface flannel.1 mac address set to: aa:f8:c8:a8:69:42
May 09 21:06:01 hellomichka-A8 k3s[2559]: I0509 21:06:01.995027    2559 iptables.go:50] Starting flannel in iptables mode...
May 09 21:06:01 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:01+02:00" level=warning msg="no subnet found for key: FLANNEL_NETWORK in file: /run/flannel/subnet.env"
May 09 21:06:01 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:01+02:00" level=warning msg="no subnet found for key: FLANNEL_SUBNET in file: /run/flannel/subnet.env"
May 09 21:06:01 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:01+02:00" level=warning msg="no subnet found for key: FLANNEL_IPV6_NETWORK in file: /run/flannel/subnet.env"
May 09 21:06:01 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:01+02:00" level=warning msg="no subnet found for key: FLANNEL_IPV6_SUBNET in file: /run/flannel/subnet.env"
May 09 21:06:01 hellomichka-A8 k3s[2559]: I0509 21:06:01.995077    2559 iptables.go:101] Current network or subnet (10.42.0.0/16, 10.42.1.0/24) is not equal to previous one (0.0.0.0/0, 0.0.0.0/0), trying to recycle old iptables rules
May 09 21:06:02 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:02+02:00" level=info msg="Wrote flannel subnet file to /run/flannel/subnet.env"
May 09 21:06:02 hellomichka-A8 k3s[2559]: time="2026-05-09T21:06:02+02:00" level=info msg="Running flannel backend."
May 09 21:06:02 hellomichka-A8 k3s[2559]: I0509 21:06:02.006841    2559 vxlan_network.go:68] watching for new subnet leases
May 09 21:06:02 hellomichka-A8 k3s[2559]: I0509 21:06:02.006867    2559 vxlan_network.go:115] starting vxlan device watcher
May 09 21:06:02 hellomichka-A8 k3s[2559]: I0509 21:06:02.006874    2559 subnet.go:150] Batch elem [0] is { lease.Event{Type:0, Lease:lease.Lease{EnableIPv4:true, EnableIPv6:false, Subnet:ip.IP4Net{IP:0xa2a0000, PrefixLen:0x18}, IPv6Subnet:ip.IP6Net{IP:(*ip.IP6)(nil), PrefixLen:0x0}, Attrs:lease.LeaseAttrs{PublicIP:0xc0a80167, PublicIPv6:(*ip.IP6)(nil), BackendType:"vxlan", BackendData:json.RawMessage{0x7b, 0x22, 0x56, 0x4e, 0x49, 0x22, 0x3a, 0x31, 0x2c, 0x22, 0x56, 0x74, 0x65, 0x70, 0x4d, 0x41, 0x43, 0x22, 0x3a, 0x22, 0x36, 0x65, 0x3a, 0x66, 0x64, 0x3a, 0x66, 0x34, 0x3a, 0x62, 0x66, 0x3a, 0x30, 0x37, 0x3a, 0x62, 0x36, 0x22, 0x7d}, BackendV6Data:json.RawMessage(nil)}, Expiration:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), Asof:0}} }
May 09 21:06:02 hellomichka-A8 k3s[2559]: I0509 21:06:02.006922    2559 vxlan_network.go:265] Received Subnet Event with VxLan: BackendType: vxlan, PublicIP: 192.168.1.103, PublicIPv6: (nil), BackendData: {"VNI":1,"VtepMAC":"6e:fd:f4:bf:07:b6"}, BackendV6Data: (nil)
## FIN CAPTURE WORKER — fichier /root/cka-net-incident-worker-20260529-1140.md
[?2004h]0;root@hellomichka-A8: ~root@hellomichka-A8:~# ^C[KOUT=/root/cka-genese-worker-$(date +%Y%m%d-%H%M).md
{
echo "# Genèse k3s — worker hellomichka-a8 — $(date -Is)"

[7mecho -e "\n## 1. Version et binaire"[27m
[7mk3s --version[27m
[7mwhich k3s; readlink -f "$(which k3s)"[27m

[7mecho -e "\n## 2. Unit systemd agent : la commande de join réelle"[27m
[7msystemctl cat k3s-agent.service 2>/dev/null | sed -n '1,60p'[27m

[7mecho -e "\n## 3. Config & variables d'environnement de join (URL serveur, token masqué)"[27m
[7mcat /etc/rancher/k3s/config.yaml 2>/dev/null || echo "(pas de config.yaml)"[27m
[7mecho "--- env (token masqué) ---"[27m
[7msed -E 's/(TOKEN=).*/\1***MASQUE***/' /etc/systemd/system/k3s-agent.service.env 2>/dev/null || echo "(pas de fichier env)"[27m

[7mecho -e "\n## 4. Date d'installation de l'agent (preuve horodatée)"[27m
[7mstat -c '%y  %n' /usr/local/bin/k3s 2>/dev/null[27m
[7mls -la --time-style=long-iso /var/lib/rancher/k3s/agent/ 2>/dev/null | head[27m

[7mecho -e "\n## 5. Premier démarrage agent dans les logs (join)"[27m
[7mjournalctl -u k3s-agent --no-pager 2>/dev/null | head -40[27m

[7mecho -e "\n## 6. CNI côté worker : subnet et tunnel"[27m
[7mcat /run/flannel/subnet.env 2>/dev/null[27m
[7mecho "--- flannel.1 (VTEP local) ---"[27m
[7mip -d link show flannel.1 2>/dev/null | sed -n '1,3p'[27m
[7mecho "--- cni0 ---"[27m
[7mip -d addr show cni0 2>/dev/null | sed -n '1,3p'[27m

[7mecho -e "\n## 7. UFW : l'asymetrie — etat brut et numerote"[27m
[7mufw status verbose 2>/dev/null[27m
[7mecho "--- numerote ---"[27m
[7mufw status numbered 2>/dev/null[27m
[7mecho "--- politique de forward ---"[27m
[7mgrep -E 'DEFAULT_FORWARD_POLICY|DEFAULT_INPUT_POLICY' /etc/default/ufw 2>/dev/null[27m

[7mecho -e "\n## 8. Genese de l'asymetrie : QUAND les regles UFW ont ete posees"[27m
[7mecho "--- dates des fichiers de regles UFW ---"[27m
[7mls -la --time-style=long-iso /etc/ufw/*.rules 2>/dev/null[27m
[7mecho "--- activation initiale d'ufw dans les logs ---"[27m
[7mjournalctl -u ufw --no-pager 2>/dev/null | head -15[27m
[7mecho "--- premieres lignes du journal systeme mentionnant ufw (install) ---"[27m
[7mgrep -i 'ufw' /var/log/dpkg.log 2>/dev/null | head -10[27m[7m} | tee "$OUT"[27m[7mecho; echo ">>> capture ecrite dans $OUT"[27m[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[Aecho -e "\n## 1. Version et binaire"
k3s --version
which k3s; readlink -f "$(which k3s)"

echo -e "\n## 2. Unit systemd agent : la commande de join réelle"
systemctl cat k3s-agent.service 2>/dev/null | sed -n '1,60p'

echo -e "\n## 3. Config & variables d'environnement de join (URL serveur, token masqué)"
cat /etc/rancher/k3s/config.yaml 2>/dev/null || echo "(pas de config.yaml)"
echo "--- env (token masqué) ---"
sed -E 's/(TOKEN=).*/\1***MASQUE***/' /etc/systemd/system/k3s-agent.service.env 2>/dev/null || echo "(pas de fichier env)"

echo -e "\n## 4. Date d'installation de l'agent (preuve horodatée)"
stat -c '%y  %n' /usr/local/bin/k3s 2>/dev/null
ls -la --time-style=long-iso /var/lib/rancher/k3s/agent/ 2>/dev/null | head

echo -e "\n## 5. Premier démarrage agent dans les logs (join)"
journalctl -u k3s-agent --no-pager 2>/dev/null | head -40

echo -e "\n## 6. CNI côté worker : subnet et tunnel"
cat /run/flannel/subnet.env 2>/dev/null
echo "--- flannel.1 (VTEP local) ---"
ip -d link show flannel.1 2>/dev/null | sed -n '1,3p'
echo "--- cni0 ---"
ip -d addr show cni0 2>/dev/null | sed -n '1,3p'

echo -e "\n## 7. UFW : l'asymetrie — etat brut et numerote"
ufw status verbose 2>/dev/null
echo "--- numerote ---"
ufw status numbered 2>/dev/null
echo "--- politique de forward ---"
grep -E 'DEFAULT_FORWARD_POLICY|DEFAULT_INPUT_POLICY' /etc/default/ufw 2>/dev/null

echo -e "\n## 8. Genese de l'asymetrie : QUAND les regles UFW ont ete posees"
echo "--- dates des fichiers de regles UFW ---"
ls -la --time-style=long-iso /etc/ufw/*.rules 2>/dev/null
echo "--- activation initiale d'ufw dans les logs ---"
journalctl -u ufw --no-pager 2>/dev/null | head -15
echo "--- premieres lignes du journal systeme mentionnant ufw (install) ---"
grep -i 'ufw' /var/log/dpkg.log 2>/dev/null | head -10} | tee "$OUT"echo; echo ">>> capture ecrite dans $OUT"
[?2004l# Genèse k3s — worker hellomichka-a8 — 2026-05-29T12:21:43+02:00

## 1. Version et binaire
k3s version v1.35.4+k3s1 (5dc8fe68)
go version go1.25.9
/usr/local/bin/k3s
/usr/local/bin/k3s

## 2. Unit systemd agent : la commande de join réelle
# /etc/systemd/system/k3s-agent.service
[Unit]
Description=Lightweight Kubernetes
Documentation=https://k3s.io
Wants=network-online.target
After=network-online.target

[Install]
WantedBy=multi-user.target

[Service]
Type=notify
EnvironmentFile=-/etc/default/%N
EnvironmentFile=-/etc/sysconfig/%N
EnvironmentFile=-/etc/systemd/system/k3s-agent.service.env
KillMode=process
Delegate=yes
User=root
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
TimeoutStartSec=0
Restart=always
RestartSec=5s
ExecStartPre=-/sbin/modprobe br_netfilter
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/k3s \
    agent \


## 3. Config & variables d'environnement de join (URL serveur, token masqué)
(pas de config.yaml)
--- env (token masqué) ---
K3S_TOKEN=***MASQUE***
K3S_URL='https://100.117.114.43:6443'

## 4. Date d'installation de l'agent (preuve horodatée)
2026-05-06 11:05:03.301085713 +0200  /usr/local/bin/k3s
total 72
drwx------  5 root root 4096 2026-05-06 11:05 .
drwxr-xr-x  4 root root 4096 2026-05-06 11:05 ..
-rw-------  1 root root  570 2026-05-09 21:06 client-ca.crt
-rw-------  1 root root 1153 2026-05-09 21:06 client-k3s-controller.crt
-rw-------  1 root root  227 2026-05-06 11:05 client-k3s-controller.key
-rw-------  1 root root 1189 2026-05-09 21:06 client-kubelet.crt
-rw-------  1 root root  227 2026-05-06 11:05 client-kubelet.key
-rw-------  1 root root 1149 2026-05-09 21:06 client-kube-proxy.crt
-rw-------  1 root root  227 2026-05-06 11:05 client-kube-proxy.key

## 5. Premier démarrage agent dans les logs (join)
May 06 11:05:04 hellomichka-A8 systemd[1]: Starting k3s-agent.service - Lightweight Kubernetes...
May 06 11:05:04 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:04+02:00" level=info msg="Acquiring lock file /var/lib/rancher/k3s/data/.lock"
May 06 11:05:04 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:04+02:00" level=info msg="Preparing data dir /var/lib/rancher/k3s/data/4373bc7eebb47a3f48304fd6d0af7f82c8f47cc82032776b7e85e70e3b73cf93"
May 06 11:05:04 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:04+02:00" level=info msg="Starting k3s agent v1.35.4+k3s1 (5dc8fe68)"
May 06 11:05:04 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:04+02:00" level=info msg="Updated load balancer k3s-agent-load-balancer default server: 100.117.114.43:6443"
May 06 11:05:04 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:04+02:00" level=info msg="Running load balancer k3s-agent-load-balancer 127.0.0.1:6444 -> [] [default: 100.117.114.43:6443]"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Module overlay was already loaded"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Module nf_conntrack was already loaded"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Module br_netfilter was already loaded"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Module iptable_nat was already loaded"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Module iptable_filter was already loaded"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=warning msg="Failed to load kernel module nft-expr-counter with modprobe"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Getting list of apiserver endpoints from server"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Creating k3s-cert-monitor event broadcaster"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Logging containerd to /var/lib/rancher/k3s/agent/containerd/containerd.log"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Running containerd -c /var/lib/rancher/k3s/agent/etc/containerd/config.toml"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Event occurred" apiVersion= fieldPath= kind=Node logger=k3s message="Node and Certificate Authority certificates managed by k3s are OK" object=hellomichka-a8 reason=CertificateExpirationOK type=Normal
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Running kube-proxy --cluster-cidr=10.42.0.0/16 --conntrack-max-per-core=0 --conntrack-tcp-timeout-close-wait=0s --conntrack-tcp-timeout-established=0s --healthz-bind-address=127.0.0.1 --hostname-override=hellomichka-a8 --kubeconfig=/var/lib/rancher/k3s/agent/kubeproxy.kubeconfig --proxy-mode=iptables"
May 06 11:05:06 hellomichka-A8 k3s[72179]: I0506 11:05:06.491876   72179 shared_informer.go:370] "Waiting for caches to sync"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Got apiserver addresses from supervisor: [192.168.1.103:6443]"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Adding server to load balancer k3s-agent-load-balancer: 192.168.1.103:6443"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Updated load balancer k3s-agent-load-balancer server addresses -> [192.168.1.103:6443] [default: 100.117.114.43:6443]"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Connecting to proxy" url="wss://192.168.1.103:6443/v1-k3s/connect"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Connected to proxy" url="wss://192.168.1.103:6443/v1-k3s/connect"
May 06 11:05:06 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:06+02:00" level=info msg="Remotedialer connected to proxy" url="wss://192.168.1.103:6443/v1-k3s/connect"
May 06 11:05:06 hellomichka-A8 k3s[72179]: I0506 11:05:06.992421   72179 shared_informer.go:377] "Caches are synced"
May 06 11:05:07 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:07+02:00" level=info msg="containerd is now running"
May 06 11:05:07 hellomichka-A8 k3s[72179]: time="2026-05-06T11:05:07+02:00" level=info msg="Running kubelet --cloud-provider=external --config-dir=/var/lib/rancher/k3s/agent/etc/kubelet.conf.d --containerd=/run/k3s/containerd/containerd.sock --hostname-override=hellomichka-a8 --kubeconfig=/var/lib/rancher/k3s/agent/kubelet.kubeconfig --node-ip=192.168.1.52,2a02:8424:61e9:4301:3e5d:9a70:87cd:77ae --node-labels= --read-only-port=0"
May 06 11:05:07 hellomichka-A8 k3s[72179]: Flag --containerd has been deprecated, This is a cadvisor flag that was mistakenly registered with the Kubelet. Due to legacy concerns, it will follow the standard CLI deprecation timeline before being removed.
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.673366   72179 server.go:521] "Kubelet version" kubeletVersion="v1.35.4+k3s1"
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.673380   72179 server.go:523] "Golang settings" GOGC="" GOMAXPROCS="" GOTRACEBACK=""
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.673398   72179 watchdog_linux.go:95] "Systemd watchdog is not enabled"
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.673406   72179 watchdog_linux.go:138] "Systemd watchdog is not enabled or the interval is invalid, so health checking will not be started."
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.674494   72179 dynamic_cafile_content.go:161] "Starting controller" name="client-ca-bundle::/var/lib/rancher/k3s/agent/client-ca.crt"
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.675963   72179 server.go:1414] "Using cgroup driver setting received from the CRI runtime" cgroupDriver="systemd"
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.680679   72179 server.go:771] "--cgroups-per-qos enabled, but --cgroup-root was not specified.  Defaulting to /"
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.680691   72179 server.go:832] "NoSwap is set due to memorySwapBehavior not specified" memorySwapBehavior="" FailSwapOn=false
May 06 11:05:07 hellomichka-A8 k3s[72179]: I0506 11:05:07.680746   72179 swap_util.go:119] "Swap is on" /proc/swaps contents=<
May 06 11:05:07 hellomichka-A8 k3s[72179]:         Filename                                Type                Size                Used                Priority
May 06 11:05:07 hellomichka-A8 k3s[72179]:         /swap.img                               file                8388604                0                -2

## 6. CNI côté worker : subnet et tunnel
FLANNEL_NETWORK=10.42.0.0/16
FLANNEL_SUBNET=10.42.1.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
--- flannel.1 (VTEP local) ---
6: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default 
    link/ether aa:f8:c8:a8:69:42 brd ff:ff:ff:ff:ff:ff promiscuity 0  allmulti 0 minmtu 68 maxmtu 65535 
    vxlan id 1 local 192.168.1.52 dev enp1s0 srcport 0 0 dstport 8472 nolearning ttl auto ageing 300 udpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 64000 gso_max_segs 64 tso_max_size 64000 tso_max_segs 64 gro_max_size 65536 
--- cni0 ---
7: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default qlen 1000
    link/ether 92:a2:66:b3:46:3b brd ff:ff:ff:ff:ff:ff promiscuity 0  allmulti 0 minmtu 68 maxmtu 65535 
    bridge forward_delay 1500 hello_time 200 max_age 2000 ageing_time 30000 stp_state 0 priority 32768 vlan_filtering 0 vlan_protocol 802.1Q bridge_id 8000.92:a2:66:b3:46:3b designated_root 8000.92:a2:66:b3:46:3b root_port 0 root_path_cost 0 topology_change 0 topology_change_detected 0 hello_timer    0.00 tcn_timer    0.00 topology_change_timer    0.00 gc_timer   23.24 vlan_default_pvid 1 vlan_stats_enabled 0 vlan_stats_per_port 0 group_fwd_mask 0 group_address 01:80:c2:00:00:00 mcast_snooping 1 no_linklocal_learn 0 mcast_vlan_snooping 0 mcast_router 1 mcast_query_use_ifaddr 0 mcast_querier 0 mcast_hash_elasticity 16 mcast_hash_max 4096 mcast_last_member_count 2 mcast_startup_query_count 2 mcast_last_member_interval 100 mcast_membership_interval 26000 mcast_querier_interval 25500 mcast_query_interval 12500 mcast_query_response_interval 1000 mcast_startup_query_interval 3125 mcast_stats_enabled 0 mcast_igmp_version 2 mcast_mld_version 1 nf_call_iptables 0 nf_call_ip6tables 0 nf_call_arptables 0 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535 tso_max_size 524280 tso_max_segs 65535 gro_max_size 65536 

## 7. UFW : l'asymetrie — etat brut et numerote
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp (OpenSSH)           ALLOW IN    Anywhere                  
22/tcp                     ALLOW IN    Anywhere                  
22/tcp (OpenSSH (v6))      ALLOW IN    Anywhere (v6)             
22/tcp (v6)                ALLOW IN    Anywhere (v6)             

--- numerote ---
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] OpenSSH                    ALLOW IN    Anywhere                  
[ 2] 22/tcp                     ALLOW IN    Anywhere                  
[ 3] OpenSSH (v6)               ALLOW IN    Anywhere (v6)             
[ 4] 22/tcp (v6)                ALLOW IN    Anywhere (v6)             

--- politique de forward ---
DEFAULT_INPUT_POLICY="DROP"
DEFAULT_FORWARD_POLICY="DROP"

## 8. Genese de l'asymetrie : QUAND les regles UFW ont ete posees
--- dates des fichiers de regles UFW ---
-rw-r----- 1 root root  915 2024-03-11 14:18 /etc/ufw/after6.rules
-rw-r----- 1 root root 1004 2024-03-11 14:18 /etc/ufw/after.rules
-rw-r----- 1 root root 6700 2024-03-11 14:18 /etc/ufw/before6.rules
-rw-r----- 1 root root 2537 2024-03-11 14:18 /etc/ufw/before.rules
-rw-r----- 1 root root 1523 2026-05-07 06:48 /etc/ufw/user6.rules
-rw-r----- 1 root root 1517 2026-05-07 06:48 /etc/ufw/user.rules
--- activation initiale d'ufw dans les logs ---
Sep 28 08:47:22 hellomichka-A8 systemd[1]: Starting ufw.service - Uncomplicated firewall...
Sep 28 08:47:22 hellomichka-A8 systemd[1]: Finished ufw.service - Uncomplicated firewall.
-- Boot fb51ebbc7ee14ad48383510322408c11 --
Sep 28 16:49:11 hellomichka-A8 systemd[1]: Starting ufw.service - Uncomplicated firewall...
Sep 28 16:49:11 hellomichka-A8 systemd[1]: Finished ufw.service - Uncomplicated firewall.
-- Boot 4007f1f4407f48e9be87f1c084577cf6 --
Sep 29 18:27:33 hellomichka-A8 systemd[1]: Starting ufw.service - Uncomplicated firewall...
Sep 29 18:27:33 hellomichka-A8 systemd[1]: Finished ufw.service - Uncomplicated firewall.
-- Boot 4622894eacf545d8aca13d991ddee332 --
Sep 30 11:26:05 hellomichka-A8 systemd[1]: Starting ufw.service - Uncomplicated firewall...
Sep 30 11:26:05 hellomichka-A8 systemd[1]: Finished ufw.service - Uncomplicated firewall.
-- Boot 50346fe54c194a6ea953f6c6c78c9d77 --
Oct 03 18:52:42 hellomichka-A8 systemd[1]: Starting ufw.service - Uncomplicated firewall...
Oct 03 18:52:42 hellomichka-A8 systemd[1]: Finished ufw.service - Uncomplicated firewall.
-- Boot e28492046cc64edb9ecaeff9c7d1499a --
--- premieres lignes du journal systeme mentionnant ufw (install) ---
2026-05-07 06:48:32 status triggers-pending ufw:all 0.36.2-6
2026-05-07 06:48:37 trigproc ufw:all 0.36.2-6 <none>
2026-05-07 06:48:37 status half-configured ufw:all 0.36.2-6
2026-05-07 06:48:37 status installed ufw:all 0.36.2-6

>>> capture ecrite dans /root/cka-genese-worker-20260529-1221.md
[?2004h]0;root@hellomichka-A8: ~root@hellomichka-A8:~# [K]0;root@hellomichka-A8: ~root@hellomichka-A8:~# [K]0;root@hellomichka-A8: ~root@hellomichka-A8:~# exit
[?2004llogout
