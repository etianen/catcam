from gpiozero import MotionSensor
from io import BytesIO
import logging
from picamera import PiCamera
import time
from datetime import timedelta
from datetime import datetime
from catcam import settings
import requests
from requests.exceptions import RequestException
from signal import pause

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="[%(levelname)s %(name)s] %(message)s", level=logging.INFO)
    pir = MotionSensor(17)
    delay = timedelta(minutes=15)
    time_stamp = datetime.now() - delay

    def motion_detected():
        nonlocal time_stamp
        if datetime.now() > (time_stamp + delay):
            logger.info("Motion detected!")
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


            # Record a video and save to a file
            logger.info("Starting video...")
            with PiCamera() as camera:
                camera.resolution = (640, 480)
                file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                camera.start_recording('/home/pi/videos/{}.h264'.format(file_name))
                camera.wait_recording(5)
                camera.stop_recording()
            logger.info("Saved video!")

            time_stamp = datetime.now()

            # All done!

    pir.when_motion = motion_detected

    logger.info("CatCam has started")
    pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
