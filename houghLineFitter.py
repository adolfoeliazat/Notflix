import cv2
import numpy as np
import math
from functools import reduce

DEBUG = False

MASK_THRESHOLD_MINIMUM = 200
MASK_THRESHOLD_MAXIMUM = 255

LINE_ANGLE = 0.25 * np.pi
LINE_MIN_VOTES = 2500

NUMBER_OF_SAMPLES = 60

def fitHoughLine(path="similaritymatrix.png"):
    """
    Step 3: Using the similarity matrix as an input, we threshold the matrix to a 
    black/white mask, and then apply a probibalistic approach to drawn a Hough line.
    This line hopefully fits the biggest diagonal in the matrix, which should be the intro.

    Output: Best fit line, in the form [x1, y1, x2, y2]
    """

    similaritymatrixImg = cv2.imread(path)
    grayscaledImg = cv2.cvtColor(similaritymatrixImg,cv2.COLOR_BGR2GRAY)


    # Threshold will return a black/white image
    ret, thresholdImg = cv2.threshold(grayscaledImg, MASK_THRESHOLD_MINIMUM, MASK_THRESHOLD_MAXIMUM, cv2.THRESH_BINARY)

    lines = cv2.HoughLinesP(thresholdImg, 1, LINE_ANGLE, LINE_MIN_VOTES)
    unpackedLines = map(lambda line: line[0], lines)
    angledLines = filter(lambda line: math.fabs((line[2] - line[0]) - (line[3] - line[1])) < 2, unpackedLines)
    bestLines = sorted(angledLines, key=lambda line: math.sqrt((line[2] - line[0])**2 + (line[3] - line[1])**2), reverse=True)
    candidateLine = reduce(lambda bestLine, newLine: [min((bestLine[0], newLine[0])), min((bestLine[1], newLine[1])), max((bestLine[2], newLine[2])), max((bestLine[3], newLine[3]))], bestLines[:NUMBER_OF_SAMPLES], bestLines[0])

    if DEBUG:
        print(candidateLine)
        for (x1, y1, x2, y2) in bestLines:
            cv2.line(similaritymatrixImg,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.line(similaritymatrixImg,(candidateLine[0], candidateLine[1]),(candidateLine[2],candidateLine[3]),(255,0,0), 3)

        cv2.imwrite('tresholdimg.jpg',thresholdImg)
        cv2.imwrite('houghlines.jpg', similaritymatrixImg)

    # Return the best fitting line
    return candidateLine


if __name__ == "__main__":
    print(fitHoughLine())