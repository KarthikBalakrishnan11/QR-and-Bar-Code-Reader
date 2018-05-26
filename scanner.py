from pyzbar import pyzbar
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

def main():
	camera = PiCamera()
	camera.resolution = (640,480)
	camera.rotation =180
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640, 480))

	# allow the camera to warmup
	time.sleep(0.1)

	# capture frames from the camera        
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		rawCapture.truncate(0)

		barcodes = pyzbar.decode(image)

		for barcode in barcodes:
			# extract the bounding box location of the barcode and draw the
			# bounding box surrounding the barcode on the image
			(x, y, w, h) = barcode.rect
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
			# the barcode data is a bytes object so if we want to draw it on
			# our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
 
			# draw the barcode data and barcode type on the image
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(image, text, (0,25), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
 
			# print the barcode type and data to the terminal
			print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
 

		cv2.imshow('Output', image)


		k = cv2.waitKey(50) & 0xff
		if k == 27:  # 'esc' key has been pressed, exit program.
			break
		if k == 112:  # 'p' has been pressed. this will pause/resume the code.
			pause = not pause
			if (pause is True):
				print("Code is paused. Press 'p' to resume..")
				while (pause is True):
					# stay in this loop until
					key = cv2.waitKey(30) & 0xff
					if key == 112:
						pause = False
						print('Resume code')
						break 

        
    # When everything done, release the capture
	cv2.destroyAllWindows()


if __name__ == "__main__":
    # execute main
    main()