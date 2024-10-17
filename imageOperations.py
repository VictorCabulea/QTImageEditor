import cv2
import numpy as np
from PyQt5.QtGui import QImage


class ImageProcessor:
    def cvMatToQImage(self, cvMat):
        qImage = QImage(cvMat.data, cvMat.shape[1],
                        cvMat.shape[0],
                        cvMat.shape[1] * 3, QImage.Format_RGB888)
        return qImage

    def qImageToCVMat(self, qimage):
        width = qimage.width()
        height = qimage.height()

        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)

        cv_mat = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

        return cv_mat

    def applyAverageFilter(self, image, value):
        try:
            if image is None:
                print("Failed to load the image.")
                return

            cvMat = self.qImageToCVMat(image)
            result = cv2.blur(cvMat, (value, value))
            return self.cvMatToQImage(result)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def applyMedianFilter(self, image, value):
        try:
            if image is None:
                print("Failed to load the image.")
                return

            cvMat = self.qImageToCVMat(image)
            result = cv2.medianBlur(cvMat, value)
            return self.cvMatToQImage(result)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def applyGaussianFilter(self, image, value):
        try:
            if image is None:
                print("Failed to load the image.")
                return

            cvMat = self.qImageToCVMat(image)
            result = cv2.GaussianBlur(cvMat, (value, value), 0)
            return self.cvMatToQImage(result)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def imageToGrayScale(self, image):
        try:
            if image is None:
                print("Failed to load the image.")
                return

            cvMat = self.qImageToCVMat(image)
            grayImage = cv2.cvtColor(cvMat, cv2.COLOR_BGR2GRAY)
            result = cv2.merge((grayImage, grayImage, grayImage))
            return self.cvMatToQImage(result)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def changeBrightness(self, image, value):
        try:
            if image is None:
                print("Failed to load the image.")
                return

            cvMat = self.qImageToCVMat(image)
            result = cv2.convertScaleAbs(cvMat, alpha=1, beta=value)
            return self.cvMatToQImage(result)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
