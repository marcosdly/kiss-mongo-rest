ARG arch
ARG port

FROM --platform=${arch} python:3.11-bookworm AS dev
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && git config --global --add safe.directory '*'
EXPOSE ${port}