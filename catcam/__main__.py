from gpiozero import MotionSensor
from io import BytesIO
import logging
from picamera import PiCamera
import time
from catcam import settings
import requests
from requests.exceptions import RequestException
from signal import pause

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="[%(levelname)s %(name)s] %(message)s", level=logging.INFO)
    pir = MotionSensor(4)

    def motion_detected():
        logger.info("Motion detected! It's a cat!")
        # Take a picture.
        with PiCamera() as camera, BytesIO() as stream:
            camera.vflip = True
            camera.hflip = True
            time.sleep(1)
            camera.capture(stream, format="jpeg")
            stream.seek(0)
            logger.info("Picture taken! Snap!")
            # Send the picture.
            logger.info("Sending pic...")
            try:
                url = "{}/node_manager/{}/".format(settings.HUB_URL, settings.NODE_ID)
                files = {'image': ("image.jpeg", stream, "image/jpeg")}
                response = requests.post(url, files=files,)
                response.raise_for_status()

            except RequestException as e:
                logger.warning("Could not send pic: {}".format(e))

            logger.info("Pic sent!")
        # All done!
        logger.info("Waiting for a bit...")
        time.sleep(30)

    pir.when_motion = motion_detected

    logger.info("CatCam has started")
    pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
