import cv2
import numpy as np
import Improve

def add():
    ######################################
    path = "TryTemp3.jpg"
    widthImg = 700
    heightImg = 1000
    question = 50
    choices = 5
    ans = []
    grading = []
    cameraNo = 0
    #####################################

    # cap = cv2.VideoCapture(cameraNo)
    video = cv2.VideoCapture(1)
    # address = "http://192.168.1.104:8080/video"
    # video.open(address)
    video.set(10, 150)

    while True:
        success, img = video.read()
        if success == False:
            img = cv2.imread(path)

        ##### PROCESSING
        img = cv2.resize(img, (widthImg, heightImg))
        imgContours = img.copy()
        imgFinal = img.copy()
        imgBiggestContours = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 70)
        try:
            # FINDING ALL CONTOURS
            contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)
            # FIND RECTANGLES
            rectCon = Improve.rectCountour(contours)
            biggestContour = Improve.getCornerPoints(rectCon[0])
            # print(biggestContour.shape)
            gradePoints = Improve.getCornerPoints(rectCon[1])
            # print(biggestContour)

            if biggestContour.size != 0 and gradePoints.size != 0:
                cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
                cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)

            biggestContour = Improve.reorder(biggestContour)
            gradePoints = Improve.reorder(gradePoints)

            pt1 = np.float32(biggestContour)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

            ptG1 = np.float32(gradePoints)
            ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))
            # cv2.imshow("Grade",imgGradeDisplay)

            # Apply Threshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 50, 255, cv2.THRESH_BINARY_INV)[1]
            # cv2.imshow("imgThresh",imgThresh)
            boxes = Improve.splitBoxes(imgThresh)
            # cv2.imshow("Test",boxes[0])
            # cv2.imshow("Try", imgWarpColored)

            # GETTING NONZERO PIXEL VALUE
            myPixelVal = np.zeros((question, choices))
            countC = 0
            countR = 0

            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if (countC == choices): countR += 1;countC = 0
            print(myPixelVal)

            # FINDING INDEX VALUES OF THE MARKINGS
            myIndex = []
            for x in range(0, question):
                arr = myPixelVal[x]
                # print("arr",arr)
                myIndexVal = np.where(arr == np.amax(arr))
                # print(myIndexVal[0])
                myIndex.append(myIndexVal[0][0])
            print(myIndex)

            # DISPLAY ANSWERKEY IN LETTERS

            imgDisplayAnskey = np.zeros([heightImg, widthImg, 3], dtype=np.uint8)
            imgDisplayAnskey.fill(255)
            cv2.putText(imgDisplayAnskey, "ANSWER KEY", (250, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.line(imgDisplayAnskey, (250, 50), (450, 50), (255, 0, 0), 5)

            AnsKey = []
            for x in range(0, question):

                if myIndex[x] == 0:
                    AnsKey.append('A')
                elif myIndex[x] == 1:
                    AnsKey.append('B')
                elif myIndex[x] == 2:
                    AnsKey.append('C')
                elif myIndex[x] == 3:
                    AnsKey.append('D')
                elif myIndex[x] == 4:
                    AnsKey.append('E')

            print(AnsKey)
            Ansk = list(AnsKey)

            w = 80
            l = 90
            for c in range(0, question):
                if c + 1 < 10:
                    cv2.putText(imgDisplayAnskey, str(c + 1) + '.', (l, w), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
                    cv2.putText(imgDisplayAnskey, str(Ansk[c]), (l + 50, w), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0),
                                2)
                elif c + 1 > 30:
                    cv2.putText(imgDisplayAnskey, str(c + 1) + '.', (300, w - 800), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 0, 0), 2)
                    cv2.putText(imgDisplayAnskey, str(Ansk[c]), (300 + 60, w - 800), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 0, 0), 2)
                else:
                    cv2.putText(imgDisplayAnskey, str(c + 1) + '.', (l - 10, w), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 0, 0), 2)
                    cv2.putText(imgDisplayAnskey, str(Ansk[c]), (l + 50, w), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0),
                                2)

                w += 30

            print(w)
            cv2.imshow('', imgDisplayAnskey)
            # INSERT HERE THE DATABASE FOR ANSWERS

            # DISPLAYING GRADING
            imgResult = imgWarpColored.copy()
            imgResult = Improve.showAnswer(imgResult, myIndex, grading, ans, question, choices)
            imgRawDrawing = np.zeros_like(imgWarpColored)
            # imgRawDrawing = cv2.resize(imgRawDrawing,(200,1000))
            imgRawDrawing = Improve.showAnswer(imgRawDrawing, myIndex, grading, ans, question, choices)
            # imgRawDrawing = cv2.resize(imgRawDrawing,(700,1000))
            # cv2.imshow("imgRawDrawing",imgRawDrawing)
            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            # cv2.imshow("imgInvWarp",imgInvWarp)
            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade, "100%", (50, 100), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 0, 255), 3)
            invMatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)

            imgBlank = np.zeros_like(img)
            imageArray = ([img, imgGray, imgBlur, imgCanny],
                          [imgContours, imgBiggestContours, imgResult, imgFinal])
            imgStacked = Improve.stackImages(imageArray, 0.5)
        except:
            imgBlank = np.zeros_like(img)
            imageArray = ([img, imgGray, imgBlur, imgCanny],
                          [imgBlank, imgBlank, imgBlank, imgBlank])
            imgStacked = Improve.stackImages(imageArray, 0.5)

        cv2.imshow("Final Result",imgFinal)
        # cv2.imshow("Stacked Images",imgStacked)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # cv2.imwrite("Final Result.jpg",imgFinal)
            cv2.waitKey(300)


