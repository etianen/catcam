from gpiozero import MotionSensor
from io import BytesIO
import logging
from picamera import PiCamera
import time
from catcam import settings
import requests
<<<<<<< HEAD
from requests import HTTPError

=======
from requests.exceptions import RequestException
>>>>>>> 3202aa048f2dba7d6ecf679475b011c13f22b717

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
<<<<<<< HEAD
=======

>>>>>>> 3202aa048f2dba7d6ecf679475b011c13f22b717
            logger.info("Picture taken! Snap!")
            # Send the picture.
            logger.info("Sending pic...")
            try:
<<<<<<< HEAD
                url = "{}/node_manager/{}".format(settings.HUB_URL, settings.NODE_ID)
                response = requests.post(url, stream,)
                response.raise_for_status()

            except HTTPError as e:
                status_code = e.response.status_code
                logger.warning("Could not send pic: {}".format(status_code))

            logger.info("Pic sent!")
=======
                url = "{}node_manager/{}/".format(settings.HUB_URL, settings.NODE_ID)
                files = {'image': stream}
                requests.post(url, files,)
            except RequestException as ex:
                logger.warning("Could not send pic: %s", ex)
            else:
                logger.info("Pic sent!")
>>>>>>> 3202aa048f2dba7d6ecf679475b011c13f22b717
        # All done!
        logger.info("Waiting for a bit...")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
