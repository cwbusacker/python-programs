####################################################################################
# Title: Python Hangman
# Author: Chase Busacker
# Time Estimate: 10 hours
#
# This is my personal hangman project. It can be played in a variety of ways:
# one "practice" round, a number(specified) of rounds verses a computer,
# or a number(specified) of rounds human against human.
#
# After all the settings have been specified, the program will allow a number(specified)
# of guesses to allow the user or computer to guess. Whoever wins will gain a point
# and the other person will start their turn.
###################################################################################
#Import sleep to slow down the program and randint for choosing random words.
from random import randint
from time import sleep
from os import system, name
import getpass

#Define the player class
class player(object):
   def __init__(self, name, points):
      self.name = name
      self.points = points

#UNIVERSAL OBJECTS
words = ["cat", "dog", "chicken", "rooster", "cow", "hen", "pig", "hamster", "guinea pig"] #Default words if the user doesn't read in a file.
pause = 0.75 #pause time in seconds will be multiplied in som
play_type = "" #the name for the current playing mode (Single, 2, or Computer)
guess_setting = 10 #the number of guesses the computer let's a person/itself guess. Will be changed in settings.

#The two players. Names will be changed when game begins.
player_1 = player("Player 1", 0)
player_2 = player("Player 2", 0)

##########################################################################
# readDict takes a filename which is usually dictionary.txt and reads
# it into words line by line.
##########################################################################
def readDict(filename):
   #words is what we will be returning. So initialize it to be empty.
   words = []
   try:
      #Open the file
      with open(filename, 'r') as files:
         #loop through each line in the file and append it to the words list.
         for line in files:
               words.append(str(line).lower())
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

   #Change the Game mode.
   while True:
      print("\nWhat version of Hangman would you like to play?")
      command = input("\n1 for 1 Player(1 solo practice round)\n2 for 2 Player(Human vs. Human)\nC for the Computer(Human vs. Computer): ").upper()
      sleep(pause)
      print

      #Only want to get the guess number if we have a valid command.
      if command == 'C' or command == '1' or command == '2':
         #Loop until we have a valid guess number.
         while True:
            try:
               #if the try worked we will have an integer and break out
               guess_setting = int(input("\nIncorrect Guess Limit: "))
               break
            except:
               print("ERROR: Invalid input. Please enter a number.")
               continue
         break
      #Invalid command given (Not 1, 2, 3). Alert the user and request again.
      else:
         print ("ERROR: Invalid Command\nPlease try again.")
         continue

   
      sleep(pause)

      #Single Player
   if(command == '1'):
      play_type = "single player"
      player_2.name = "You"
      print ("Would you like to read in a file of words?")
      print ("\nEnter a fileName for Yes, N for No.")
      command = input()

      #if the user requested to read a file in, then
      #we will call the readfile function which
      #will the take the filename and read it into our global words list.
      if command.upper() != "N":
         words = readFile(command)
      play_hangman()
  
   # 2 Player. Sets the play_type and calls play_hangman_multi
   elif(command == '2'):
      play_type = "2-player"
      play_hangman_multi()
  
   # Computer! Sets the play_type and plays the computer.
   elif(command == 'C'):

      #setup the settings of the game
      play_type = "against the computer"
      player_1.name = "computer"
      player_1.points = 0
      player_2.name = "You"
      player_2.points = 0

      #this is here because we only want to call it once and play_computer gets called
      #multiple times since there are multiple rounds.
      while True:
         try:
            rounds = int(input("\nHow many rounds would you like to play? "))
            break
         except:
            print("ERROR: Rounds must be a number! Try again.")
         
         #Load the dictionary before we begin.
      print("\nLoading...\n")
      words = readDict("dictionary.txt")

         #Loop the amount of rounds
      for i in range(0, rounds):
         print ("Round: %d" % (i + 1))

         #play the computer
         play_computer()
         sleep(pause)  

         #Computer challenge the user
         print("\n\nMy turn to challenge you.")
         sleep(pause)
         play_hangman()

         #Display who is winning and repeat
         if i < rounds - 1:
            print("Your turn to challenge me again.")
            if(player_1.points > player_2.points):
               print ("I am winning with " + str(player_1.points) + " points.")
               print ("You are behind with " + str(player_2.points) + " points.")
            elif(player_2.points > player_1.points):
               print ("You are winning with " + str(player_2.points) + " points.")
               print ("I am behind with " + str(player_1.points) + " points.")
            else:
               print ("It's currently a tie. We both have " + str(player_1.points) + " points.")
         
         #display the final results.
      print("\n\nGame Over\nHere are the results:\n")
      if(player_1.points > player_2.points):
         print ("I won with " + str(player_1.points) + " points.")
         print ("You lost with " + str(player_2.points) + " points.")
      elif(player_2.points > player_1.points):
         print ("I won with " + str(player_2.points) + " points.")
         print ("You lost with " + str(player_1.points) + " points.")
      else:
         print ("It ended in a tie. We both have " + str(player_1.points) + " points.")

      sleep(pause)
      
      

   if(input("\n\nPlay again(Y for Yes, Any key for No)? ").upper() == "Y"):
      print("\n")
      play_again()

