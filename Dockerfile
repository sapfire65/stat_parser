#FROM python:3.12.0a4-alpine3.17
FROM python:3.12-rc-alpine3.17

# update apk repositories
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# install chromedriver
#RUN apk update
#RUN apk add --no-cache chromium chromium-chromedriver tzdata

RUN apk update
RUN apk add curl unzip
RUN curl -O https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chrome-linux64.zip
RUN ls -l
RUN unzip chrome-linux64.zip
RUN mv chromedriver /usr/local/bin/






# Get all the prereqs
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk

#RUN apk update && \
#    apk add openjdk11-jre curl tar && \
#    curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz \
#    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
#    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
#    rm allure-2.13.8.tgz

WORKDIR /usr/workspace

# Copy the dependencies file
COPY ./requirements.txt /usr/workspace

# install Python dependencies
RUN pip3 install -r requirements.txt

