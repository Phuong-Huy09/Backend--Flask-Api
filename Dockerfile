FROM --platform=linux/amd64 python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# System deps + MS ODBC 18 + sqlcmd (mssql-tools18)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg apt-transport-https ca-certificates \
    build-essential \
    unixodbc unixodbc-dev \
 && curl https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/microsoft.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 mssql-tools18 \
 && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> /etc/profile \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && pip install --no-cache-dir pyodbc

# App dirs
RUN mkdir -p instance

# Copy source
COPY src/app.py .
COPY src/api/ ./api/
COPY src/domain/ ./domain/
COPY src/infrastructure/ ./infrastructure/
COPY src/services/ ./services/
COPY src/scripts/ ./scripts/
COPY src/migrations/ ./migrations/
COPY src/create_app.py .
COPY src/app_logging.py .
COPY src/config.py .
COPY src/cors.py .
COPY src/error_handler.py .
COPY src/dependency_container.py .
COPY src/swagger_config.json .

# (KHÔNG khuyến khích copy .env vào image; nên truyền env qua docker-compose)
# COPY .env .

EXPOSE 5000
ENV PYTHONPATH=/app

# Nếu bạn có entrypoint đợi DB (entrypoint.sh), thêm:
# COPY src/entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh
# CMD ["/app/entrypoint.sh"]

# Giữ container sống để có thể exec vào
CMD ["tail", "-f", "/dev/null"]
