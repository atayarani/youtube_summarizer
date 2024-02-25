FROM python:3.10-bookworm

USER root


RUN echo "deb http://deb.debian.org/debian bookworm main contrib" > /etc/apt/sources.list.d/debian.source &&\
    echo "deb-src http://deb.debian.org/debian bookworm main contrib" >> /etc/apt/sources.list.d/debian.source &&\
    apt-get update &&\
    apt-get install --no-install-recommends -y glibc-source=2.36-9+deb12u4 wget=1.21.3-1+b2 fonts-firacode &&\
    adduser nonroot &&\
    mkdir -p /home/nonroot &&\
    chown -R nonroot /home/nonroot &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/* &&\
    sh -c "curl https://get.trunk.io -fsSL | bash -s -- -y" && chmod 0755 /usr/local/bin/trunk &&\
    sh -c "curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | bash" &&\
    chmod 0755 /bin/act

USER nonroot
ENV RYE_INSTALL_OPTION "--yes"
ENV RYE_TOOLCHAIN_VERSION "cpython@3.10.13"
ENV RYE_HOME "/home/nonroot"
RUN sh -c 'curl -sSf https://rye-up.com/get | bash'
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "rye" ]
