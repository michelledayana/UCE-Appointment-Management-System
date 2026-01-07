import time
import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

# ESTA ES LA FUNCIÓN QUE TE DI:
def conectar_kafka():
    print("Intentando conectar con Kafka...")
    while True:
        try:
            # Aquí configuramos el consumidor
            consumer = KafkaConsumer(
                'user_registered_topic',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='auth-service-group'
            )
            print("¡Conectado a Kafka exitosamente!")
            return consumer
        except NoBrokersAvailable:
            print("Kafka no está listo aún. Reintentando en 5 segundos...")
            time.sleep(5)

# ESTO ES LO QUE INICIA EL CONSUMIDOR:
def iniciar_consumidor():
    consumer = conectar_kafka() # Llamamos a la función segura
    for message in consumer:
        datos_usuario = message.value
        print(f"Recibido evento de usuario: {datos_usuario}")