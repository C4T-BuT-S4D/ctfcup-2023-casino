FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6 as builder

RUN apt update && apt install -y gcc

WORKDIR build/

COPY ./orders.c .

RUN gcc -O0 -Wl,-z,relro,-z,now -no-pie -o ./run ./orders.c


FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

RUN apt -y update && apt -y install socat

COPY --from=builder /build/run /app/run
RUN chmod +x /app/run
COPY flag.txt /

RUN echo "nobody:x:1337:1337:::" > /etc/passwd
RUN echo "nobody::1337:nobody" > /etc/group

RUN mkdir /app/orders && chown nobody:nobody /app/orders

WORKDIR /app
USER nobody

CMD socat "TCP-LISTEN:13002,reuseaddr,fork" "EXEC:/app/run"