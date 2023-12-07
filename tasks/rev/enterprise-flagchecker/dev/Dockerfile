FROM ubuntu:22.04

RUN apt update && apt install -y git python3 python-is-python3

WORKDIR /build

# cache ya binary
RUN git clone https://github.com/yandex/yatool && cd yatool && ./ya --help

COPY sources/ .
RUN python3 create_checker.py

RUN mv checker yatool/library/python/ \
    && mv task yatool/task

WORKDIR /build/yatool
RUN --mount=type=cache,target=/root/.ya \
    ./ya make task && \
    cp -L task/task /build/task
