import numpy as np
import cv2 as oc

Image = oc.imread('Image3.jpeg', oc.IMREAD_COLOR) # first read image
ImageGreyScale = oc.cvtColor(Image, oc.COLOR_BGR2GRAY) # then coverted it to grayscale
_, ImageThreshold = oc.threshold(ImageGreyScale, 220, 255, oc.THRESH_BINARY) # then applay the threshold
ImageContours, hry = oc.findContours(ImageThreshold, oc.RETR_TREE, oc.CHAIN_APPROX_SIMPLE) # after that, i used the find counters function to get counters and hierarchy

# ----------------------------------------------------

def findNumberOfEdges(contourr):
    app = oc.approxPolyDP(contourr, 0.035 * oc.arcLength(contourr, True), True)
    numberofEdges = len(app)
    return numberofEdges

# ----------------------------------------------------

def findNumberOfNeighbors(i):
    funcNumberOfNeighbors = 0
    funcSon = hry[0][i][2]
    funcGrandKid = np.intc(hry[0][funcSon][2])
    funcNext = funcGrandKid
    while True:
        funcNext = np.intc(hry[0][funcNext][0])
        if funcNext == -1:
            break
        else:
            if oc.contourArea(ImageContours[funcNext]) > 100:
                funcNumberOfNeighbors += 1
    return funcNumberOfNeighbors

# ----------------------------------------------------

def findNumberOfApprovedShapes():
    numberOfShapes = 0
    for contour in ImageContours:
        if oc.contourArea(contour) >= 110:
            numberOfShapes += 1
        else:
            continue
    return numberOfShapes
# ----------------------------------------------------
# make names global
names = ["" for y in range(findNumberOfApprovedShapes())]

# ----------------------------------------------------

def identifyShapes(choice):
    if choice == 1:
        index = -1
        approvedShapeIndex = 0

        for contour in ImageContours:
            index = index + 1
            parent = np.intc(hry[0][index][3])

            if oc.contourArea(contour) < 110 or parent != 0:
                continue
            else:
                son = hry[0][index][2]

                numberOfEdges = findNumberOfEdges(contour)
                numberOfNeighbors = findNumberOfNeighbors(index)
                if numberOfEdges > 5:
                    app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour,True), True)
                    approxCircle = oc.approxPolyDP(contour, 0.01 * oc.arcLength(contour, True), True)
                    if son != -1:
                        if len(approxCircle) > 10:
                            if numberOfNeighbors <= 2:
                                names[approvedShapeIndex] = "CIRCLE"
                                app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                                xAxis, yAxis = app[0][0]
                                oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                            else:
                                names[approvedShapeIndex] = "FACE"
                                app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                                xAxis, yAxis = app[0][0]
                                oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                    else:
                        names[approvedShapeIndex] = "CURVE"
                        app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                elif numberOfEdges < 3:
                    names[approvedShapeIndex] = "LINE"
                    app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                    xAxis, yAxis = app[0][0]
                    oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                elif numberOfEdges == 3:
                    names[approvedShapeIndex] = "TRIANGLE"
                    app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                    xAxis, yAxis = app[0][0]
                    oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                elif numberOfEdges == 4:

                    app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                    (x, y, w, h) = oc.boundingRect(app)
                    per = w / float(h)
                    if son != -1:
                        if numberOfNeighbors <= 2:
                            if oc.contourArea(contour) > 500:
                                if 0.95 <= per <= 1.05:
                                    names[approvedShapeIndex] = "SQUARE"
                                else:
                                    names[approvedShapeIndex] = "RECTANGLE"
                                xAxis, yAxis = app[0][0]
                                oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                        else:
                            names[approvedShapeIndex] = "FACE"
                            xAxis, yAxis = app[0][0]
                            oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                    else:
                        names[approvedShapeIndex] = "CURVE"
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                else:
                    names[approvedShapeIndex] = "CURVE"
                    app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                    xAxis, yAxis = app[0][0]
                    oc.putText(Image, names[approvedShapeIndex], (xAxis, yAxis - 5), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)

                approvedShapeIndex += 1
    elif choice == -1:
        index = -1
        for o in range(findNumberOfApprovedShapes()):
            names[o] = ""
        approvedShapeIndex = 0

        for contour in ImageContours:
            index += 1
            parent = np.intc(hry[0][index][3])
            gf = np.intc(hry[0][parent][3])
            if oc.contourArea(contour) < 110 or gf <= 0:
                continue
            else:
                son = np.intc(hry[0][index][2])
                ggp = np.intc(hry[0][gf][3])
                numberOfEdges = findNumberOfEdges(contour)
                if numberOfEdges == 3:
                    if son != -1 and hry[0][son][2] == -1:
                        names[approvedShapeIndex] = "NOSE"
                        app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis - 3, yAxis + 8), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                elif numberOfEdges < 3:
                    if son == -1:
                        names[approvedShapeIndex] = "MOUTH"
                        app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis - 3, yAxis - 8), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                elif numberOfEdges == 4:
                    app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                    (x, y, w, h) = oc.boundingRect(app)
                    per = w / float(h)
                    if oc.contourArea(contour) > 500:
                        if 0.95 <= per <= 1.05:
                            names[approvedShapeIndex] = "Square"
                        else:
                            names[approvedShapeIndex] = "Rectangle"
                        app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis - 3, yAxis - 8), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                    else:
                        names[approvedShapeIndex] = "MOUTH"
                        app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis - 3, yAxis - 8), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)

                elif numberOfEdges > 5:
                    approxCircle = oc.approxPolyDP(contour, 0.01 * oc.arcLength(contour, True), True)
                    if len(approxCircle) > 9:
                        if son != -1 and ggp == 0 and oc.contourArea(contour) > 1200:
                            names[approvedShapeIndex] = "EYE"
                        elif son != -1 and ggp == 0 and 1000 < oc.contourArea(contour) < 1200:
                            names[approvedShapeIndex] = "MOUTH"
                        elif son != -1 and ggp == 0:
                            names[approvedShapeIndex] = "EYE"
                        elif son == -1 and ggp == 0:
                            names[approvedShapeIndex] = "EYE"
                        app = oc.approxPolyDP(contour, 0.035 * oc.arcLength(contour, True), True)
                        xAxis, yAxis = app[0][0]
                        oc.putText(Image, names[approvedShapeIndex], (xAxis - 3, yAxis - 8), oc.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 1)
                approvedShapeIndex = approvedShapeIndex + 1
# ----------------------------------------------------
def doProcessing():
    identifyShapes(1)
    identifyShapes(-1)
# ----------------------------------------------------
def revealFinalImage():
    oc.imshow('img', Image)
    oc.waitKey(0)
    oc.destroyAllWindows()
# ----------------------------------------------------
doProcessing()
revealFinalImage()

print("Tala Hamad 11924518 - Image Processing assignment #2")


