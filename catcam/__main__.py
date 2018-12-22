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
        # Email the picture.
        logger.info("Sending email...")
        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = COMMASPACE.join(settings.EMAIL_TO)
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = "[CatCam] Cat detected"
        msg.attach(MIMEText("A wild cat was spotted in the house!"))
        part = MIMEApplication(picture, Name="cat.jpg")
        part["Content-Disposition"] = 'attachment; filename="cat.jpg"'
        msg.attach(part)
        try:
            with smtplib.SMTP(settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
                smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                smtp.sendmail(settings.EMAIL_FROM, settings.EMAIL_TO, msg.as_string())
        except OSError as ex:
            logger.warning("Could not send email: %s", ex)
        else:
            logger.info("Email sent!")
        # All done!
        logger.info("Waiting for a bit...")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("CatCam has stopped")
