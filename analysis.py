import skimage.io as io
import matplotlib.pyplot as plt
import math
import os
import sys

def getImagesFolder(imageName):
  return '../compressedImages/' + imageName + '/'

def getImageName(originalImageName, k):
  return originalImageName + '_' + str(k) + '.png'

def getOriginalImagePath(originalImageName):
  return '../images/' + originalImageName + '.png'

def readOriginalImage(originalImageName):
  path = getOriginalImagePath(originalImageName)
  return io.imread(path)

def rmse(originalImage, kImage):
  totalDifferenceChannel = [0,0,0]
  M = kImage.shape[0]
  N = kImage.shape[1]
  for channel in range(3):
    for m in range(M):
      for n in range(N):
        totalDifferenceChannel[channel] = totalDifferenceChannel[channel] + pow(int(originalImage[m][n][channel]) - int(kImage[m][n][channel]), 2)
  
  rmseChannel = [0.0, 0.0, 0.0]
  for channel in range(3):
    rmseChannel[channel] = math.sqrt(totalDifferenceChannel[channel] / float(M*N))
  
  averageChannels = (rmseChannel[0] + rmseChannel[1] + rmseChannel[2]) / float(3)  
  return round(averageChannels, 3)

def compressionTax(originalImageName, k, originalSize):
  kImagePath = getImagesFolder(originalImageName) + getImageName(originalImageName, k)
  kImageSize = os.path.getsize(kImagePath)
  return kImageSize / float(originalSize)

def getGraphsPath(originalImageName):
  return '../graphs/' + originalImageName + '/'

def saveGraphAllMetrics(xAxis, yAxisRMSE, yAxisCompressionTax, originalImageName):
  fig = plt.figure()
  plt.plot(xAxis, yAxisRMSE)
  plt.plot(xAxis, yAxisCompressionTax)
  plt.xlabel('K')
  #plt.ylabel('block difference')
  plt.legend(['RMSE', 'CompressionTax'], loc='upper right')
  #plt.legend(['RMSE'], loc='upper right')
  fig.savefig(getGraphsPath(originalImageName) + 'allMetrics.png')
  
def saveGraphRMSE(xAxis, yAxisRMSE, originalImageName):
  fig = plt.figure()
  plt.plot(xAxis, yAxisRMSE)
  plt.xlabel('K')
  plt.legend(['RMSE'], loc='upper right')
  fig.savefig(getGraphsPath(originalImageName) + 'rmse.png')
  
def saveGraphCompressionTax(xAxis, yAxisCompressionTax, originalImageName):
  fig = plt.figure()
  plt.plot(xAxis, yAxisCompressionTax)
  plt.xlabel('K')
  plt.legend(['CompressionTax'], loc='lower right')
  fig.savefig(getGraphsPath(originalImageName) + 'CompressionTax.png')
  
def main(originalImageName):
  xAxis = []
  yAxisRMSE = []
  yAxisCompressionTax = []
  numberImages = 512
  imagesFolder = getImagesFolder(originalImageName)
  originalImage = readOriginalImage(originalImageName)
  originalImageSize = os.path.getsize(getOriginalImagePath(originalImageName))
  
  for k in range(numberImages):
    k = k + 1
    kImage = io.imread(imagesFolder + getImageName(originalImageName, k))
    rmseValue = rmse(originalImage, kImage)
    compressionTaxValue = compressionTax(originalImageName, k, originalImageSize)
    xAxis.append(k)
    yAxisRMSE.append(rmseValue)
    yAxisCompressionTax.append(compressionTaxValue)
    
  saveGraphAllMetrics(xAxis, yAxisRMSE, yAxisCompressionTax, originalImageName)
  saveGraphRMSE(xAxis, yAxisRMSE, originalImageName)
  saveGraphCompressionTax(xAxis, yAxisCompressionTax, originalImageName)
    
args = sys.argv
main(args[1])
