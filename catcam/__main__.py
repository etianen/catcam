from gpiozero import MotionSensor
from io import BytesIO
import logging
from picamera import PiCamera
import time
from catcam import settings
import requests
from requests import HTTPError


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
            logger.info("Picture taken! Snap!")
            # Send the picture.
            logger.info("Sending pic...")
            try:
                url = "{}/node_manager/{}".format(settings.HUB_URL, settings.NODE_ID)
                response = requests.post(url, stream,)
                response.raise_for_status()

            except HTTPError as e:
                status_code = e.response.status_code
                logger.warning("Could not send pic: {}".format(status_code))

            logger.info("Pic sent!")
        # All done!
        logger.info("Waiting for a bit...")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
