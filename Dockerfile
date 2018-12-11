from ubuntu

LABEL maintainer "Cody De Arkand <cdearkland@vmware.com> and Grant Orchard (gorchard@vmware.com)"
LABEL description "Caspyr Image"

RUN apt update && apt install -y \
    git \
    python3.6 \
    python3-pip

RUN pip3 install requests

COPY caspyr /usr/local/lib/python3.6/dist-packages/caspyr

CMD ["/bin/sh"]

