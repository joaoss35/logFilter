# A single layer containing cherry-picked pieces of the source code
FROM scratch AS source-code

COPY constants /output/app/constants
COPY app.py /output/app/app.py


FROM python:3.10-alpine

LABEL maintainer="Joao Pacheco joaopachecos@hotmail.com"

# Create a non-root user and group
RUN addgroup -S logfilter && adduser -S logfilter -G logfilter

WORKDIR /app

# Switch to the non-root user
USER logfilter

COPY --chown=logfilter:logfilter --from=source-code /output /

# Since I don't have any dependencies, no reason for copying and installing requirements.txt
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

LABEL version="1.0" \
      description="A log filter for a legacy application" \
      docker.cmd="docker run --rm --name logfilter --env LOG_LEVEL=1 joaoss35/logfilter:1.0"

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
