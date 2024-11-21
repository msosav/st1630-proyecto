# Módulo 1: Generación de datos (EC2 y Kinesis Data Streams)

## Despliegue de la API

Para la generación de datos, se desplegará una API en una instancia de EC2 que constantemente estará enviando datos ficticios de precios de acciones a un flujo de Kinesis Data Streams.

### Pasos a seguir

1. **Creación de la instancia de EC2**

   - Ingresar a la consola de AWS y dirigirse al servicio de EC2.
   - Hacer clic en el botón "Launch Instance" para lanzar una nueva instancia.
   - Seleccionar una `Amazon Linux 2 AMI` y elegir una instancia `t2.micro`.
   - En la configuración de instancias, agregar una regla de seguridad para permitir el tráfico `HTTP`.
   - Descargar el par de claves y lanzar la instancia.

2. **Conexión a la instancia**

   - Conectarse a la instancia de EC2 mediante SSH.

3. **Instalación de Docker**

   - Actualizar los paquetes de la instancia con el comando.

     ```bash
     sudo yum update -y
     ```

   - Instalar Docker y Docker Compose con el siguiente comando.

     ```bash
     sudo amazon-linux-extras install docker
     ```

   - Iniciar el servicio de Docker con el comando.

     ```bash
     sudo systemctl enable docker
     sudo systemctl start docker
     ```

   - Agregar el usuario al grupo de Docker con el comando.

     ```bash
     sudo usermod -a -G docker ec2-user
     ```

   - Cerrar la sesión y volver a conectarse a la instancia.
   - Instalar Docker Compose con el siguiente comando.

     ```bash
     sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     docker-compose version
     ```

4. **Despliegue de la API**

   - Crear un archivo `docker-compose.yml` con el siguiente contenido.

     ```yaml
     services:
       api:
         image: msosav/stock-market-shares:latest
         ports:
           - "80:80"
         restart: always
     ```

   - Correr el contenedor con el comando.

     ```bash
     docker-compose up -d
     ```

5. **Verificación de la API**

   - Acceder a la dirección IP pública de la instancia de EC2 en un navegador.
   - Verificar que la API esté funcionando correctamente yendo a la ruta `/stocks/USD`.

    <div align="center">
        <img src="./res/verificacion-api.png" width="600">
    </div>
