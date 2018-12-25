#
# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# fabric.py
import greengrasssdk
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')


def handler(event, context):
    logger.info('Invoked with payload ' + str(event))
    logger.info('Invoked with context ' + str(context))
    return 'Invoked successfully'