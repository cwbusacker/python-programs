####################################################################################
# Title: Python Hangman
# Author: Chase Busacker
# Time Estimate: 3 hours
#
# This is my personal hangman project. It allows 9 guesses for a user to guess the
# letters in a word. If the user fails, it tells them that they lost and tells them
# the result. The program has the option to read words from a .txt file or use the 
# default words list. After teaching myself python (using online tutorials), this 
# was my very first personal python project.
# 
###################################################################################
#Need random in order to select a random word.
from random import randint

#import sleep to slow down the program (makes the program more usable)
from time import sleep

#Default words
words = ["running", "python", "infinite loops", "memory leak", "internship"]

#pause time in seconds.
pause = 0.75



#reads the file
def readFile(filename):
   global words
   with open(filename, 'r') as files:
      for line in files:
         for word in line.split():
            if len(word) > 6:
               words.append(word)
#######################################################################   
# Welcome will introduce the hangman game the first time it is run
# and determine where the user wants to get the words from.
####################################################################
def welcome():
   print ("Welcome to Python Hangman!")
   print ("Would you like to read in a file of words?")
   print ("Enter a fileName for Yes, N for No.")
   command = input()

   #if the user requested to read a file in, then
   #we will call the readfile function which
   #will the take the filename and read it into our list.
   if command.upper() != "N":
      readFile(command)

#################################################################
# Play Hangman runs the game after the correct files have been 
# read in. Will run recursively until the user wants to exit.
#################################################################
def play_hangman():
   #Choose a random word in our list
   word = words[randint(0, len(words) - 1)].lower()
   
   #make a copy of the word that we can manipulate as the game plays on.
   wordcopy = word
   
   #set the number of guesses
   guessnum = 9

   #sleep will slow down the program to make it more user friendly.
   sleep(pause)
   print ("You have %d guesses to guess each letter in the word." % guessnum)
   
   #introduce the hangman word.
   sleep(pause)
   print ("Here is the Hangman word:")
   
   #set the guesses list to empty.
   guesses = []

   #Let the games begin. Run while there are still guesses left!
   while guessnum > 0:
      
      #print a new line each time to organize the screen better.
      print ("\n")

      #reset letters to guess to zero and create the display word
      letterstoguess = 0
      displayword = ""

      # Here is where we prepare the display (with '_ ' for each letter not guessed)
      for i in range(0, len(word)):

         #if the char is alphanumeric, that means that the letter has not been guessed so
         #we print '_ ' and add one to the letters not guessed.
         if wordcopy[i].isalnum():
            displayword += "_ "
            letterstoguess += 1
         
            #if the letter has been guessed, we print the letter and a space.
         elif wordcopy[i] == "@":
            displayword += word[i] + " "

         #otherwise, we have punctuation. just print punctuation.
         else:
            displayword += word[i]

      #print our display
      print (displayword) 
      
      #if there were no more letters to guess then the game is over.
      #so break the loop
      if letterstoguess == 0:
         print ("Congratulations! You won!")
         break
      
      #guess a letter and add to guesses.
      sleep(pause)
      guess = input("Please enter a letter to guess: ")
      sleep(pause)

      #guess must be only one letter!
      if len(guess) < 2:
         #if the user guessed a letter in the word.
         if guess in word and guess not in guesses:
            wordcopy = wordcopy.replace(guess, "@")
            print("%s was in the word!" % guess, flush = True)
      
         #if the user guessed the same letter twice (guess count not changed)
         elif guess in guesses:
            print ("Try again. You already guessed that.", flush = True)
      
         #the user guessed a letter that wasn't in the word.
         else: 
            print ("Sorry. %s was not in the word." % guess, flush = True)
            guessnum -= 1
            sleep(pause)
            print ("%d guesses left!" % guessnum, flush = True) 
      
      #the guess was not a single letter!
      else:
          print ("Try again. You cannot guess more than one letter.", flush = True)
      
      #add to the list of guesses
      guesses.append(guess)
      sleep(pause)
   #if the while loop exits normally, then display the lost message.
   else:
      print ("You lost! Mr. Hangman is dead. The word was %s" % word) 
   
   #if the user wants to play again, then recursively call play_hangman again.
   if(input("Play_again(Y for Yes)?").upper() == "Y"):
      print("\n")
      play_hangman()

######################################################################
# Main is where the program will start. It will call welcome (which
# will welcome the user and read in the word file. Then it will call
# Play Hangman which will run the game until the user is done
######################################################################
def main():
   #welcome is used to welcome the user and open the file
   welcome()
   print("\n")

   #play_hangman is where all the fun happens.
   play_hangman()
   

main()








