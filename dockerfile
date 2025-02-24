# Usar uma imagem base com Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Instalar as dependências
RUN pip install flask fuzzywuzzy

# Expor a porta 8080
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "app.py"]