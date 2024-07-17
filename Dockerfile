FROM bitnami/kafka:latest

# Instalar nano
RUN apt-get update && apt-get install -y nano

# Copiar archivos de configuración u otros ajustes necesarios

# Comando por defecto al iniciar el contenedor
CMD ["kafka-server-start.sh", "/opt/bitnami/kafka/config/server.properties"]
