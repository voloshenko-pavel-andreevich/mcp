FROM python:3.12-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "server.py"]

#FROM python:3.12-slim

#COPY . .

#RUN pip install -r requirements.txt

#CMD ["uvicorn", "server:mcp", "--host", "0.0.0.0", "--port", "80"]