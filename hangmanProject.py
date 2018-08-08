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

import operator
#Default words
words = ["running", "python", "infinite loops", "memory leak", "internship"]

#pause time in seconds.
pause = 0.75

#the name for the current playing mode (Single, 2, or Computer)
play_type = ""

#the number of guesses the computer let's a person/itself guess.
guess_setting = 9

player_1 = "Player 1"
player_2 = "Player 2"

rounds = 0
player1points = 0
player2points = 0

##########################################################################
# readFile takes a filename, attempts to open it and requests a different
# filename if the file is not found.
##########################################################################
def readDict(filename):
  
   #words is what we will be returning. So initialize it to be empty.
   words = []
   try:
      #Open the file!
      with open(filename, 'r') as files:
         #loop through each line in the file
         for line in files:
               words.append(line.lower()[0:len(line)-1])
   except:
      print ("ERROR: Dictionary not found! Please add a dictionary to the local directory.")

   return words
##########################################################################
# readFile takes a filename, attempts to open it and requests a different
# filename if the file is not found.
##########################################################################
def readFile(filename):
  
   #words is what we will be returning. So initialize it to be empty.
   words = []
   try:
      #Open the file!
      with open(filename, 'r') as files:
         #loop through each line in the file
         for line in files:
            #lowercase all the strings and split them between the spaces.
            for word in line.lower().split():
               #Remove a punctuation attached at the end of the word.
               if not word[len(word) -1].isalnum():
                  word = word[0:len(word) - 1]
               #append the word to the list.
               words.append(word)
   #if the file didn't open correctly, request another filename
   except:
      print ("ERROR: Incorrect Filename.\nPlease try again.")
      words = readFile(input("Enter filename: "))

   return words
#######################################################################   
# Setting updater will update the settings of the game
####################################################################
def setting_updater():

   #the global variables we will be changing.
   global words
   global play_type
   global guess_setting
   global player_1
   global player_2
   global player1points
   global player2points

   #while loop (keep trying until we break).
   while True:
      try:
         #if the try worked we will have an integer and break out
         guess_setting = int(input("\n\nIncorrect Guess Limit: ")) 
         break
      except:
         print("ERROR: Invalid input. Please enter a number.")
         continue
   sleep(pause)

   #next setting to change: Playing mode.
   while True:
      print("\nWhat version of Hangman would you like to play?")
      command = input("\n1 for 1 Player(1 solo practice round)\n2 for 2 Player(Human vs. Human)\nC for the Computer(Human vs. Computer): ").upper()
      sleep(pause)
      print

      #Single Player
      if(command == '1'):
         play_type = "single player"
         player_2 = "You"
         print ("Would you like to read in a file of words?")
         print ("\nEnter a fileName for Yes, N for No.")
         command = input()

         #if the user requested to read a file in, then
         #we will call the readfile function which
         #will the take the filename and read it into our global words list.
         if command.upper() != "N":
            words = readFile(command)
         play_hangman()
         break

      # 2 Player. Sets the play_type and calls play_hangman_multi
      elif(command == '2'):
         play_type = "2-player"
         play_hangman_multi()
         break

      # Computer! Sets the play_type and plays the computer.
      elif(command == 'C'):
         
         player1points = 0
         player2points = 0
         while True:
            try:
               rounds = int(input("\nHow many rounds would you like to play? "))
               break
            except:
               print("ERROR: Rounds must be a number! Try again.")
         player_1 = "computer"
         player_2 = "You"

         print("\nLoading...\n")
         words = readFile("dictionary.txt")

         for i in range(0, rounds):
            print ("Round: %d" % (i + 1))
            
            play_type = "2-player"
            play_computer()

            sleep(pause)  
            print("\n\nMy turn to challenge you.")
            sleep(pause)
            play_hangman()
            if i < rounds - 1:
               print("Your turn to challenge me again.")
               if(player1points > player2points):
                  print ("I am winning with " + str(player1points) + " points.")
                  print ("You are behind with " + str(player2points) + " points.")
               elif(player2points > player1points):
                  print ("You are winning with " + str(player2points) + " points.")
                  print ("I am behind with " + str(player1points) + " points.")
               else:
                  print ("It's currently a tie. We both have " + str(player1points) + " points.")
            else:
               if(player1points > player2points):
                  print ("I won with " + str(player1points) + " points.")
                  print ("You lost with " + str(player2points) + " points.")
               elif(player2points > player1points):
                  print ("I won with " + str(player2points) + " points.")
                  print ("You lost with " + str(player1points) + " points.")
               else:
                  print ("It ended in a tie. We both have " + str(player1points) + " points.")

            sleep(pause)
           
               
         play_type = "against the computer"
    

         
      
      #Invalid command. Alert the user and request again.
      else:
         print ("ERROR: Invalid Command\nPlease try again.")
         continue

   if(input("Play again(Y for Yes, Any key for No)? ").upper() == "Y"):
      print("\n")
      play_again()

