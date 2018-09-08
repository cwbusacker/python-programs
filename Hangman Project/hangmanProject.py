####################################################################################
# Title: Python Hangman
# Author: Chase Busacker
# Time Estimate: 10 hours
#
# This is my personal hangman project.  It can be played in a variety of ways:
# one "practice" round, a number(specified) of rounds verses a computer,
# or a number(specified) of rounds human against human.
#
# After all the settings have been specified, the program will allow a
# number(specified)
# of guesses to allow the user or computer to guess.  Whoever wins will gain a
# point
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
words = ["cat", "dog", "chicken", "rooster", "cow", "hen", "pig", "hamster", "guinea pig"] #default words 
pause = 1
play_type = ""
guess_setting = 14                   
command = 'Z'
rounds = 1
man = "    44444444\n    3      5\n    3      6\n    3     879\n    3     0 +\n111132222" #Will change
manCopy = "    44444444\n    3      5\n    3      6\n    3     879\n    3     0 +\n111132222" #CONSTANT

#The two players.  Names will be changed when game begins.
player_1 = player("Player 1", 0)
player_2 = player("Player 2", 0)

##########################################################################
# readDict takes a filename which is usually dictionary.txt and reads
# it into words line by line.
##########################################################################
def readDict(filename):
   #words is what we will be returning.  So initialize it to be empty.
   words = []
   try:
      #Open the file
      with open(filename, 'r') as files:
         #loop through each line in the file and append it to the words list.
         for line in files:
               words.append(str(line[0:len(line)-1]).lower())
   except:
      print("ERROR: Dictionary not found! Please add a dictionary.txt file to the local directory.")

   return words


##########################################################################
# readFile takes a filename, attempts to open it and requests a different
# filename if the file is not found.
##########################################################################
def readFile(filename):
  
   #words is what we will be returning.  So initialize it to be empty.
   words = []
   try:
      #Open the file!
      with open(filename, 'r') as files:
         #loop through each line in the file
         for line in files:
            #lowercase all the strings and split them between the spaces.
            for word in line.lower().split():
               #Remove a punctuation attached at the end of the word.
               if not word[len(word) - 1].isalnum():
                  word = word[0:len(word) - 1]
               #append the word to the list.
               words.append(word)
   #if the file didn't open correctly, request another filename
   except:
      print("ERROR: Incorrect Filename.\nPlease try again.")
      words = readFile(input("Enter filename: "))

   return words

def changeSettings(type, name1, name2):
    #setup the settings of the game
    global play_type, player_1, player_2

    play_type = type
    player_1.name = name1
    player_1.points = 0
    player_2.name = name2
    player_2.points = 0

def getRounds():
   try:
      rounds = int(input("\nHow many rounds would you like to play? "))
      return rounds
   except:
      print("ERROR: Rounds must be a number! Try again.")
      getRounds()

