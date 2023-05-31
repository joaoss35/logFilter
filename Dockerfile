# A single layer containing cherry-picked pieces of the source code
FROM scratch AS source-code

COPY constants /output/app/constants
COPY app.py /output/app/app.py


FROM python:3.9-alpine

# Create a non-root user and group
RUN addgroup -S logfilter && adduser -S logfilter -G logfilter

WORKDIR /app

# Switch to the non-root user
USER logfilter

COPY --chown=logfilter:logfilter --from=source-code /output /

# Since I don't have any dependencies, no reason for copying and installing requirements.txt
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

CMD ["python", "app.py"]
