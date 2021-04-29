TAG?=0.2

build:
	docker build --network host . -t map-scheduler:$(TAG)

load: build
	kind load docker-image map-scheduler:$(TAG) --name kind

run: build
	docker run -ti map-scheduler:$(TAG)

kube-run: load
	kubectl delete pod map-scheduler --force; true
	kubectl run map-scheduler --image=map-scheduler:$(TAG)
	sleep 2
	kubectl logs -f map-scheduler