#######################################################################
# Setting updater will update the settings of the game
####################################################################
def setting_updater(updateSettings):

   #the global variables we will be changing.
   global words, play_type, guess_setting, player_1, player_2, command, rounds, man
   
   while updateSettings:
      print("\nWhat version of Hangman would you like to play?")
      command = input("\n1 for 1 Player(1 solo practice round)\n2 for 2 Player(Human vs. Human)\nC for the Computer(Human vs. Computer): ").upper()
      sleep(pause)
         
      #Only want to get the guess number if we have a valid command.
      
      if command == 'C' or command == '1' or command == '2':
         #Loop until we have a valid guess number.
         guess_setting = 14
         while guess_setting > 10 or guess_setting < 1:
            try:
               #if the try worked we will have an integer and break out
               guess_setting = int(input("\nIncorrect Guess Limit (max:10) : "))
            except:
               print("ERROR: Invalid input. Please enter a number.")
               continue
         break
      #Invalid command given (Not 1, 2, 3).  Alert the user and request again.
      else:
         print("ERROR: Invalid Command\nPlease try again.")
         continue
   
      sleep(pause)

      #Single Player
   if(command == '1'):
      if updateSettings:
         changeSettings("single player","UNKNOWN", "You")
         print("Would you like to read in a file of words?")
         print("\nEnter a fileName for Yes, N for No.")
         file = input()

      #if the user requested to read a file in, then
      #we will call the readfile function which
      #will the take the filename and read it into our global words list.
         if file.upper() != "N":
            words = readFile(file)
      clearScreen()
      play_hangman()
  
   # 2 Player.  Sets the play_type and calls play_hangman_multi
   elif(command == '2'):
      play_type = "2-player"
      play_hangman_multi()
  
   # Computer!  Sets the play_type and plays the computer.
   elif(command == 'C'):
      changeSettings("against the computer", "computer", "You")

      if updateSettings:
         rounds = getRounds()
         
         clearScreen()
         #Load the dictionary before we begin.
         print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\t\tLoading...\n")
         words = readDict("dictionary.txt")
         clearScreen()  

         #Loop the amount of rounds   
      for i in range(0, rounds):

         clearScreen()
         print("Round: %d" % (i + 1))
         #play the computer
         play_computer()
         sleep(pause*2)  

         #Computer challenge the user
         print("My turn to challenge you.")
         sleep(pause)
         play_hangman()

         #Display who is winning and repeat
         if i < rounds - 1:
            print("Your turn to challenge me again.")
            if(player_1.points > player_2.points):
               print("I am winning with " + str(player_1.points) + " points.")
               print("You are behind with " + str(player_2.points) + " points.")
            elif(player_2.points > player_1.points):
               print("You are winning with " + str(player_2.points) + " points.")
               print("I am behind with " + str(player_1.points) + " points.")
            else:
               print("It's currently a tie. We both have " + str(player_1.points) + " points.")
         
         #display the final results.
      print("Game Over\nHere are the results:\n")
      if(player_1.points > player_2.points):
         print("I won with " + str(player_1.points) + " points.")
         print("You lost with " + str(player_2.points) + " points.")
      elif(player_2.points > player_1.points):
         print("I won with " + str(player_2.points) + " points.")
         print("You lost with " + str(player_1.points) + " points.")
      else:
         print("It ended in a tie. We both have " + str(player_1.points) + " points.")

      sleep(pause)

   if(input("Play again(Y for Yes, Any key for No)? ").upper() == "Y"):
      clearScreen()
      setting_updater(play_again())
            
def displayBoard(phrase, guessesLeft):
   
   letterstoguess = 0 #A count of unguessed letters
   displayword = "" #eventually the final display word
   for i in range(0, len(phrase)):

        #This made it easier to keep track of variables.
      if phrase[i].isupper():
         displayword += "_ "
         letterstoguess += 1
         
            #if the letter has been guessed, we print the letter and a space.
      elif phrase[i].islower():
         displayword += phrase[i] + " "

         #spaces = 2 spaces to make it more readable
      elif(phrase[i] == " "):
         displayword += "  "

         #It must be a number or symbol.  We display these for free.
      else:
         displayword += phrase[i]

      ########PRINT THE DISPLAY
      #print our display
   displayMan(guess_setting - guessesLeft)
   print("")
   print(displayword) 
   return letterstoguess


