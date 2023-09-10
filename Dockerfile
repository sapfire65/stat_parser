# Собираем stable докер образ на основе python
FROM python:3.12.0a4-alpine3.17
#FROM python:3.12-rc-alpine3.17

# update apk repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.17/main" >> /etc/apk/repositories; \
    echo "https://dl-cdn.alpinelinux.org/alpine/v3.17/community" >> /etc/apk/repositories
#    echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories; \
#    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories; \

#    echo "http://mirror.yandex.ru/mirrors/alpine/v3.10/main" >> /etc/apk/repositories; \
#    echo "http://mirror.clarkson.edu/alpine/v3.10/main" >> /etc/apk/repositories; \
#    echo "http://mirror1.hs-esslingen.de/pub/Mirrors/alpine/v3.10/main" >> /etc/apk/repositories; \
#    echo "http://mirror.yandex.ru/mirrors/alpine/v3.10/main" >> /etc/apk/repositories; \
#    echo "http://mirror1.hs-esslingen.de/pub/Mirrors/alpine/v3.10/main" >> /etc/apk/repositories

# Вспомогательный набор библиотек
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk



# install chromedriver
RUN apk update &&  \
    apk upgrade && \
    apk add --no-cache chromium chromium-chromedriver

RUN pip install add --no-cache --upgrade pip



#RUN apk update && \
#    apk add openjdk11-jre curl tar && \
#    curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz \
#    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
#    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
#    rm allure-2.13.8.tgz

WORKDIR /usr/workspace

# Copy the dependencies file
COPY ./requirements.txt /usr/workspace

# install Python dependencies
RUN pip3 install -r requirements.txt

