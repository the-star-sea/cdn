chmod +x /usr/local/apache2/bin/httpd
cd /usr/local/apache2/lib/
rm libaprutil-1.so.0
ln -s libaprutil-1.so.0.5.3 libaprutil-1.so.0
rm libexpat.so.0
ln -s libexpat.so.0.5.0 libexpat.so.0
rm libapr-1.so.0
ln -s libapr-1.so.0.5.1 libapr-1.so.0
pip3 install flask,numpy,pymysql
pip install numpy,matplotlib
# nohup python3 dns/dns.py --servers docker_setup/netsim/servers/10servers &
# nohup python3 starter_proxy/proxy1.py --filename log1 --a 0.5 &
# nohup python3 starter_proxy/proxy2.py --filename log2 --a 0.5 &
# python3 docker_s                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          etup/netsim/netsim.py twolink start