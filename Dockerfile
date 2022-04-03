#
# conductor:server - Netflix conductor server
#

# ===========================================================================================================
# 0. Builder stage
# ===========================================================================================================
FROM openjdk:11-jdk AS builder

LABEL maintainer="Netflix OSS <conductor@netflix.com>"

ARG CONDUCTOR_VERSION=v3.6.1

WORKDIR /
RUN git clone https://github.com/netflix/conductor.git
WORKDIR /conductor
RUN git checkout tags/$CONDUCTOR_VERSION

# Build the server on run
RUN ./gradlew build -x test --stacktrace

# ===========================================================================================================
# 1. Bin stage
# ===========================================================================================================
FROM openjdk:11-jre

LABEL maintainer="Rafa Martins <rafamarts@gmail.com>"

# Make app folders
RUN mkdir -p /app/config /app/logs /app/libs

RUN apt-get update
RUN apt-get install -y python bash curl gettext netcat-openbsd psmisc
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py && python get-pip.py
RUN pip2 install requests fmt

# Copy the compiled output to new image
COPY --from=builder /conductor/docker/server/bin /app
COPY --from=builder /conductor/docker/server/config /app/config
COPY --from=builder /conductor/server/build/libs/conductor-server-*-boot.jar /app/libs

# Provisionig Tasks and Workflows
WORKDIR /app
RUN mv /app/startup.sh /app/startup-conductor.sh
ADD app .

# Copy the files for the server into the app folders
RUN chmod +x /app/startup.sh
RUN chmod +x /app/startup-conductor.sh

HEALTHCHECK --interval=60s --timeout=30s --retries=10 CMD curl -I -XGET http://localhost:8080/health || exit 1

CMD [ "/app/startup.sh" ]
ENTRYPOINT [ "/bin/sh"]
