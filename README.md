# Proyecto Final - Sistemas Intensivos en Datos <!-- omit in toc -->

Sistema de monitoreo en tiempo casi real del cambio de las acciones con FastAPI y AWS

## Tabla de Contenidos <!-- omit in toc -->

- [Descripción del Caso](#descripción-del-caso)
  - [Caso de Negocio](#caso-de-negocio)
  - [Caso Tecnológico](#caso-tecnológico)
- [Metodología Analítica a Emplear](#metodología-analítica-a-emplear)
- [Arquitectura de Referencia](#arquitectura-de-referencia)
  - [Ingesta de Datos](#ingesta-de-datos)
  - [Almacenamiento](#almacenamiento)
  - [Visualización](#visualización)
- [Implementación](#implementación)

## Integrantes <!-- omit in toc -->

- Miguel Sosa Villegas
- Santiago Ospina Idrobo
- Diego Alexánder Múnera Tobón
- Yhilmar Andrés Chaverra Castaño

## Descripción del Caso

### Caso de Negocio

El objetivo de este proyecto es desarrollar un sistema que permita a los gestores de portafolios e inversionistas monitorear en tiempo casi real el rendimiento de sus activos mediante una visualización de los precios y rendimientos actuales de cada acción del portafolio. Este sistema proporciona una vista centralizada y actualizada de los cambios de precios, facilitando la identificación de tendencias y patrones en los activos del portafolio, lo cual es crucial para la toma de decisiones estratégicas y gestión de riesgos en el mercado financiero.

### Caso Tecnológico

El proyecto enfrenta desafíos típicos de Big Data, principalmente en la ingesta y procesamiento de datos en tiempo casi real, dado el volumen de datos generados en mercados bursátiles. Para capturar, almacenar y analizar estos datos, el sistema empleará una arquitectura basada en servicios de AWS:

- Ingesta de datos: Utilización de Kinesis para la extracción periódica de datos de la API y procesamiento en lotes simulando un flujo continuo.

- Almacenamiento: Los datos se almacenarán en un Data Lake en S3 para datos crudos y en DynamoDB para datos procesados.

- Visualización: La visualización de los datos se realizará mediante el servicio de Grafana, permitiendo a los usuarios finales acceder a los datos en tiempo casi real.

Esta solución aborda el reto de ingestión continua, almacenamiento en un Data Lake y visualización en tiempo casi real, con un enfoque escalable y de bajo costo.

## Metodología Analítica a Emplear

Para la implementación del proyecto se utilizará la metodología CRISP-DM (Cross-Industry Standard Process for Data Mining), que nos permitirá definir un ciclo de vida de análisis y procesamiento de datos eficaz en seis fases principales:

- **Comprensión del Negocio:** Definir métricas de rendimiento y alertas de interés para los gestores de portafolio, estableciendo criterios clave para la evaluación de cambios de precio.

- **Comprensión de los Datos:** Realizar un análisis preliminar de los datos de API, comprendiendo su estructura, frecuencia y formato, para una ingesta y transformación adecuadas.

- **Preparación de los Datos:** Configuración de Kinesis para capturar datos, enviándolos a S3 y DynamoDB.

- **Modelado:** Diseño de estructuras de almacenamiento en S3 y DynamoDB, optimizando para consultas de tiempo casi real en Grafana.

- **Evaluación:** Validar que los datos ingresen correctamente a intervalos específicos y que el sistema funcione sin interrupciones, permitiendo un análisis en tiempo casi real.

- **Despliegue:** Configuración de dashboards en Grafana para visualización de datos, permitiendo a los usuarios finales monitorear el rendimiento de sus activos en tiempo casi real.

## Arquitectura de Referencia

Para este sistema de monitoreo, la arquitectura de referencia está basada en servicios de AWS que optimizan la ingesta, almacenamiento, y análisis en tiempo casi real:.

### Ingesta de Datos

- **Amazon Kinesis Data Streams con Kinesis Agent:** Kinesis Agent es configurado para capturar y enviar datos de la API de Alpha Vantage a Kinesis Data Streams. Kinesis, a su vez, permite que los datos se procesen en tiempo casi real, alimentando nuestro pipeline para ser enviados a Amazon S3.

  - Kinesis Agent actúa como un agente en la instancia de EC2 o en el sistema donde se ejecutan las solicitudes de datos de Alpha Vantage, capturando y enviando el flujo de datos de manera continua hacia Kinesis Data Streams.
  - Kinesis Data Streams sirve como el buffer de ingesta, proporcionando un flujo continuo que puede ser fácilmente escalado para manejar volúmenes grandes de datos en tiempo casi real.

- **Kinesis Data Firehose (Opcional):** Si se necesita una integración directa con S3 o Elasticsearch, Kinesis Firehose puede configurarse para recibir los datos de Kinesis Data Streams y almacenarlos directamente en Amazon S3 para el Data Lake, o en Elasticsearch para consultas en tiempo casi real.

### Almacenamiento

- **Amazon S3:** Almacén de datos crudos, donde se guardan archivos JSON para cada lote de datos extraídos. Actúa como Data Lake para almacenar toda la información histórica.

- **AWS Glue:** Crea un catálogo de datos en S3 para integrarse fácilmente con Redshift si se requiere análisis histórico avanzado.

- **Amazon DynamoDB:** Base de datos NoSQL para almacenar datos procesados, como precios y rendimientos de acciones. Permite consultas de tiempo casi real para la visualización de datos.

### Visualización

- **Amazon Grafana:** Servicio de BI que permite la creación de dashboards y visualizaciones interactivas de los datos almacenados en Athena (la cual se alimenta de los datos almacenados en Amazon S3). Los usuarios finales pueden monitorear el rendimiento de sus activos en tiempo casi real, identificando tendencias y patrones en los precios de las acciones.

Esta arquitectura permite el despliegue de un sistema de análisis en tiempo casi real utilizando los datos de la API, con un diseño modular y escalable en AWS.

## Implementación

- [Módulo 1: Generación de datos (EC2 y Kinesis Data Streams)](https://github.com/msosav/st1630-proyecto/tree/main/M%C3%B3dulo%201) - Miguel Sosa Villegas
- [Módulo 2: Procesamiento de datos (Lambda y DynamoDB)](https://github.com/msosav/st1630-proyecto/tree/2b19bea04736e186bd2c38eb9047e148c3e8660c/M%C3%B3dulo%202%20-%203) - Santiago Ospina Idrobo
- [Módulo 3: Almacenamiento histórico (S3 y monitoreo)](https://github.com/msosav/st1630-proyecto/tree/2b19bea04736e186bd2c38eb9047e148c3e8660c/M%C3%B3dulo%202%20-%203) - Yhilmar Andrés Chaverra Castaño
- [Módulo 4: Análisis y visualización (Amazon Athena y Grafana)](https://github.com/msosav/st1630-proyecto/tree/2b19bea04736e186bd2c38eb9047e148c3e8660c/M%C3%B3dulo%204) - Diego Alexánder Múnera Tobón


