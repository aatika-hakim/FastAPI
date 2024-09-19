from aiokafka import AIOKafkaConsumer  # type: ignore
import json
from app.deps import get_session
from app.models.product_model import Product
from app.crud.product_crud import add_new_product


async def consume_product_messages(topic, bootstrap_servers):
    """Fetch and handle product messages from Kafka."""    
    # Initialize Kafka consumer for the given topic and server
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product_consumer_group",
        auto_offset_reset='earliest'
    )

    # Start the Kafka consumer
    await consumer.start()
    try:
        # Continuously listen for new messages on the topic
        async for message in consumer:
            print(f"Message received from topic '{message.topic}'")

            # Decode and parse the product data from the message
            product_data = json.loads(message.value.decode())
            print(f"Product data received: {product_data}")

            # Create a new session and add the product to the database
            with next(get_session()) as session:
                db_insert_product = add_new_product(product_data=Product(**product_data), session=session)
                print(f"Product successfully stored in the database: {db_insert_product}")
    finally:
        # Stop the Kafka consumer when finished
        await consumer.stop()
        print("Kafka consumer has been stopped.")
