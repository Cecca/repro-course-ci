FROM mambaorg/micromamba:1.5.9-noble

COPY . .
RUN micromamba install -y -n base -f env.yaml && \
    micromamba clean --all --yes
RUN mkdir /tmp/app

CMD python3 pipeline.py check

