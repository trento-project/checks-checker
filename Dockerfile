FROM registry.suse.com/bci/python:3
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY checks-checker .
COPY entrypoint.sh .
RUN mkdir /checks
WORKDIR /checks
ENTRYPOINT [ "/app/entrypoint.sh" ]
