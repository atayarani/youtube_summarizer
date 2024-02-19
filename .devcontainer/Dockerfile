FROM python:3.10-bookworm

USER root

RUN apt-get update && apt-get install --no-install-recommends -y glibc-source=2.36-9+deb12u4 wget &&\
    adduser nonroot && mkdir -p /home/nonroot && chown -R nonroot /home/nonroot 


USER nonroot
ENV RYE_INSTALL_OPTION "--yes"
ENV RYE_TOOLCHAIN_VERSION "cpython@3.10.13"
ENV RYE_HOME "/home/nonroot"
RUN sh -c 'curl -sSf https://rye-up.com/get | bash'

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "rye" ]