#######################################################################
# play_computer uses a dictionary and letter frequency algorithms to
# guess the next best letter for a given word or phrase.
# Then it will show the user what it's trying to guess and keep guessing
# up until the guess_setting.
########################################################################
def play_computer():
   global player_1
   global player_2
   #Request the word or phrase from the user
   word = input("\nEnter a word or phrase to challenge the computer: ").upper()

   #wordlist = words because words is currently our dictionary.
   wordlist = readDict("dictionary.txt")
   dictionary = {}

   #Letters in the order of most to least common.
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

      ##########STEP 1 : DETERMINE WORD TO WORK ON#########
      #The length of numwordsguessed is smaller than the index AND the word at the index islower AKA has been guessed
      if len(wordlist) > numwordsguessed and word.split()[numwordsguessed].islower() :
         numwordsguessed += 1
         continue
      elif(len(wordlist) == numwordsguessed):
         pass
      else:
         #if changing words isn't necessary then we will continue narrowing down until
         ##########STEP 2 : CREATE DICTIONARY AND NARROW DOWN#########
         #try just in case the dictionary is empty.
         try:
            for possibles in dictionary[len(word.split()[numwordsguessed])]:
               count = 0

               #if we haven't guessed a single letter yet then the possible words are any word that's the same length.
               if len(guesses) == 0:
                  possiblewords = dictionary[len(wordlist[0])]
                  break

               else: #no guesses have occured so include ONLY words that are the same length
                     #lack letters that have been guessed incorrectly, and contain letters
                     #in the same spot if guessed correctly.
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
      #if there is more than one letter to guess or are only a 
      #couple of possible words left then we will find the next best guess.
      #For loops used to find the 
      if (letterstoguess > 1 
          or len(possiblewords) < 3) and len(possiblewords) > 0:
         for guess in lettercount:
            if guess not in guesses:
               break
      # Only 1 letter left, better to use default letters
      else:
         for guess in defaultletters:
               if guess not in guesses:
                  break
      

       ##########STEP 5 : DISPLAY WORD, GUESS AND RESULTS#########
      # Here is where we prepare the display (with '_ ' for each letter not guessed)
      letterstoguess = 0 #A count of unguessed letters
      displayword = "" #eventually the final display word
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

         #It must be a number or symbol. We display these for free.
         else:
            displayword += word[i]
      ########PRINT THE DISPLAY
      #print our display
      print (displayword) 
      
      #if there were no more letters to guess then the game is over.
      #so break the loop
      if letterstoguess == 0:
         print ("\n\nI beat you! You lost!")
         player_1.points += 1
         break
      
      rand = randint(0,4)

      ########PRINT THE GUESS Let the computer "THINK"
      #Allows some time between guesses so the user can 
      #actually see what is going on.
      print("\n\nI'm thinking...")
      sleep(pause * 4)

      if len(possiblewords) < 4 and len(possiblewords) > 0:
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
      guesses.append(guess)
      ########PRINT RESULTS##########

      #CORRECT GUESS
      if guess.upper() in word:
         print ("%s was in the word/phrase!" % guess, flush = True)
         sleep(pause * 2)
         print("\n")
         word = word.replace(guess.upper(), guess)

      #INCORRECT GUESS
      else: 
         print ("I guessed wrong!", flush = True)
         guessnum -= 1
         sleep(pause)
         if(guessnum != 0):
            print ("But I have incorrect %d guesses left!" % guessnum, flush = True) 
            sleep(pause)
            print("\n")

   #The while loop will exit normally if the computer runs our of guesses.
   else:
      print ("\n\nI ran out of guesses! You won this round!")
      player_2.points += 1

   #Display the results of the round.
   if(player_1.points > player_2.points):
      print("I am currently winning with %d points. You have %d points." %(player_1.points, player_2.points))
   elif(player_2.points > player_1.points):
      print("You are currently winning with %d points. I have %d points."% (player_2.points, player_1.points))
   else:
      print("We are tied with %d points" % player_1.points)

