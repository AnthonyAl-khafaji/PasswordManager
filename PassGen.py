import string
import random

class GenPassWord():
    def __init__ (self, numOfChunks = 3, excludedChar = ""):
        self.numOfChunks = numOfChunks
        self.excludedChar = excludedChar

    def makePassword(self, length: int):
        password = ""
        lengthOfChunk = round(length/self.numOfChunks)
        patternForOdd = string.ascii_uppercase + string.digits + string.ascii_lowercase 
        patternForEven = patternForOdd + string.punctuation
        #print (patternForEven)
        for i in range (self.numOfChunks):
            #chunk += 1
            if (i  % 2) > 0:
                pattern = patternForOdd
            else:
                pattern = patternForEven
            
            password += self.passwordChunk(pattern, lengthOfChunk) + '-'
        if len(password) >= length:
            password = password[:length]
        return password

    def passwordChunk(self, chunkPattern: str, LengthOfChunk: int):
        filterPattern = ''.join(c for c in chunkPattern if c not in self.excludedChar)
        LengthOfChunk = int(LengthOfChunk)
        return ''.join(random.choices(filterPattern, k=LengthOfChunk))