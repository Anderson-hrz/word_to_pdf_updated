# Use a imagem oficial do Python 3.12.0-bullseye como base
FROM python:3.12.0-bullseye

# Defina o diretório de trabalho
WORKDIR /python-docker


# Atualiza o sistema e instala pacotes necessários (LibreOffice e Java)
RUN apt-get update && \
    apt-get --no-install-recommends install libreoffice -y && \
    apt-get install -y libreoffice-java-common default-jre

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copie o código da aplicação
COPY . .

# Expor a porta 5006
EXPOSE 5006

# Comando para iniciar a aplicação com o Gunicorn, escutando na porta 5005
CMD ["gunicorn", "-b", "0.0.0.0:5006", "app:app"]
