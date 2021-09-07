FROM python:3.8-alpine
LABEL maintainer="Valentin Rudloff"

RUN mkdir -p /var/log/capsule/

# bluez dependencies
RUN apt-get install -y libglib2.0-dev libical-dev libreadline-dev libudev-dev libdbus-1-dev libdbus-glib-1-dev

# download, compile & install bluez
RUN wget "http://www.kernel.org/pub/linux/bluetooth/bluez-5.34.tar.xz" && \
    tar xJvf bluez-5.34.tar.xz && cd bluez-5.34 && \
    ./configure --prefix=/usr/local --disable-systemd && \
    make -j 4 && \
    make install

COPY . .
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install lib/python-OBD

#EXPOSE 1884 Needed for MQTT

ENTRYPOINT [ "python3", "can_interface.py" ]