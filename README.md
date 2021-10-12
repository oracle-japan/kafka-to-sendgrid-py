# Kafka to Sendgrid Python Script

Consume messages from Kafka and forward to Sendgrid.

## Usage

```bash
usage: kafka-to-sendgrid.py [-h] --sender SENDER [--to TO] [--cc CC]
                            [--bcc BCC] [--subject SUBJECT] --sendgrid-apikey
                            SENDGRID_APIKEY
                            [--sendgrid-template-id SENDGRID_TEMPLATE_ID]
                            [--kafka-bootstrap-servers KAFKA_BOOTSTRAP_SERVERS]
                            --kafka-topic KAFKA_TOPIC
                            [--kafka-group-id KAFKA_GROUP_ID]

optional arguments:
  -h, --help            show this help message and exit
  --sender SENDER       email address of the sender
  --to TO               list of "to" recipient email addresses delimited by ","
  --cc CC               list of "cc" recipient email addresses delimited by ","
  --bcc BCC             list of "bcc" recipient email addresses delimited by ","
  --subject SUBJECT     mail subject, ignored when --sendgrid-template-id is present
  --sendgrid-apikey SENDGRID_APIKEY
  --sendgrid-template-id SENDGRID_TEMPLATE_ID
  --kafka-bootstrap-servers KAFKA_BOOTSTRAP_SERVERS
                        list of Kafka bootstrap servers delimited by ",",
                        default is localhost:9092
  --kafka-topic KAFKA_TOPIC
  --kafka-group-id KAFKA_GROUP_ID 
                        default is my-group
```


## Build docker image

Dockerfile is available.

```bash
docker build -t kafka-to-sendgrid-py .
```

## SendGrid Dynamic Template

This script is assuming to receive messages as a json text via Kafka, then setting following two items as dynamic template data for SendGrid when `--sendgrid-template-id` is presetnt.
+ "content" : message as json object (you can use Handlebars)
+ "json" : message as json text 
