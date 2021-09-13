import os
import rabbitpy
import time
from ch6 import utils

connection = rabbitpy.Connection()
channel = connection.channel()

exchange = rabbitpy.DirectExchange(channel, 'rpc-replies')
exchange.declare()

queue_name = 'response-queue-%s' % os.getpid()
response_queue = rabbitpy.Queue(channel, queue_name, auto_delete=True, durable=False, exclusive=True)

if response_queue.declare():
    print('Response queue declared')
if response_queue.bind('rpc-replies', queue_name):
    print('Response queue bound')

for img_id, filename in enumerate(utils.get_images()):
    print('Sending request for image #%s: %s' % (img_id, filename))

    message = rabbitpy.Message(channel, utils.read_image(filename), {
        'content_type': utils.mime_type(filename),
        'correlation_id': str(img_id),
        'headers': {'source': 'profile',
                    'object': 'image',
                    'action': 'new'},
        'reply_to': queue_name
    }, opinionated=True)

    message.publish('fanout-rpc-requests', 'detect-faces')

    message = None
    while not message:
        time.sleep(0.5)
        message = response_queue.get()

    message.ack()

    duration = (time.time() - time.mktime(message.properties['headers']['first_publish']))
    print('Facial detection RPC call for image %s duration %.2f' % (message.properties['correlation_id'], duration))

    utils.display_image(message.body, message.properties['content-type'])

channel.close()
connection.close()

