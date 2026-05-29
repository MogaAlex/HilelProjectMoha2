FROM python:3.12


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    vim \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

#RUN pip install --upgrade pip && \
#    pip install -r requirements.txt \
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt



COPY . .

RUN chmod +x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]