import argparse
import json
import sys
import signal

from kafka import KafkaConsumer
import sendgrid
from sendgrid.helpers.mail import Mail, Email
from sendgrid.helpers.mail.personalization import Personalization

consumer: KafkaConsumer = None

def send_mail(body: str, args: argparse.Namespace, sg: sendgrid.SendGridAPIClient):

    mail = Mail(from_email=Email(args.sender))

    personalization = Personalization()
    for to in args.to.split(',') if args.to else []:
        personalization.add_to(Email(to.strip()))
    for cc in args.cc.split(',') if args.cc else []:
        personalization.add_to(Email(cc.strip()))
    for bcc in args.bcc.split(',') if args.bcc else []:
        personalization.add_bcc(Email(bcc.strip()))
    
    if args.sendgrid_template_id:
        content = json.loads(body)
        personalization.dynamic_template_data = {
            "content" : content,
            "json" : json.dumps(content, indent=2)
        }
        mail.template_id=args.sendgrid_template_id
    else:
        personalization.subject = args.subject

    mail.add_personalization(personalization)

    print(f'Sendgrid Request: {mail.get()}')
    response = sg.send(mail)

    print(f'Sendgrid Response: {response.status_code}')

def sig_handler(signum, frame) -> None:
    if(consumer):
        print('Closing consumer...')
        consumer.close()
    sys.exit(0)

def main():
    signal.signal(signal.SIGTERM, sig_handler)
    parser = argparse.ArgumentParser(description='Consume messages from Kafka and forward to Sendgrid.')
    parser.add_argument('--sender', required=True, help='email address of the sender')
    parser.add_argument('--to', help='list of "to" recipient email addresses delimited by ","')
    parser.add_argument('--cc', help='list of "cc" recipient email addresses delimited by ","')
    parser.add_argument('--bcc', help='list of "bcc" recipient email addresses delimited by ","')
    parser.add_argument('--subject', help='mail subject, ignored when --sendgrid-template-id is present')
    parser.add_argument('--sendgrid-apikey', required=True)
    parser.add_argument('--sendgrid-template-id')
    parser.add_argument('--kafka-bootstrap-servers', default='localhost:9092', 
                help='list of Kafka bootstrap servers delimited by ",", default is localhost:9092')
    parser.add_argument('--kafka-topic', required=True)
    parser.add_argument('--kafka-group-id', default='my-group', help='default is my-group')
    args = parser.parse_args()
    print(args)

    # To consume latest messages and auto-commit offsets
    global consumer
    consumer = KafkaConsumer(
                        args.kafka_topic,
                        group_id = args.kafka_group_id,
                        bootstrap_servers = args.kafka_bootstrap_servers.split(','),
                        enable_auto_commit=False)

    sg = sendgrid.SendGridAPIClient(args.sendgrid_apikey)

    for message in consumer:
        print('----- new message -----')
        print(f'{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}')
        send_mail(message.value.decode('utf-8'), args, sg)
        consumer.commit()

if __name__ == '__main__':
    main()