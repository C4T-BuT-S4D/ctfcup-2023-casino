FROM golang:1.21.5-alpine3.18 AS builder

WORKDIR /build

RUN echo "nobody:x:1000:1000:::" > etcpasswd
RUN echo "nobody::1000:nobody" > etcgroup
RUN mkdir dir

COPY go.* .
COPY *.go .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -o jail .

FROM scratch

COPY --from=builder /build/etcpasswd /etc/passwd
COPY --from=builder /build/etcgroup /etc/group
COPY --from=builder --chown=nobody:nobody --chmod=500 /build/jail /jail
COPY --from=builder --chown=nobody:nobody --chmod=400 /build/dir /tools
COPY --from=builder --chown=nobody:nobody --chmod=400 /build/dir /jokes
COPY --chown=nobody:nobody --chmod=400 tools/* /tools
COPY --chown=nobody:nobody --chmod=400 jokes/* /jokes

WORKDIR /
USER nobody

CMD [ "/jail" ]
