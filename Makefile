.PHONY: all test-svc start-svc install clean

test-svc: start-svc
	systemctl is-active covind >/dev/null 2>&1 && echo YES || echo NO

start-svc:
ifneq (,$(wildcard ./covind.service))
	cp covind.service /lib/systemd/system/covind.service
	systemctl daemon-reload
	systemctl enable covind.service
	systemctl start covind
endif

install:
	apt install systemd python3 python3-dev python3-pip -y
	pip install -r requirements.txt

clean:
	rm -rf /lib/systemd/system/covind.service
	rm -rf __pycache__
	rm -rf *.pyc
