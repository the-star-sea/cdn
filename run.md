# dns 
nohup python3 dns/dns.py --servers docker_setup/netsim/servers/10servers &
# server
python3 docker_setup/netsim/netsim.py servers start -s docker_setup/netsim/servers/10servers
python3 docker_setup/netsim/netsim.py servers stop -s docker_setup/netsim/servers/10servers
# proxy
nohup python3 proxy1.py -filename log1 --a 0.85 &
# grapher
python grapher.py logs/netsim_log1 logs/log1 logs/log2