###########################################################################################
# play_hangman_multi takes a word or phrase from Player 1 and allows Player 2 to start
# guessing the letters in the word or phrase
##########################################################################################
def play_hangman_multi():

   global player_1
   global player_2
   global words
   
   #Keep trying for error checking.
   while True:
      try:
         rounds = int(input("\nHow many rounds would you like to play? "))
         break
      except:
         continue
   
   #initialize the settings for the game
   sleep(pause)
   print("")
   player_1.name = input("What's the name of player 1? ")
   player_2.name = input("What's the name of player 2? ")
   
   #run rounds * 2 (1 turn for each player)
   for r in range(0, rounds * 2):
      if(r % 2 == 0):
         print ("Round: %d" % ((r + 2)/2))
      
      #empty out words and add what we request on top.
      words.clear()
      
      #Request the next word from the user.
      words.append(input("\n%s, enter the word or phrase (make sure %s doesn't see): " % (player_1.name, player_2.name)))
      
      #Clear the screen so that the other player cannot see the word that was just entered.
      if(name == 'nt'):
         system('cls')
      else:
         system('clear')
      
      #Play the round
      play_hangman()

      #Switch the players, display results so far and play another round
      player_1, player_2 = player_2, player_1
      if (r < rounds * 2 - 1):
         if(player_1.points > player_2.points):
            print (player_1.name + " is winning with " + str(player_1.points) + " points.")
            print (player_2.name + " is behind with " + str(player_2.points) + " points.")
         elif(player_2.points > player_1.points):
            print (player_2.name + " is winning with " + str(player_2.points) + " points.")
            print (player_1.name + " is behind with " + str(player_1.points) + " points.")
         else:
            print ("It's currently a tie. You both have " + str(player_1.points) + " points.")
      
      #Display final results
      else:
         print("\n\nGame Over\nHere are the results:")
         if(player_1.points > player_2.points):
            print (player_1.name + " won with " + str(player_1.points) + " points.")
            print (player_2.name + " lost with " + str(player_2.points) + " points.")
         elif(player_2.points > player_1.points):
            print (player_2.name + " won with " + str(player_2.points) + " points.")
            print (player_1.name + " lost with " + str(player_1.points) + " points.")
         else:
            print ("It ended in a tie. You both have " + str(player_1.points) + " points.")


#######################################################################################
# Play again will determine if the user wants to change any settings before
# playing again. Then it will run the program again
#######################################################################################
def play_again():
   
   #Display the current settings
   print("CURRENT SETTINGS:")
   if(play_type == "single player"):
      print("There are %d possible words which are chosen at random." % len(words))
   print("You are currently playing %s." % play_type)
   print("Incorrect Guess Limit: %d" % guess_setting)
   if play_type == "2-player":
      print("Player 1: %s" % player_1.name)
      print("Player 2: %s" % player_2.name)

   #Change the settings if necessary
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

   global player_1
   global player_2
   #Choose a random word in our list
   word = words[randint(0, len(words) - 1)].lower()
   
   #make a copy of the word that we can manipulate as the game plays on.
   wordcopy = word
   
   #set the number of guesses
   guessnum = guess_setting

   #sleep will slow down the program to make it more user friendly.
   sleep(pause)

   if play_type == "2-player" or play_type == "against the computer":
      print ("%s, you have %d guesses to guess each letter in the word or phrase." % (player_2.name, guessnum))
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
         else:
            print ("\n\n%s won! Better luck next time %s." % (player_2.name, player_1.name))
            player_2.points += 1
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
      print ("\n\n%s lost! Mr. Hangman is dead. The word/phrase was %s" % (player_2.name, word)) 
      player_1.points += 1
  

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








