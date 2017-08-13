#runs rotation encrytion schemes on a user supplied string using positive character value increases 
# e.g. rot1 for a -> b

#requests input from the user for a string to be examined
encrypted = raw_input("Please enter your encoded string: ")
#constant for the length of the alphabet
ALPHABET_LENGTH = 26

#does a single rotation for a character
def rotation(character, lowerBound, upperBound):
    rotated = ord(character) + i          
    #check if the character jumps out of the bounds of its alphabet
    if rotated > ord(upperBound):
        rotated = rotated - ord(upperBound) + ord(lowerBound) - 1
    correctRotation = rotated
    return chr(correctRotation)

#tries to rotate the characters with all the possibilities between 1 and 25
for i in range (0, ALPHABET_LENGTH):
    #change each character in the string to the rotated character
    decrypted = "Rotation " + str(i) + ": "
    for character in encrypted:
        rotated = character
        #checks if the character is between A and z, otherwise leaves it untouched
        if character <= 'z' and character >= 'a':
            rotated = rotation(character, 'a', 'z')
        elif character <= 'Z' and character >= 'A':
            rotated = rotation(character, 'A', 'Z')
        decrypted += rotated
    print(decrypted)

