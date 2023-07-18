FROM registry.suse.com/bci/python:3
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY entrypoint.sh 
COPY action.sh .
COPY checks-checker .
RUN mkdir /checks
WORKDIR /checks
ENTRYPOINT [ "/app/entrypoint.sh" ]
