#
# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# fabric.py
# Receives a message from a GG device on an MQTT topic.
# Calls another Lambda to publish the message to Hyperledger Fabric

import greengrasssdk
import base64
import platform
from threading import Timer
import logging
import json
import datetime

# Setup logging to stdout. GG will log to either the local filesystem or CloudWatch logs (or both), depending on
# how the GG Group is configured. See 'settings' under the GG Group.
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()

# Creating a greengrass core & Lambda sdk client
clientIoT = greengrasssdk.client('iot-data')
client = greengrasssdk.client('lambda')

# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.  The code will enter the infinite while loop
# below.
# If you execute a 'test' on the Lambda Console, this test will fail by hitting the
# execution timeout of three seconds.  This is expected as this function never returns
# a result.

def pi_run():
    # Publish the temp to an MQTT topic. This is really only for testing, so you can subscribe an MQTT client to this
    # topic and check that this Lambda is running
    clientIoT.publish(topic='pi/temp', payload='25')
    logger.info('Publishing to topic pi/temp, payload of 25')

    #Payload to publish to Hyperledger Fabric
    msg={"timestamp":datetime.datetime.now(), "temperature":25}
    msgJSON=json.dumps(msg, indent=4, sort_keys=True, default=str)

    client_context = json.dumps({
        'custom': 'custom text'
    })

    # Call the Lambda function to publish to Fabric

    try:
        response = client.invoke(
            ClientContext=base64.b64encode(bytes(client_context)),
            FunctionName='arn:aws:lambda:us-east-1:295744685835:function:fabric:4',
            InvocationType='RequestResponse',
            Payload=msgJSON
        )

        logger.info('Trying to call fabric Lambda. Response is: ' + str(response))
        logger.info(response['Payload'].read())
    except Exception as e:
        logger.error('Error calling fabric Lambda: ' + str(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, pi_run).start()


# Start executing the function above
pi_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
