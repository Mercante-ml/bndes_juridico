# Usa uma imagem leve do Python
FROM python:3.12-slim

# Evita que o Python crie arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema necessárias para o Postgres e outras libs
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libldap2-dev \ 
    libsasl2-dev  \   
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código (que ainda não existe, mas vai existir)
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando padrão (será sobrescrito pelo docker-compose na maioria das vezes)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]