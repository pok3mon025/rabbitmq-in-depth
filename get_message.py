import rabbitpy

url = 'amqp://guest:guest@localhost:5672/%2F'
connection = rabbitpy.Connection(url)
channel = connection.channel()
queue = rabbitpy.Queue(channel, 'example')

while len(queue) > 0:
    message = queue.get()
    print('Message:')
    print(' ID: %s' % message.properties['message_id'])
    print(' TIME: %s' % message.properties['timestamp'].isoformat())
    print(' Body: %s' % message.body)
    message.ack()
