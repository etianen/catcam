from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from gpiozero import MotionSensor
from io import BytesIO
import logging
from picamera import PiCamera
import smtplib
import time
from catcam import settings
import requests
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="[%(levelname)s %(name)s] %(message)s", level=logging.INFO)
    pir = MotionSensor(4)
    logger.info("CatCam has started")
    while True:
        # Wait for motion.
        logger.info("Waiting for motion...")
        pir.wait_for_motion()
        logger.info("Motion detected! It's a cat!")
        # Take a picture.
        with PiCamera() as camera, BytesIO() as stream:
            camera.vflip = True
            camera.hflip = True
            time.sleep(2)
            camera.capture(stream, format="jpeg")
            picture = stream.getvalue()
        logger.info("Picture taken! Snap!")
        # Send the picture.
        logger.info("Sending pic...")
        try:
            pass  # TODO
        except RequestException as ex:
            logger.warning("Could not send pic: %s", ex)
        else:
            logger.info("Pic sent!")
        # All done!
        logger.info("Waiting for a bit...")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
