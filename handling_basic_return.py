import datetime
import rabbitpy

connection = rabbitpy.Connection()
try:
    with connection.channel() as channel:
        body = 'server.cpu.utilization 25.5 1350884514'
        message = rabbitpy.Message(channel,
                                   body,
                                   {'content_type': 'text/plain',
                                    'timestamp': datetime.datetime.now(),
                                    'message_type': 'graphite metric'})
        message.publish('chapter2-example',
                        'server-metrics',
                        mandatory=True)
except rabbitpy.exceptions.MessageReturnedException as error:
    print('Publish failure: %s' % error)
