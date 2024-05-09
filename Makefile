# MiniCPS Makefile

# VARIABLES {{{1

MININET = sudo mn

PYTHON3 = python3
PYTHON3s = sudo python3

# waterTower {{{1

watertower:
	cd waterTower; $(PYTHON3s) init.py; cd .. 
	sudo gnome-terminal -- sh -c 'cd waterTower; python3 run.py'
	sleep 5
	sudo gnome-terminal -- sh -c 'cd waterTower; python3 scada.py; exec bash'
	sleep 5
	xdg-open http://127.0.0.1:5000/


# CLEAN {{{1

clean:
	sudo pkill -f -u root $(PYTHON3)" -m cpppo.server.enip"
	sudo mn -c
	cd waterTower; sudo rm swat_s1_db.sqlite; sudo rm physical_log.csv; sudo rm -f logs/*.log; sudo rm -f minicps/*.pyc; rm -f minicps/*,cover
	sudo fuser -k 6653/tcp

# }}}
