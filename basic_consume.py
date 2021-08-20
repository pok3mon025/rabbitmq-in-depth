import rabbitpy

for message in rabbitpy.consume('amqp://guest:guest@localhost:5672/%2F', 'test-messages'):
    message.pprint()
    message.ack()
