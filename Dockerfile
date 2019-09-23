FROM arm32v7/alpine

RUN apk update
RUN apk add --no-cache python3 py3-bottle py3-paho-mqtt git fontconfig ttf-freefont py3-graphviz
RUN cd /
RUN git clone https://github.com/3DIRK/z2m-nwm.git

CMD python3 /z2m-nwm/nwm.py
