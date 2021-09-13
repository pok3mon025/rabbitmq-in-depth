import os
import rabbitpy
import time
from ch6 import detect
from ch6 import utils

connection = rabbitpy.Connection()
channel = connection.channel()

queue_name = 'rpc-worker-%s' % os.getpid()
queue = rabbitpy.Queue(channel, queue_name, auto_delete=True, durable=False, exclusive=True)

if queue.declare():
    print('Worker queue declared')
if queue.bind('direct-rpc-requests', 'detect-faces'):
    print('Worker queue bound')

for message in queue.consume_messages():
    duration = (time.time() - int(message.properties['timestamp'].strftime('%s')))
    print('Received RPC request published %.2f seconds ago % duration')

    temp_file = utils.write_temp_file(message.body, message.properties['content_type'])
    result_file = detect.faces(temp_file)

    properties = {'app_id': 'Chapter 6 Listing 2 Consumer',
                  'content_tpe': message.properties['content_type'],
                  'correlation_id': message.properties['correlation_id'],
                  'headers': {
                      'first_publish': message.properties['timestamp']
                  }}

    body = utils.read_image(result_file)
    os.unlink(temp_file)
    os.unlink(result_file)

    response = rabbitpy.Message(channel, body, properties)
    response.publish('rcp-replies', message.properties['reply_to'])
    message.ack()

