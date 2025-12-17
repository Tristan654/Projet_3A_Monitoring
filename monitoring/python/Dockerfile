FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install flask paramiko
COPY main.py .
CMD ["python", "main.py"]