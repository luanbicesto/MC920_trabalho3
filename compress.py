import skimage.io as io
import numpy as np
import sys

def adjustPixel(pixelIntensity):
  roundedIntensity = round(pixelIntensity)
  if roundedIntensity < 0:
    roundedIntensity = 0
  if roundedIntensity > 255:
    roundedIntensity = 255
    
  return roundedIntensity

def compressImage(k, image):
  svdPerChannel = []
  #computing the SVD to each channel
  for channel in range(3):
    U, s, V = np.linalg.svd(image[:,:,channel], full_matrices=True, compute_uv=True)
    svdPerChannel.append([U, s, V])
    
  compressedImage2 = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
  compressedImage = []
  for channel in range(3):
    U = svdPerChannel[channel][0]
    Ug = U[:, 0:k]
    S = svdPerChannel[channel][1]
    Stmp = np.diag(S)
    Sg = Stmp[0:k, 0:k]
    V = svdPerChannel[channel][2]
    #Vg = np.matrix.transpose(V[0:k, :])
    Vg = V[0:k, :]
    tmpProduct = np.dot(Ug, Sg)
    compressedImage.append(np.dot(tmpProduct, Vg))
  
  for channel in range(3):
    compressedImage2[..., channel] = [[adjustPixel(element) for element in elements] for elements in compressedImage[channel]]
    
  return compressedImage2

def getDestinationFolder(imageName, k):
  return '../compressedImages/' + imageName + '/' + imageName + '_' + str(k) + '.png'

def main(imageName):
  image = io.imread('../images/' + imageName + '.png')
  
  for k in range(512):
    k = k+1
    compressedImage = compressImage(k, image)
    io.imsave(getDestinationFolder(imageName, k), compressedImage)

args = sys.argv
main(args[1])
