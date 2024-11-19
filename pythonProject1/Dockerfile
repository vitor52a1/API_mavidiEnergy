# Use uma imagem oficial do Python como imagem base
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do seu projeto para o diretório de trabalho no contêiner
COPY . /app

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta que a aplicação Flask vai rodar
EXPOSE 5000

# Defina o comando para rodar a aplicação Flask
CMD ["python", "app.py"]
