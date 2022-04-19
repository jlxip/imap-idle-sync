FROM python:alpine

# Give parameters here too, so they're visibly set on Docker
ENV PORT=993 TIMEOUT=600

RUN ["mkdir", "/app"]
RUN ["chown", "nobody:nobody", "/app"]
COPY --chown=nobody:nobody imap-idle-sync.py /app/imap-idle-sync.py

USER nobody
CMD ["/app/imap-idle-sync.py"]
