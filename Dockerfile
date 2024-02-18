FROM python:3.12.1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
# CMD ["uvicorn", "main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "8001"]
EXPOSE 8000