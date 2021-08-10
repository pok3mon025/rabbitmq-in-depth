import rabbitpy

url = 'amqp://guest:guest@localhost:5672/%2F'

connection = rabbitpy.Connection(url)

# 커넥션에 새로운 채널 열기
channel = connection.channel()

# 채널을 인자로 전달해서 새로운 익스체인지 객체 생성
exchange = rabbitpy.Exchange(channel, 'chapter2-example')

# RabbitMQ 서버에 익스체인지 선언하기
exchange.declare()

# 채널을 전달해 새로운 Queue 객체 생성하기
queue = rabbitpy.Queue(channel, 'example')

# RabbitMQ 서버에 큐 선언하기
queue.declare()

# RabbitMQ 서버의 큐와 익스체인지를 연결하기
queue.bind(exchange, 'example-routing-key')

# example 큐에 저장할 메시지 발행
for message_number in range(0, 10):
    Message = rabbitpy.Message(channel,
                               'Test message #%i' % message_number,
                               {'content_type': 'text/plain'},
                               opinionated=True)
    Message.publish(exchange, 'example-routing-key')
