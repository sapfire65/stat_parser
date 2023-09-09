#FROM python:3.12.0a4-alpine3.17
FROM python:3.12-rc-alpine3.17

# update apk repositories
#RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
#    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# Устанавливаем переменные с зеркальными ссылками
ENV MIRROR_1="http://mirror.yandex.ru/mirrors/alpine/v3.10/main"
ENV MIRROR_2="http://mirror.clarkson.edu/alpine/v3.10/main"
ENV MIRROR_3="http://mirror1.hs-esslingen.de/pub/Mirrors/alpine/v3.10/main"

# Обновляем ссылки на зеркальные серверы и устанавливаем пакеты
RUN set -eux; \
    sed -i -e "s|dl-cdn.alpinelinux.org|$MIRROR_1|g" /etc/apk/repositories && \
    apk update && apk upgrade && \
    apk add --no-cache chromium chromium-chromedriver || true; \
    sed -i -e "s|dl-cdn.alpinelinux.org|$MIRROR_2|g" /etc/apk/repositories && \
    apk update && apk upgrade && \
    apk add --no-cache chromium chromium-chromedriver || true; \
    sed -i -e "s|dl-cdn.alpinelinux.org|$MIRROR_3|g" /etc/apk/repositories && \
    apk update && apk upgrade && \
    apk add --no-cache chromium chromium-chromedriver || true



# install chromedriver

#RUN apk update && apk upgrade && \
#    apk add --no-cache chromium chromium-chromedriver


# Создаем файл сценария для установки
RUN echo '#!/bin/sh' > /install.sh && \
    echo 'sed -i -e "s|dl-cdn.alpinelinux.org|$1|g" /etc/apk/repositories' >> /install.sh && \
    echo 'apk update' >> /install.sh && \
    echo 'apk upgrade' >> /install.sh && \
    echo 'apk add --no-cache chromium chromium-chromedriver' >> /install.sh && \
    chmod +x /install.sh

# Вызываем сценарий с двумя зеркальными серверами
RUN /install.sh $MIRROR_1 || /install.sh $MIRROR_2


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

