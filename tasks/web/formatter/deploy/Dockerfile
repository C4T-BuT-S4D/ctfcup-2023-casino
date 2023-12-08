FROM golang:1.21.5-alpine3.18 AS formatter-builder

WORKDIR /build
RUN mkdir dir

COPY formatters/src src

WORKDIR /build/src/json
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -o /build/json .

WORKDIR /build/src/yaml
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -o /build/yaml .

FROM python:3.12.0-alpine3.18

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --from=formatter-builder --chown=nobody:nobody --chmod=700 /build/dir uploads
COPY --from=formatter-builder --chown=nobody:nobody --chmod=700 /build/dir formatters
COPY --from=formatter-builder --chown=nobody:nobody --chmod=400 /build/json formatters/json
COPY --from=formatter-builder --chown=nobody:nobody --chmod=400 /build/yaml formatters/yaml
COPY app.py index.html .

USER nobody

CMD [ "gunicorn", "--workers=4", "--bind=:5000", "--keep-alive=0", "--access-logfile=-", "app:app" ]
