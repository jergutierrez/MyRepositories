#  Title: image_encrypt_hide.py
#  Abstract: This program will take an .jpg image file, .txt file, cipher the .txt file with a 4-digit pin, and
#            hide the text file in the .jpg image. This program will also convert the file back to its original decrypted text file.
#  Author: Jeremy Gutierrez
#  ID: 001045927
#  Date: 02/10/2015
#  Test Input: image.jpg, Pin: 1978 and information.txt for encryption. image.jpg, secretImage.jpg, Pin:1978 for decryption.
#  Test Output: secretImage.jpg for encryption. decryptedText.txt for decryption.
#

import os, sys, difflib, shutil
from string import lowercase, uppercase
from javax.swing import *
from javax.swing import JButton, JFrame

def main(): # This will ask the user what they would like to do.
    choice = requestNumber("Welcome, Please Select\n    1. Encrypt\n    2. Decrypt\n    3. Exit\nYour Choice:") #Request user make choice
    if choice == 1: # Run Encrypt Instructions
      encryptInstructions()

    elif choice == 2: # Run Decrypt Instructions
      decryptInstructions()

    else: # Exit if other then selections available
      os._exit()

def encryptInstructions(): ##encrypt_Instructions(event=None): # Instructions for the encrypt button
  showInformation("Please, select the .jpg image you would like to use.")
  imageFile = pickAFile() # Will ask the user to select an image
  result = encrypt()      # Will ask the user for text file and will encrypt it
  hideFile(result, imageFile) #Will write the image and encrypted file to a new file
  return 0

def encrypt(): # Will encrypt the file
    key = 0
    while(key < 999 or key > 10000):
      key = requestInteger("Please enter a 4-Digit Pin:")
    else:
      showInformation("Please select a .txt file to encrypt and hide")
      textFile=open(pickAFile()) # Select text file to hide
      text=textFile.read() # read file into memory
      result = [] # This is for the final text
      for c in text: # will apply ceasar cipher
        if c in lowercase:
            idx = lowercase.index(c)
            idx = (idx + key) % 26
            result.append(lowercase[idx])
        elif c in uppercase:
            idx = uppercase.index(c)
            idx = (idx + key) % 26
            result.append(uppercase[idx])
        else:
            result.append(c)
    return "".join(result) # return final text

def hideFile(result, imageFile): # Will hide the encrypted text in the image file
    secretImage = file("c:\secretImage.jpg", "wb") #new file to be created
    secretImage.write(file(imageFile, "rb").read()) #will add image to new file
    secretImage.write(result) #will add text to the file
    secretImage.close()
    showInformation("The program has completed.\n The new image has been saved to:\n C:\secretImage.jpg")
    return 0

def decryptInstructions(): # Instructions for the decrypt button
    encoded = seperateFile() # Will seperate the image and hidden file and return encoded text
    decryptedText = decrypt(encoded) # Will decrypt the file and return the unencrypted tex
    decodedFile(decryptedText) # Will take the unencoded text and write it to a new file
    return 0

def seperateFile(): # Will seperate the hidden file from image file into a temp file
    showInformation("Please, select the original .jpg image file.\n")
    originalFileName = pickAFile() # Select 1st image to compare
    showInformation("Please, select the .jpg image file to decrypt.\n")
    secretFileName = pickAFile() # Select 2nd File
    originalFile = open(originalFileName, "r").read().split('\n') # Open & load the files for comparisson
    secretFile = open(secretFileName, "r").read().split('\n')
    encoded = ' '.join([comm for comm in secretFile if not (comm in originalFile)]) #This will compare the files and seperate the hidden File
    return encoded

def decrypt(encoded): # Will decrypt the text file
    key = 0
    while(key < 999 or key > 10000): #checks to see if pin # is in range
      key = requestInteger("Please enter a 4-Digit Pin:")
    else:
      text = encoded
      result = [] # for the unencoded text
      for c in text: # Will reverse the Ceasar cipher
        if c in lowercase:
            idx = lowercase.index(c)
            idx = (idx - key) % 26
            result.append(lowercase[idx])
        elif c in uppercase:
            idx = uppercase.index(c)
            idx = (idx - key) % 26
            result.append(uppercase[idx])
        else:
            result.append(c)
    return "".join(result) # returns the results

def decodedFile(decryptedText): # This will take the unencoded text and write it to a file
    decodedFile = file("c:\unencodedText.txt", "wb") # Creates a new file foe the unencoded text
    decodedFile.write(decryptedText) #will add text to the file
    decodedFile.close() # will close the file
    showInformation("The program has completed.\n The decrypted text has been saved to:\n C:\unencodedText.txt")
    return 0

main()