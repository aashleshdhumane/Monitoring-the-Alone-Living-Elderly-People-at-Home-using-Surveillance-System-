import cv2
from sendmail import MailSender

class Check:
    def __init__(self,eid):

        self.eid = eid

        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture('dataset/abc.mp4')
        #fall-03-cam1  adl-40-cam0

        fgbg = cv2.createBackgroundSubtractorMOG2()
        j = 0
        m = 0

        while (1):
            ret, frame = cap.read()

            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                fgmask = fgbg.apply(gray)
                contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    areas = []

                    for contour in contours:
                        ar = cv2.contourArea(contour)
                        areas.append(ar)

                    max_area = max(areas, default=0)

                    max_area_index = areas.index(max_area)

                    cnt = contours[max_area_index]

                    M = cv2.moments(cnt)

                    x, y, w, h = cv2.boundingRect(cnt)

                    cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

                    if h < w:
                        j += 1

                    if j > 30:
                        #print("FALL")
                        m = 1
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        break

                    if h > w:
                        j = 0
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    cv2.imshow('video', frame)

                    if cv2.waitKey(33) == 27:
                        break

            except Exception as e:
                break

        if m == 1:
            plaintext = "Hello User, \n" \
                        "There is a emergency. Patient fall is detected.\n" \
                        "\nThanks & Regards\nElderly Care\nRCOEM, Nagpur"

            ourmailsender = MailSender('elderlycare.pro20@gmail.com', 'Happy@998', ('smtp.gmail.com', 587))

            ourmailsender.set_message(plaintext, "Alert!", "Elderly Care")

            ourmailsender.set_recipients([eid])

            ourmailsender.connect()
            ourmailsender.send_all()

        else:
            print("No Fall occurs")


        cv2.destroyAllWindows()