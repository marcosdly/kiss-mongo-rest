ARG arch
ARG port

FROM --platform=${arch} python:3.11-slim AS dev
RUN <<PKG sh
  apt-get update
  apt-get install -y --no-install-recommends \
    git
PKG
EXPOSE ${port}