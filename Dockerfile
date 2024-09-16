# ------------------------------------------------------------------------
# Build image
FROM continuumio/miniconda:latest AS builder

COPY conda-linux-64.lock /var/locks/conda-linux-64.lock
RUN conda create -p /opt/env --file /var/locks/conda-linux-64.lock &&\
    /opt/env/bin/pip install pyattimo==0.6.1

# ------------------------------------------------------------------------
# Runtime image
FROM ubuntu:noble
COPY --from=builder /opt/env /opt/env
COPY . .
ENV PATH="/opt/env/bin:${PATH}"

CMD python3 pipeline.py check

