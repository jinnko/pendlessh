FROM python:3-alpine

WORKDIR /app

RUN apk --no-cache update \
 && apk --no-cache upgrade \
 && apk --no-cache add dumb-init gcc musl-dev

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/app/pendlessh.py"]

ADD requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt

USER nobody
