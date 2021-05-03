import requests
import random

# Global Variables
global wins
global losses
global pokemon
global max
global min
global mycards
global prevstat
mycards = []
pokemon = []
wins = 0
losses = 0
prevstat = -1


def playagain():
    again = input("Play again (Y/N) ? ")
    if again.lower() == "y":
        main(0)
    elif again.lower() == "yes":
        main(0)


def load():
    global pokemon
    global max
    global min
    # makesure array is empty!
    pokemon = []
    # load all pokemon with id min to max
    for i in range(min, max):
        url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(i)
        pokemon.append(requests.get(url).json())
        print("loading: " + str(int(i/max*100))+"%")
    print("Loaded!\n\n\n\n\n\n\n\n")
    return 1


def rand_op():
    global mycards
    test = 1
    opponent = 0
    # test for the same as player and randomise until different
    while test == 1:
        test = 0
        opponent = random.randint(0,len(pokemon)-1)
        for j in mycards:
            for i in j:
                if opponent == i:
                    test = 1
                    opponent = random.randint(0,len(pokemon)-1)
    return opponent


def createdeck(numcards):
    global mycards
    deck = []
    for i in range(0,numcards):
        deck.append(rand_op())
    mycards.append(deck)
    print("Player deck generated with " + str(numcards) + " cards")


def main(start):
    global max
    global min
    global wins
    global losses
    global pokemon
    global mycards
    global prevstat
    global opponents
    print("")

    # check if game already in progress
    if start == 0:
        opponents = int(input('Number of opponents:'))
        for i in range(0,opponents+1):
            createdeck(int(len(pokemon)/(opponents+1)))

    #use variable "string" as buffer to create complicated print() without using multiple print functions

    string = "You have: " + str(pokemon[mycards[0][0]]['name']).upper() +  "- Your Opponent(s) have:"
    for i in range(1,len(mycards)):
        string = string + "  " + str(pokemon[mycards[i][0]]['name']).upper()

    #shiny pokemon bonus!
    bonus =0
    if random.randint(1,1000)>999:
        print("Your pokemon wants to evolve!")
        bonus = 25
    elif random.randint(1,15)>14:
        print("Your pokemon is holding something!")
        bonus = random.randint(5,15)
    elif random.randint(1,20)>19:
        print("Your pokemon is holding something?")
        bonus =-random.randint(5,25)
    #counting variable i
    i=0
    #rotate through stats for pokemon, load into selector
    for stat in pokemon[mycards[i][0]]['stats']:
        i =i+1
        # checks for previously used stat
        if i-1 != prevstat:
            string = string + "\n\t(" + str(i)+") "+ stat['stat']['name'] + " - " + str(stat['base_stat'])
            if bonus!=0:
                string= string +"*"
        else:
            string =string + "\n\t(-) "+ stat['stat']['name'] + " - USED LAST ROUND"
    print (string)

    #grab stat selection from input, cast to integer
    chosen = int(input("choose a stat: "))-1
    if chosen > i:
        chosen = -1
    if chosen ==prevstat:
        chosen =-1
    #check selection is above 1-1(0), repeat input command if not!
    while chosen <0:
        chosen = int(input("INVALID please choose a stat:"))-1
        if chosen > i :
            chosen =-1
        elif chosen ==prevstat:
            chosen = -1
    prevstat = chosen


    #check for winner

    print("")
    winner = -1
    for i in range(1,len(mycards)):
        if winner <=0 :
            if pokemon[mycards[0][0]]['stats'][chosen]['base_stat']+bonus > pokemon[mycards[i][0]]['stats'][chosen]['base_stat']:
                winner = 0
            else:
                winner = i
        else:
            if pokemon[mycards[winner][0]]['stats'][chosen]['base_stat'] > pokemon[mycards[i][0]]['stats'][chosen]['base_stat']:
                winner = i

    # adds loosing cards to winners deck
    win_pk = ""
    for i in range (0,len(mycards)):
        if winner == i:
            for j in range(0,len(mycards)):
                if winner != j:
                    mycards[i].append(mycards[j][0])
                    mycards[j].pop(0)
                else:
                    win_pk = str(pokemon[mycards[i][0]]['name']).upper()
                    mycards[i].append(mycards[i][0])
                    mycards[i].pop(0)

    # text for who's won
    if winner == 0 :
        string = "you won! the opposing pokemon have been added to your hand!"
        wins = wins+1
    else:
        string = "Your pokemon lost against "+ win_pk
        losses = losses+1

    string = string +" - You have " + str(wins) +" wins and "+ str(losses) +" losses - " +  str(len(mycards[0])) + ' cards in your deck ' + str(len(pokemon)-len(mycards[0])) +" to collect"


    print(string)
    if len(mycards[0]) <1 :
        print ("you lost!")
        playagain()
    elif len(mycards) > len(pokemon)-1:
        print("you won all of the cards!")
        playagain()
    else:

        # if deck has less than 1 card, removes deck/opponent from play
        for i in range(1, len(mycards)):
            if len(mycards[i]) <= 0:
                mycards.pop(i)
        # run main function in game in progress mode
        main(1)

max = 300
min = 151
opponents = 0
load()
main(0)
