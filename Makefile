IMAGE_NAME=letsrolld

ifndef VERBOSE
.SILENT:
endif

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it --rm --name $(IMAGE_NAME) \
		-v $(PWD)/letsrolld.db:/app/letsrolld.db \
		-v $(PWD)/cache.sqlite:/app/cache.sqlite \
		-v $(PWD)/data:/app/data \
		$(IMAGE_NAME)

test:
	pdm install
	pdm run pytest
