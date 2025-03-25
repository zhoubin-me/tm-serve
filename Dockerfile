FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04

RUN apt-get update

RUN apt-get install -y git curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN echo "source /root/.local/bin/env" >> /root/.bashrc

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /workspace

WORKDIR /workspace

RUN git clone https://github.com/zhoubin-me/tm-serve.git

WORKDIR /workspace/tm-serve

RUN uv sync