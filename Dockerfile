FROM python:3.12.5-alpine3.20
ENV PYTHONUNBUFFERED=1
WORKDIR /sms2po
COPY requirements.txt /sms2po
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt && \
    apk add --update --no-cache tini && \
    adduser -D -H sms2po
USER sms2po
COPY sms2po.py /sms2po
EXPOSE 8088
ENTRYPOINT  ["/sbin/tini", "--", "python", "sms2po.py"]
