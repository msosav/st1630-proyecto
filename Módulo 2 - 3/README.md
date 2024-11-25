


# **Documentación del Proyecto: Módulos 2 y 3**
**Pipeline de Procesamiento y Almacenamiento de Datos**

Este documento detalla los pasos necesarios para implementar y probar los módulos 2 (procesamiento de datos) y 3 (almacenamiento en S3) del proyecto.

---

## **Requisitos previos**
1. Acceso a una cuenta de AWS con las siguientes configuraciones:
   - **Kinesis Data Stream** configurado (ARN proporcionado por el equipo del módulo 1).
   - Permisos para utilizar **DynamoDB**, **S3** y **Lambda**.
2. Código del productor ejecutándose en una instancia **EC2** (módulo 1).

---

## **Módulo 2: Procesamiento de datos y almacenamiento en DynamoDB**

### **1. Crear la tabla en DynamoDB**
1. Accede a la consola de **DynamoDB**.
2. Asegúrate de estar en la región donde se configuró el flujo de Kinesis.
3. Haz clic en **Create Table**.
4. Configura los detalles de la tabla:
   - **Table name:** `StockMarketData` (o un nombre relevante).
   - **Partition Key:** `symbol` (Tipo: String).
   - **Sort Key:** `timestamp` (Tipo: String).
5. Selecciona **Use default settings** y ajusta lo siguiente:
   - **Capacity Mode:** On-demand (para escalar automáticamente).
6. Opcional: Configura índices secundarios globales (GSI) si necesitas consultas adicionales.
7. Guarda los cambios.

---

### **2. Crear la función Lambda**
1. Accede a la consola de **AWS Lambda**.
2. Haz clic en **Create Function** y selecciona **Author from scratch**.
3. Configura:
   - **Function name:** `ProcessKinesisToStore`.
   - **Runtime:** Python 3.9.
   - **Execution role:** Usa un rol existente o crea uno con permisos adecuados.
4. Haz clic en **Create Function**.

---

### **3. Agregar el código a Lambda**
1. En la pestaña **Code**, reemplaza el contenido con el siguiente código para procesar datos y almacenarlos en DynamoDB:

```python
import json
import boto3
import base64
from datetime import datetime
from decimal import Decimal

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = 'StockMarketData'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            payload_base64 = record['kinesis']['data']
            payload_decoded = base64.b64decode(payload_base64).decode('utf-8')
            payload = json.loads(payload_decoded, parse_float=Decimal)
            transformed_data = {
                'symbol': payload['symbol'],
                'price': Decimal(str(payload['price'])),
                'timestamp': payload['timestamp'],
                'day': datetime.fromisoformat(payload['timestamp']).strftime('%Y-%m-%d')
            }
            table.put_item(Item=transformed_data)
        return {'statusCode': 200, 'body': 'Datos procesados correctamente'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
```

### **4. Configurar el disparador de Kinesis**
1. Ve a la pestaña **Configuration > Triggers** en Lambda.
2. Haz clic en **Add Trigger**.
3. Selecciona **Kinesis** y configura:
   - **Stream:** Selecciona el flujo `stock-market-stream`.
   - **Batch size:** 100.
   - **Starting position:** Latest.
4. Haz clic en **Add**.

---

### **5. Prueba del módulo 2**
1. Asegúrate de que el productor en **EC2** esté enviando datos al flujo de Kinesis.
2. Valida que:
   - La función Lambda transforma `price` a **Decimal**.
   - Los datos se guardan correctamente en DynamoDB con los atributos: `symbol`, `price`, `timestamp`, y `day`.

---

## **Módulo 3: Almacenamiento en S3**

### **1. Crear el bucket S3**
1. Accede a la consola de **Amazon S3**.
2. Haz clic en **Create Bucket**.
3. Configura:
   - **Bucket name:** `stock-market-data-username`.
   - **Block Public Access:** Recomendado desactivado (si necesitas acceso público).
4. Haz clic en **Create Bucket**.

---

### **2. Modificar la función Lambda para almacenar datos en S3**
Actualiza la función Lambda con el siguiente código para guardar datos procesados y crudos (**RAW** y **PROCESSED**) como archivos JSON individuales.

```python
import json
import boto3
import base64
from datetime import datetime
from decimal import Decimal

# Inicializar clientes de AWS
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table_name = 'StockMarketData'
bucket_name = 'stock-market-data-username'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            payload_base64 = record['kinesis']['data']
            payload_decoded = base64.b64decode(payload_base64).decode('utf-8')
            payload = json.loads(payload_decoded, parse_float=Decimal)

            # Guardar datos crudos
            save_to_s3(f"raw/{payload['symbol']}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}.json", payload)

            # Transformar y guardar datos procesados
            transformed_data = {
                'symbol': payload['symbol'],
                'price': Decimal(str(payload['price'])),
                'timestamp': payload['timestamp'],
                'day': datetime.fromisoformat(payload['timestamp']).strftime('%Y-%m-%d')
            }
            table.put_item(Item=transformed_data)
            save_to_s3(f"processed/{transformed_data['symbol']}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}.json", transformed_data)
        return {'statusCode': 200, 'body': 'Datos procesados y guardados en S3'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

def save_to_s3(key, data):
    try:
        file_content = json.dumps(data, default=str)
        s3.put_object(Bucket=bucket_name, Key=key, Body=file_content, ContentType='application/json')
    except Exception as e:
        print(f"Error guardando datos en S3: {e}")
```

### **1. Haz clic en Deploy**
Haz clic en el botón **Deploy** en la consola de Lambda para aplicar los cambios realizados en la función.

---

### **3. Prueba del módulo 3**
1. Reinicia el productor en **EC2**.
2. Valida que:
   - Los datos crudos se guarden en la carpeta **raw/** del bucket S3.
   - Los datos procesados se guarden en la carpeta **processed/** del bucket S3.
   - Cada registro se guarde como un archivo JSON individual.

---

## **Conclusión**
Con estos pasos, se configuran correctamente los módulos 2 y 3 para procesar datos desde **Kinesis**, almacenarlos en **DynamoDB**, y guardar archivos crudos y procesados en **S3**. Esto permite análisis y visualización futuros de los datos que es el ultimo modulo.