#######################################################################
# play_computer uses a dictionary and letter frequency algorithms to
# guess the next best letter for a given word or phrase.
# Then it will show the user what it's trying to guess and keep guessing
# up until the guess_setting.
########################################################################
def play_computer():
   
   global player_1, player_2, man

   man = manCopy
   #Request the word or phrase from the user
   word = input("Enter a word or phrase to challenge the computer: ").upper()

   #wordlist = words because words is currently our dictionary.
   wordlist = readDict("dictionary.txt")
   dictionary = {}

   #Letters in the order of most to least common.
   defaultletters = ["e", "t", "a", "o", "i", "n", "s", "r", "h", "l", "d", "c", "u",
                     "m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]

   letterstoguess = len(word)
   #Place each word in the dictionary/association array with a key(word length)
   #and value(word).
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
   print("I have %d guesses to guess each letter in the word." % guessnum)

   #guesses is the guesses the computer has done.
   guesses = []

   #make a list of words for the final result
   wordlist = word.lower().split()

   #The Number of words the computer has guessed, helps access the index for
   #which word the computer is working on
   numwordsguessed = 0
   print("\n")
   #Let the games begin.  Run while there are still guesses left!
   while guessnum > 0:

      letterstoguess = displayBoard(word, guessnum)

      if letterstoguess == 0:
         print("\n\nI beat you! You lost!")
         player_1.points += 1
         break

      #Allows some time between guesses so the user can
      #actually see what is going on.
      sleep(pause * 2)
      print("\n\nI'm thinking...")
      sleep(pause * 2)

      #make a list of possible words (empty at the beginning)
      possiblewords = []

      ##########STEP 1 : DETERMINE WORD TO WORK ON#########
      #The length of numwordsguessed is smaller than the index AND the word at
      #the index islower AKA has been guessed
      if len(wordlist) > numwordsguessed and word.split()[numwordsguessed].islower() :
         numwordsguessed += 1
         continue
      elif(len(wordlist) == numwordsguessed):
         pass
      else:
         #if changing words isn't necessary then we will continue narrowing
         #down until
         ##########STEP 2 : CREATE DICTIONARY AND NARROW DOWN#########
         #try just in case the dictionary is empty.
         try:
            for possibles in dictionary[len(word.split()[numwordsguessed])]:
               count = 0

               #if we haven't guessed a single letter yet then the possible
               #words are any word that's the same length.
               if len(guesses) == 0 and word.split()[numwordsguessed].isalpha():
                  possiblewords = dictionary[len(wordlist[0])]
                  break

               else: #no guesses have occured so include ONLY words that are the same length
                     #lack letters that have been guessed incorrectly, and
                                         #contain letters
                                         #in the same spot if guessed correctly.
                  for c in word.split()[numwordsguessed]:
                     if ((c.islower() and c != possibles[count]) 
                         or (possibles[count] in guesses and (possibles[count] not in word.split()[numwordsguessed][count] or c.isupper()))
                         or (not c.isalpha() or not possibles[count].isalpha()) and c != possibles[count]):
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
            if c in guesses or not c.isalpha():
               continue
            elif c not in lettercount.keys() and c not in guesses:
               lettercount[c] = 1
            elif c not in guesses:
               lettercount[c] += 1
      
      #make letter count a list of letters sorted by most frequent to least
      #frequent
      lettercount = sorted(lettercount.keys(), key = lettercount.get, reverse = True)

      
       ##########STEP 4 : GENERATE GUESS#########
      #if there is more than one letter to guess or are only a
      #couple of possible words left then we will find the next best guess.
      #For loops used to find the
      if (letterstoguess > 1 or len(possiblewords) < 3) and len(lettercount) > 0:
         guess = lettercount[0]
      # Only 1 letter left, better to use default letters
      else:
         possiblewords = []
         for guess in defaultletters:
               if guess not in guesses:
                  break
      
      
      rand = randint(0,5)

      ########PRINT THE GUESS Let the computer "THINK"
      

      if len(possiblewords) < 4 and len(possiblewords) > 0:
         print("OH! I think I know what that word is now!!")
         sleep(pause * 1.5)
         print("Let's go with %s!" % guess)
      elif(rand == 1):
         print("I'm gonna guess %s?" % guess)

      elif(rand == 2):
         print("How about %s?" % guess)

      elif(rand == 3):
         print("I'll try the letter %s." % guess)

      else:
         print("Are there any %s's?" % guess)
      possiblewords = []
      sleep(pause * 1.5)
      guesses.append(guess)
      ########PRINT RESULTS##########
      clearScreen()
      #CORRECT GUESS
      if guess.upper() in word:
         print("%s was in the word/phrase!" % guess, flush = True)
         print()
         word = word.replace(guess.upper(), guess)

      #INCORRECT GUESS
      else: 
         print("I guessed wrong!", flush = True)
         guessnum -= 1
         if(guessnum != 0):
            print("But I have incorrect %d guesses left!" % guessnum, flush = True) 


   #The while loop will exit normally if the computer runs our of guesses.
   else:
      displayBoard(word, guessnum)
      print("")
      print("\n\nI ran out of guesses! You won this round!")
      player_2.points += 1

   #Display the results of the round.
   if(player_1.points > player_2.points):
      print("I am currently winning with %d points. You have %d points." % (player_1.points, player_2.points))
   elif(player_2.points > player_1.points):
      print("You are currently winning with %d points. I have %d points." % (player_2.points, player_1.points))
   else:
      print("We are tied with %d points" % player_1.points)
   sleep(pause*6)
   clearScreen()

###########################################################################################
# play_hangman_multi takes a word or phrase from Player 1 and allows Player 2
# to start
# guessing the letters in the word or phrase
##########################################################################################
def play_hangman_multi():

   global player_1, player_2, words, man
   
   rounds = getRounds()
   
   #initialize the settings for the game
   sleep(pause)
   print("")
   player_1.name = input("What's the name of player 1? ")
   player_2.name = input("What's the name of player 2? ")
   player_1.points = 0
   player_2.points = 0

   #run rounds * 2 (1 turn for each player)
   for r in range(0, rounds * 2):
      if(r % 2 == 0):
         print("Round: %d" % ((r + 2) / 2))
      
      #empty out words and add what we request on top.
      words.clear()
      
      #Request the next word from the user.
      words.append(input("\n%s, enter the word or phrase (make sure %s doesn't see): " % (player_1.name, player_2.name)))
      
      while len(words[0]) == 0:
         words.clear()
         print("You didn't enter anything. Please try again.")
         words.append(input("%s, enter the word or phrase (make sure %s doesn't see): " % (player_1.name, player_2.name)))

      #Clear the screen so that the other player cannot see the word that was
      #just entered.
      clearScreen()
      
      #Play the round
      play_hangman()

      #Switch the players, display results so far and play another round
      player_1, player_2 = player_2, player_1
      if (r < rounds * 2 - 1):
         if(player_1.points > player_2.points):
            print(player_1.name + " is winning with " + str(player_1.points) + " points.")
            print(player_2.name + " is behind with " + str(player_2.points) + " points.")
         elif(player_2.points > player_1.points):
            print(player_2.name + " is winning with " + str(player_2.points) + " points.")
            print(player_1.name + " is behind with " + str(player_1.points) + " points.")
         else:
            print("It's currently a tie. You both have " + str(player_1.points) + " points.")
      
      #Display final results
      else:
         print("\n\nGame Over\nHere are the results:")
         if(player_1.points > player_2.points):
            print(player_1.name + " won with " + str(player_1.points) + " points.")
            print(player_2.name + " lost with " + str(player_2.points) + " points.")
         elif(player_2.points > player_1.points):
            print(player_2.name + " won with " + str(player_2.points) + " points.")
            print(player_1.name + " lost with " + str(player_1.points) + " points.")
         else:
            print("It ended in a tie. You both have " + str(player_1.points) + " points.")


#######################################################################################
# Play again will determine if the user wants to change any settings before
# playing again.  Then it will run the program again
#######################################################################################
def play_again():
   
   clearScreen()
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
         return True
      elif command == 'N':
         return False
      else:
         print("ERROR: Invalid command.\nPlease try again.")


def clearScreen():
   if(name == 'nt'):
      system('cls')
   else:
      system('clear')

#################################################################
# Play Hangman runs the game after the correct files have been
# read in.  Will run recursively until the user wants to exit.
#################################################################
def play_hangman():
   
   global man, player_1, player_2

   man = manCopy
   #Choose a random word in our list
   word = words[randint(0, len(words) - 1)].upper()
   
   #set the number of guesses
   guessnum = guess_setting

   if play_type == "2-player" or play_type == "against the computer":
      print("%s, you have %d guesses to guess each letter in the word or phrase." % (player_2.name, guessnum))
   else:
      print("You have %d guesses to guess each letter in the word or phrase." % guessnum)

   
   #set the guesses list to empty.
   guesses = []

   #Let the games begin.  Run while there are still guesses left!
   while guessnum > 0:

      #print a new line each time to organize the screen better.
      print("\n")

      #reset letters to guess to zero and create the display word
      letterstoguess = 0
      displayword = ""
      
      # Here is where we prepare the display (with '_ ' for each letter not
      # guessed)
      letterstoguess = displayBoard(word, guessnum)

      
      #if there were no more letters to guess then the game is over.
      #so break the loop
      if letterstoguess == 0:
         if play_type == "single player":
            print("\n\nCongratulations! You won!")
            break
         else:
            print("\n\n%s won! Better luck next time %s." % (player_2.name, player_1.name))
            player_2.points += 1
            break

      #guess a letter and add to guesses.

      guess = input("\n\nPlease enter a letter to guess: ").lower()

      clearScreen()

      #guess must be only one letter!
      if len(guess) < 2:
         #if the user guessed a letter in the word.
         if guess in word.lower() and guess not in guesses:
            word = word.replace(guess.upper(), guess)
            print("%s was in the word/phrase!" % guess, flush = True)
      
         #if the user guessed the same letter twice (guess count not changed)
         elif guess in guesses:
            print("Try again. You already guessed that.", flush = True)
      
         #the user guessed a letter that wasn't in the word.
         else: 
            print("Sorry. %s was not in the word/phrase." % guess, flush = True)
            guessnum -= 1
            print("%d incorrect guesses left!" % guessnum, flush = True) 
      
      #the guess was not a single letter!
      else:
          print("Try again. You cannot guess more than one letter.", flush = True)
      
      #add to the list of guesses
      guesses.append(guess)

   #if the while loop exits normally, then display the lost message.
   else:
      displayBoard(word, guessnum)
      print("")
      print("\n\n%s lost! Mr. Hangman is dead. The word/phrase was %s" % (player_2.name, word.lower())) 
      player_1.points += 1
   sleep(pause*3)
   clearScreen()
  

def changeMan(changeNum):
   
   global man    
   #1, 2 and 4
   if changeNum < 3 or changeNum == 4:
      man = man.replace(str(changeNum)[0], "_")
   #3, 5, 7
   elif changeNum % 2 == 1 and changeNum < 8:
      man = man.replace(str(changeNum), "|")
   elif changeNum == 6:
      man = man.replace('6', "O")
   elif changeNum == 8:
      man = man.replace("8", "/")
   elif changeNum == 9:
      man = man.replace("9", "\\")
   elif changeNum == 10:
      man = man.replace("0", "/")
   elif changeNum == 11:
      man = man.replace("+", "\\")
  
  
def displayMan(guess):
   
   if guess == 0:
      pass
   elif guess_setting == 1:
      for i in range(1, 12):
         changeMan(i)

   elif guess_setting < 8 and guess == 1:
      for i in range(1,6):
         changeMan(i)

   elif guess_setting == 10:
      if guess == 1:
         changeMan(1)
         changeMan(2)
      else:
         changeMan(guess+1)
   elif guess_setting == 9:
      if guess == 1:
         changeMan(1)
         changeMan(2)
      elif guess == 2:
         changeMan(3)
         changeMan(4)
      else:
         changeMan(guess + 2)
   elif guess_setting == 8:
      if guess == 1:
         changeMan(1)
         changeMan(2)
         changeMan(3)
      elif guess == 2:
         changeMan(4)
         changeMan(5)
      else:
         changeMan(guess + 3)
   elif guess_setting == 7:
         changeMan(guess + 4)
   elif guess_setting == 6:
      if guess == 4:
         changeMan(8)
         changeMan(9)
      elif guess == 2 or guess == 3:
         changeMan(guess + 4)
      else:
         changeMan(guess + 5)
   elif guess_setting == 5:
      if guess == 4:
         changeMan(8)
         changeMan(9)
      elif guess == 5:
         changeMan(10)
         changeMan(11)
      else:
         changeMan(guess+4)
   elif guess_setting == 4:
      if guess == 2:
         changeMan(6)
      elif guess == 3:
         for i in range(7,10):
            changeMan(i)
      elif guess == 4:
         for i in range(10, 12):
            changeMan(i)
   elif guess_setting == 3:
      if guess == 2:
         changeMan(6)
         changeMan(7)
      elif guess == 3:
         for i in range(8,12):
            changeMan(i) 
   elif guess_setting == 2:
         for i in range(6,12):
            changeMan(i)
   display = ""
   for c in man:
      if c.isdigit() or c == '+':
         display += " "
      else:
         display += c
   print(display)


######################################################################
# Main is where the program will start. It will call welcome (which
# will welcome the user and read in the word file. Then it will call
# Play Hangman which will run the game until the user is done
######################################################################
def main():
   #welcome is used to welcome the user, get the settings, and open the file
   print ("Welcome to Python Hangman!")
   print("Before we begin, let's configure the settings of the game:")
   setting_updater(True)
   
  
main()








