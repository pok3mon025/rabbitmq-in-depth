import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        for message in rabbitpy.Queue(channel, 'test-messages'):
            message.pprint()
            message.ack()
            if message.body == 'stop':
                break
