from gpiozero import MotionSensor
import logging
from picamera import PiCamera
from datetime import timedelta
from datetime import datetime
from catcam import settings
from signal import pause

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="[%(levelname)s %(name)s] %(message)s", level=logging.INFO)
    pir = MotionSensor(17)
    delay = timedelta(minutes=1)
    time_stamp = datetime.now() - delay

    def motion_detected():
        nonlocal time_stamp
        if datetime.now() > (time_stamp + delay):
            logger.info("Motion detected!")
            filename = datetime.now().strftime("%m_%d_%Y__%H_%M_%S")
            camera = PiCamera()
            # camera.resolution = (1024, 768)
            # camera.start_preview()
            # # Camera warm-up time
            # time.sleep(2)
            # camera.capture('/home/pi/photos/{}.jpg'.format(filename))
            # logger.info("Picture taken! Snap!")
            # time_stamp = datetime.now()
            camera.resolution = (640, 480)
            camera.start_recording('/home/pi/photos/{}.h264'.format(filename))
            camera.wait_recording(30)
            camera.stop_recording()

    pir.when_motion = motion_detected

    logger.info("CatCam has started")
    pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
