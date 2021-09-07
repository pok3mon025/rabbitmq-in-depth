import rabbitpy

for iteration in range(10):
    rabbitpy.publish('amqp://guest:guest@localhost:5672/%2F', '', 'test-messages', 'go')
rabbitpy.publish('amqp://guest:guest@localhost:5672/%2F', '', 'test-messages', 'stop')
