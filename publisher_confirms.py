import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel, 'chapter4-example')
        exchange.declare()
        # RabbitMQ로 발행자 확인 기능 켜기
        channel.enable_publisher_confirms()
        message = rabbitpy.Message(channel,
                                   'This is an important message',
                                   {'content_type': 'text/plain',
                                    'message_type': 'very important'})
        # 메시지를 발행하고 발행 확인을 위해 응답 평가
        if message.publish('chapter4-example', 'important.message'):
            print('The message was confirmed')
