ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY unifihassio /
RUN true
COPY pyunifi /
RUN true
COPY run.sh /
RUN true


# Install requirements for add-on
RUN apk add --no-cache python3
RUN apk add --no-cache py3-pip
RUN apk add --no-cache nginx

RUN pip install Flask
RUN pip install pyunifi
RUN pip install gunicorn



RUN chmod a+x /run.sh
COPY rootfs /
RUN true

CMD [ "/run.sh" ]
