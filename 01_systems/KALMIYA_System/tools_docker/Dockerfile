FROM alpine:latest

# Instalar dependencias basicas seguras
RUN apk add --no-cache python3 bash curl jq

# Configurar usuario sin privilegios
RUN addgroup -g 1000 sandboxgroup && \
    adduser -u 1000 -G sandboxgroup -D sandboxuser

USER sandboxuser
WORKDIR /tmp

CMD ["tail", "-f", "/dev/null"]