#######################################################################
# play_computer uses a dictionary and letter frequency algorithms to
# guess the next best letter for a given word or phrase.
# Then it will show the user what it's trying to guess and keep guessing
# up until the guess_setting.
########################################################################
def play_computer():
   global player1points
   global player2points

   #Request the word or phrase from the user
   word = input("\nEnter a word or phrase to challenge the computer: ").upper()
   #Read in the dictionary.
   wordlist = readDict("dictionary.txt")
   dictionary = {}
   defaultletters = ["e", "t", "a", "o", "i", "n", "s", "r", "h", "l", "d", "c", "u",
                     "m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]

   letterstoguess = len(word)
   #Place each word in the dictionary/association array with a key(word length) and value(word).
   for words in wordlist:
      if(len(words) in dictionary.keys()):
         dictionary[len(words)].append(words)
      else:
         dictionary[len(words)] = [words]

   #set the number of guesses
   guessnum = guess_setting

   #sleep will slow down the program to make it more user friendly.
   sleep(pause)

   #tell how many guesses the computer will try to guess the word.
   print ("I have %d guesses to guess each letter in the word." % guessnum)
   
   #introduce the hangman word.
   sleep(pause)
   print ("Here is the Hangman word/phrase:")

   #guesses is the guesses the computer has done.
   guesses = []

   #make a list of words for the final result
   wordlist = word.lower().split()

   #The Number of words the computer has guessed, helps access the index for which word the computer is working on
   numwordsguessed = 0
   print("\n")
   #Let the games begin. Run while there are still guesses left!
   while guessnum > 0:
      #make a list of possible words (empty at the beginning)
      possiblewords = []

      #some checking to see which word we are currently working on...
      #start with the first word and continue until the end of the phrase.

      ##########STEP 1 : DETERMINE WORD TO WORK ON#########
      if len(wordlist) > numwordsguessed and wordlist[numwordsguessed] == word.split()[numwordsguessed] :
         numwordsguessed += 1
         continue
      elif(len(wordlist) == numwordsguessed):
         pass
      else:
         ##########STEP 2 : CREATE DICTIONARY AND NARROW DOWN#########
         try:
            for possibles in dictionary[len(word.split()[numwordsguessed])]:
               count = 0
               #seems like the system error is here somewhere....
               if word.split()[numwordsguessed].isupper() and len(guesses) == 0:
                  possiblewords = dictionary[len(wordlist[0])]
                  break
               else: 
                  for c in word.split()[numwordsguessed]:
                     if ((c.islower() and c != possibles[count])
                     or (possibles[count] in guesses and possibles[count] not in word.split()[numwordsguessed])):
                        break
                     elif(count == len(word.split()[numwordsguessed]) - 1):
                        possiblewords.append(possibles)
                     count += 1
         except:
            pass
  
       ##########STEP 3 : COUNT UP LETTERS#########
      lettercount = {}
      
      #count up the letters in the words
      for words in possiblewords:
         for c in words:
            if c not in lettercount.keys():
               lettercount[c] = 1
            else:
               lettercount[c] += 1
      
      #make letter count a list of letters sorted by most frequent to least frequent
      lettercount = sorted(lettercount.keys(), key = lettercount.get, reverse = True)

      
       ##########STEP 4 : GENERATE GUESS#########
      wordslefttoguess = len(word.split()) - numwordsguessed #APPROXIMATELY
      if (letterstoguess > 1 
          or len(possiblewords) < (guesses - wordslefttoguess)/wordslefttoguess):
         for guess in lettercount:
            if guess not in guesses:
               break
       # Only invalid guesses in lettercount
         else:
            for guess in defaultletters:
               if guess not in guesses:
                  break
      # Only 1 letter left, better to use default letters
      else:
         for guess in defaultletters:
               if guess not in guesses:
                  break
      letterstoguess = 0
      displayword = ""

       ##########STEP 5 : DISPLAY WORD, GUESS AND RESULTS#########
      # Here is where we prepare the display (with '_ ' for each letter not guessed)
      for i in range(0, len(word)):

        #For computer guessing, we used uppercase to lower case instead of the '@' symbol.
        #This made it easier to keep track of variables.
         if word[i].isupper():
            displayword += "_ "
            letterstoguess += 1
         
            #if the letter has been guessed, we print the letter and a space.
         elif word[i].islower():
            displayword += word[i] + " "

         #spaces = 2 spaces to make it more readable 
         elif(word[i] == " "):
            displayword += "  "
         else:
            displayword += word[i]
      ########PRINT THE DISPLAY
      #print our display
      print (displayword) 
      
      #if there were no more letters to guess then the game is over.
      #so break the loop
      if letterstoguess == 0:
         print ("\n\nI beat you! You lost!")
         player1points += 1
         break
      
      rand = randint(0,4)

      ########PRINT THE GUESS
      print("\n\nI'm thinking...")
      sleep(pause * 4)

      if len(possiblewords) < 10 and len(possiblewords) > 0:
         print("OH! I think I know what that word is now!!")
         sleep(pause * 1.5)
         print("Let's go with %s!" % guess)
      elif(rand == 1):
         print ("I'm gonna guess %s?" % guess)

      elif(rand == 2):
         print ("How about %s?" % guess)

      elif(rand == 3):
         print("I'll try the letter %s." % guess)

      else:
         print("Are there any %s's?" % guess)
      possiblewords = []
      sleep(pause * 2)
      ########PRINT RESULTS##########

      #CORRECT GUESS
      if guess.upper() in word:
         print ("%s was in the word/phrase!" % guess, flush = True)
         sleep(pause * 2)
         print("\n")
         guesses.append(guess)
         word = word.replace(guess.upper(), guess)

      #INCORRECT GUESS
      else: 
         print ("I guessed wrong!", flush = True)
         guessnum -= 1
         guesses.append(guess)
         sleep(pause)
         if(guessnum != 0):
            print ("But I have incorrect %d guesses left!" % guessnum, flush = True) 
            sleep(pause)
            print("\n")
   else:
      print ("\n\nI ran out of guesses! You won this round!")
      player2points += 1
   if(player1points > player2points):
      print("I am currently winning with %d points. You have %d points." %(player1points, player2points))
   elif(player2points > player1points):
      print("You are currently winning with %d points. I have %d points."% (player2points, player1points))
   else:
      print("We are tied with %d points" % player1points)

###########################################################################################
# play_hangman_multi takes a word or phrase from Player 1 and allows Player 2 to start
# guessing the letters in the word or phrase
##########################################################################################
def play_hangman_multi():
   while True:
      try:
         rounds = int(input("\nHow many rounds would you like to play? "))
         break
      except:
         continue
   global player_1
   global player_2
   global words
   global player1points
   global player2points
   sleep(pause)
   print("")
   player_1 = input("What's the name of player 1? ")
   player_2 = input("What's the name of player 2? ")
   for r in range(0, rounds * 2):
      if(r % 2 == 0):
         print ("Round: %d" % ((r + 2)/2))
      words.clear()
      words.append(input("\n%s, enter the word or phrase (make sure %s doesn't see): " % (player_1, player_2)))
      print("\n"*2000)
      play_hangman()
      player_1, player_2 = player_2, player_1
      player1points, player2points = player2points, player1points
      if (r < rounds * 2 - 1):
         if(player1points > player2points):
            print (player_1 + " is winning with " + str(player1points) + " points.")
            print (player_2 + " is behind with " + str(player2points) + " points.")
         elif(player2points > player1points):
            print (player_2 + " is winning with " + str(player2points) + " points.")
            print (player_1 + " is behind with " + str(player1points) + " points.")
         else:
            print ("It's currently a tie. You both have " + str(player1points) + " points.")
      else:
         if(player1points > player2points):
            print (player_1 + " won with " + str(player1points) + " points.")
            print (player_2 + " lost with " + str(player2points) + " points.")
         elif(player2points > player1points):
            print (player_2 + " won with " + str(player2points) + " points.")
            print (player_1 + " lost with " + str(player1points) + " points.")
         else:
            print ("It ended in a tie. You both have " + str(player1points) + " points.")


#######################################################################################
# Play again will determine if the user wants to change any settings before
# playing again. Then it will run the program again
#######################################################################################
def play_again():
   print("CURRENT SETTINGS:")
   if(play_type == "single player"):
      print("There are %d possible words which are chosen at random." % len(words))
   print("You are currently playing %s." % play_type)
   print("Incorrect Guess Limit: %d" % guess_setting)
   if play_type == "2-player":
      print("Player 1 (challenger): %s" % player_1)
      print("Player 2 (guesser): %s" % player_2)

   while True:
      command = input("\nWould you like to change these settings(y or n)? ").upper()
      if command == 'Y':
         setting_updater()
      elif command == 'N':
         if(play_type == "2-player"):
            play_hangman_multi()
         elif(play_type == "single player"):
            play_hangman()
         else:
            play_computer()
      else:
         print("ERROR: Invalid command.\nPlease try again.")

#################################################################
# Play Hangman runs the game after the correct files have been 
# read in. Will run recursively until the user wants to exit.
#################################################################
def play_hangman():

   global player1points
   global player2points
   #Choose a random word in our list
   word = words[randint(0, len(words) - 1)].lower()
   
   #make a copy of the word that we can manipulate as the game plays on.
   wordcopy = word
   
   #set the number of guesses
   guessnum = guess_setting

   #sleep will slow down the program to make it more user friendly.
   sleep(pause)

   if play_type == "2-player":
      print ("%s, you have %d guesses to guess each letter in the word or phrase." % (player_2, guessnum))
   else:
      print ("You have %d guesses to guess each letter in the word or phrase." % guessnum)
   
   #introduce the hangman word.
   sleep(pause)
   print ("Here is the Hangman word/phrase:")
   
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
         if wordcopy[i].isalpha():
            displayword += "_ "
            letterstoguess += 1
         
            #if the letter has been guessed, we print the letter and a space.
         elif wordcopy[i] == "@":
            displayword += word[i] + " "

         #spaces = 2 spaces to make it more readable 
         elif(wordcopy[i] == " "):
            displayword += "  "
         else:
            displayword += word[i] + " "

      #print our display
      print (displayword) 
      
      #if there were no more letters to guess then the game is over.
      #so break the loop
      if letterstoguess == 0:
         if play_type == "single player":
            print ("\n\nCongratulations! You won!")
         elif play_type == "2-player":
            print ("\n\n%s won! Better luck next time %s." % (player_2, player_1))
            player2points += 1
            break

      #guess a letter and add to guesses.
      sleep(pause)
      guess = input("\n\nPlease enter a letter to guess: ").lower()
      sleep(pause)

      #guess must be only one letter!
      if len(guess) < 2:
         #if the user guessed a letter in the word.
         if guess in word and guess not in guesses:
            wordcopy = wordcopy.replace(guess, "@")
            print("%s was in the word/phrase!" % guess, flush = True)
      
         #if the user guessed the same letter twice (guess count not changed)
         elif guess in guesses:
            print ("Try again. You already guessed that.", flush = True)
      
         #the user guessed a letter that wasn't in the word.
         else: 
            print ("Sorry. %s was not in the word/phrase." % guess, flush = True)
            guessnum -= 1
            sleep(pause)
            print ("%d incorrect guesses left!" % guessnum, flush = True) 
      
      #the guess was not a single letter!
      else:
          print ("Try again. You cannot guess more than one letter.", flush = True)
      
      #add to the list of guesses
      guesses.append(guess)
      sleep(pause)
   #if the while loop exits normally, then display the lost message.
   else:
      print ("\n\n%s lost! Mr. Hangman is dead. The word/phrase was %s" % (player_2, word)) 
      player1points += 1
  

######################################################################
# Main is where the program will start. It will call welcome (which
# will welcome the user and read in the word file. Then it will call
# Play Hangman which will run the game until the user is done
######################################################################
def main():
   #welcome is used to welcome the user, get the settings, and open the file
   print ("Welcome to Python Hangman!")
   print ("Before we begin, let's configure the settings of the game:")
   setting_updater()

   

main()








