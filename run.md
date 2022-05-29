# dns 
python3 dns.py --servers ../docker_setup/netsim/servers/2servers
# server
python3 netsim.py servers start -s servers/2servers
python3 netsim.py servers stop -s servers/2servers
# proxy
python3 proxy1.py -filename log3 --a 0.85
# grapher
python grapher.py logs/netsim_log1 logs/log1 logs/log2