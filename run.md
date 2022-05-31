# dns 
nohup python3 dns/dns.py --servers docker_setup/netsim/servers/10servers &
python3 dns/dns.py --servers docker_setup/netsim/servers/twolink
python3 dns/dns.py --servers docker_setup/netsim/servers/onelink
# server
python3 docker_setup/netsim/netsim.py servers start -s docker_setup/netsim/servers/10servers
python3 docker_setup/netsim/netsim.py servers stop -s docker_setup/netsim/servers/10servers
## onelink
python3 docker_setup/netsim/netsim.py twolink start
python3 docker_setup/netsim/netsim.py twolink stop
python3 docker_setup/netsim/netsim.py twolink run -e docker_setup/netsim/topology/twolink/twolink.events -l starter_proxy/logs/0.5log
# proxy
nohup python3 starter_proxy/proxy1.py --filename log1 --a 0.85 &
nohup python3 starter_proxy/proxy2.py --filename log2 --a 0.85 &
# grapher
python starter_proxy/grapher.py starter_proxy/logs/0.5log starter_proxy/logs/0.5log1 starter_proxy/logs/0.5log2