FROM jlxip/imap-idle-sync:latest

USER root
RUN apk add isync

VOLUME /config
RUN touch "/config/mbsyncrc"
ENV SYNC="mbsync -c /config/mbsyncrc"

USER nobody