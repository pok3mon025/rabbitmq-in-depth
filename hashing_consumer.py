import os
import hashlib
import rabbitpy

connection = rabbitpy.Connection()
channel = connection.channel()

queue_name = 'hashing-woker-%s' % os.getpid()
queue = rabbitpy.Queue(channel, queue_name, auto_delete=True, durable=False, exclusive=True)

if queue.declare():
    print('Worker queue declared')
if queue.bind('fanout-rpc-requests'):
    print('Worker queue bound')

for message in queue.consume_messages():
    hash_obj = hashlib.md5(message.body)
    print('Image with correlation-id of %s has a hash of %s' % (message.properties['correlation_id'], hash_obj.hexdigest()))
    message.ack()

