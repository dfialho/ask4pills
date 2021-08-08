FROM python:3.8 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code
COPY --from=builder /root/.local /root/.local
COPY config.json .
COPY ./src .
ENV PATH=/root/.local:$PATH
CMD [ "python", "./server.py", "-c", "config.json" ]
