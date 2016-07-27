#!/usr/bin/python
import argparse
import logging
import time
import sys
import operator
import random
import getpass
from collections import Counter
from custom_exceptions import GeneralPogoException

from api import PokeAuthSession
from location import Location

from pokedex import pokedex
from inventory import items

def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

## Mass remove pokemon. It first displays the "Safe" numbers of pokemon that can be released, then makes sure you want to release them
def massRemove(session):
	party = session.checkInventory().party
	myParty = []
	
	# Get the stats for all the pokemon in the party. Easier to store and nicer to display.
	for pokemon in party:
		IvPercent = ((pokemon.individual_attack + pokemon.individual_defense + pokemon.individual_stamina)*100)/45
		L = [pokedex[pokemon.pokemon_id],pokemon.cp,pokemon.individual_attack,pokemon.individual_defense,pokemon.individual_stamina,IvPercent,pokemon]
		myParty.append(L)
	
	# Sort the list by name and then IV percent
	myParty.sort(key = operator.itemgetter(0, 5))
	
	safeIV = int(raw_input('\nWhat is your IV cut off? (Pokemon above this will be safe from transfer): '))
	safeCP = int(raw_input('What is your CP cut off? (Pokemon above this will be safe from transfer): '))
	
	# Create a "safe" party by removing good IVs and high CPs
	safeParty = [item for item in myParty if item[5] < safeIV and item[1] < safeCP]
	
	# Ask user which pokemon they want. This must be CAPITALS.
	userPokemon = raw_input("\nWhich pokemon do you want to transfer? (ALL will transfer everything below the safe zones): ").upper()
	
	# If they choose ALL, then sort by IV, not by name
	if userPokemon == 'ALL':
		safeParty.sort(key = operator.itemgetter(5))
	
	# Show user all the "safe to remove" pokemon
	refinedMonsters = []
	print '\n'
	print ' NAME            | CP    | ATK | DEF | STA | IV% '
	print '---------------- | ----- | --- | --- | --- | ----'
	for monster in safeParty:
		if monster[0] == userPokemon or userPokemon == 'ALL':
			if monster[5] > 74:
				logging.info('\033[1;32;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])
			elif monster[5] > 49:
				logging.info('\033[1;33;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])
			else:
				logging.info('\033[1;37;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])
			refinedMonsters.append(monster)
	
	# If they can't "safely" remove any pokemon, then send them to the main menu again
	if len(refinedMonsters) < 1:
		print "\nCannot safely transfer any Pokemon of this type. IVs or CP are too high."
		mainMenu(session)
	
	if userPokemon == 'ALL':
		logging.info('\nCan safely remove %s Pokemon',len(refinedMonsters))
	else:
		logging.info('\nCan safely remove %s of this Pokemon',len(refinedMonsters))
	
	# Ask how many they want to remove
	userNumber = int(raw_input("How many do you want to remove?: "))
	
	if userNumber == 0:
		mainMenu(session)
	
	# Show the pokemon that are going to be removed to confirm to user
	print '\n'
	i = 0
	monstersToRelease = []
	print ' NAME            | CP    | ATK | DEF | STA | IV% '
	print '---------------- | ----- | --- | --- | --- | ----'
	for monster in refinedMonsters:
		if i < int(userNumber):
			i = i + 1
			if monster[5] > 74:
				logging.info('\033[1;32;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])
			elif monster[5] > 49:
				logging.info('\033[1;33;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])
			else:
				logging.info('\033[1;37;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])
			monstersToRelease.append(monster)
	
	# Double check they are okay to remove
	if userPokemon == 'ALL':
		if int(userNumber) > len(refinedMonsters):
			logging.info('\nThis will transfer %s Pokemon',len(refinedMonsters))
		else:
			logging.info('\nThis will transfer %s Pokemon',userNumber)
	else:
		if int(userNumber) > len(refinedMonsters):
			logging.info('\nThis will transfer %s of this Pokemon',len(refinedMonsters))
		else:
			logging.info('\nThis will transfer %s of this Pokemon',userNumber)
		
	okayToProceed = raw_input('Do you want to transfer these Pokemon? (y/n): ').lower()
	
	# Remove the pokemon! Use randomness to reduce chance of bot detection
	outlier = random.randint(8,12)
	index = 0
	counter = 1
	if okayToProceed == 'y':
		for monster in monstersToRelease:
			index = index + 1
			counter = counter + 1
			session.releasePokemon(monster[6])
			logging.info('Transferring Pokemon %s of %s...',counter,len(monstersToRelease))
			t = random.uniform(2.0, 5.0)
			if index == outlier:
				t = t * 3
				outlier = random.randint(8,12)
				index = 0
			time.sleep(t)
	
	# Go back to the main menu
	mainMenu(session)
	
def massRename(session):
	party = session.checkInventory().party
	myParty = []
	
	# Get the party and put it into a nicer list
	for pokemon in party:
		IvPercent = ((pokemon.individual_attack + pokemon.individual_defense + pokemon.individual_stamina)*100)/45
		L = [pokedex[pokemon.pokemon_id],pokemon.cp,pokemon.individual_attack,pokemon.individual_defense,pokemon.individual_stamina,IvPercent,pokemon]
		myParty.append(L)
	
	# Sort party by name and then IV percentage	
	myParty.sort(key = operator.itemgetter(0, 5))
	
	# Ask the user to enter an IV threshold (to only rename good pokemon)
	userThreshold = int(raw_input('Enter an IV% threshold to rename Pokemon (0 will rename all): '))
	
	# Refine a party with the IV threshold
	print '\n NAME            | CP    | ATK | DEF | STA | IV% '
	print '---------------- | ----- | --- | --- | --- | ----'
	refinedParty = []
	for monster in myParty:
		if monster[5] > userThreshold:# and monster[6].nickname == '':
			logging.info(' %-15s | %-5s | %-3s | %-3s | %-3s | %-3s | %s',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5],monster[6].nickname)
			refinedParty.append(monster)
	
	# Show how many it will rename and if they want to continue
	logging.info('\nThis will rename %s Pokemon.',len(refinedParty))
	okayToProceed = raw_input('Do you want to rename these Pokemon? (y/n): ').lower()
	
	# Rename the pokemon! Use randomness to reduce chance of bot detection
	outlier = random.randint(8,12)
	index = 0
	if okayToProceed == 'y':
		for monster in refinedParty:
			index = index + 1
			session.nicknamePokemon(monster[6],str(monster[5]) + '-' + str(monster[2]) + '/' + str(monster[3]) + '/' + str(monster[4]))
			logging.info('Renamed ' + monster[0] + ' to ' + str(monster[5]) + '-' + str(monster[2]) + '/' + str(monster[3]) + '/' + str(monster[4]))
			t = random.uniform(4.0, 8.0)
			if index == outlier:
				t = t * 2
				outlier = random.randint(8,12)
				index = 0
			time.sleep(t)
	
	mainMenu(session)
	
def viewCounts(session):
	party = session.checkInventory().party
	myParty = []
	
	# Get the party and put it into a nicer list
	for pokemon in party:
		L = pokedex[pokemon.pokemon_id]
		myParty.append(L)
	
	# Count the number of pokemon, put them in a list, and sort alphabetically
	countRepeats = Counter(myParty)
	countListTmp = countRepeats.items()
	countList = []
	
	for entry in countListTmp:
		item = list(entry)
		pokedexNum = getattr(pokedex, item[0])
		item.append(pokedexNum)
		countList.append(item)
	
	# logging.info(countList)
	
	sortBy = int(raw_input('How to sort the list? (1 = Alphabetically, 2 = Total Numbers, 3 = Pokedex): '))
	countList.sort(key = operator.itemgetter(sortBy - 1))
	
	# Total number of Pokemon that can be evolved
	# Number of evolutions per Pokemon
	countEvolutions = 0
	evolutions = 0
	
	# Print the list of pokemon in a nicer format
	print '\n NAME            | COUNT | CANDIES | EVOLVE '
	print '---------------- | ----- | ------- | ------ '
	for monster in countList:
		evolutions = ''
		skipCount = 0
		pokedexNum = getattr(pokedex, monster[0])
		try:
			candies = session.checkInventory().candies[pokedexNum]
		except:
			skipCount = 1
			try:
				candies = session.checkInventory().candies[pokedexNum - 1]
			except:
				try:
					candies = session.checkInventory().candies[pokedexNum - 2]
				except:
					candies = 0

		if(pokedex.evolves[pokedexNum]):
			evolutions = min(monster[1],int((candies-1)/pokedex.evolves[pokedexNum]))
			if evolutions > 0 and skipCount == 0:
				countEvolutions += evolutions
			else:
				evolutions = ''
		print ' %-15s | %-5d | %-7d | %s ||| %s' % (monster[0], monster[1], candies, evolutions, countEvolutions)
	
	mainMenu(session)
	
def viewPokemon(session):
	party = session.checkInventory().party
	myParty = []
	
	# Get the party and put it into a nicer list
	for pokemon in party:
		IvPercent = ((pokemon.individual_attack + pokemon.individual_defense + pokemon.individual_stamina)*100)/45
		L = [pokedex[pokemon.pokemon_id],pokemon.cp,pokemon.individual_attack,pokemon.individual_defense,pokemon.individual_stamina,IvPercent,pokemon]#,pokemon.move_1,pokemon.move_2]
		myParty.append(L)
	
	# Sort party by name and then IV percentage	
	myParty.sort(key = operator.itemgetter(0, 5))
	
	# Display the pokemon, with color coding for IVs and separation between types of pokemon
	i = 0
	print ' NAME            | CP    | ATK | DEF | STA | IV% '
	print '---------------- | ----- | --- | --- | --- | ----'
	for monster in myParty:
		if i > 0:
			if myParty[i][0] != myParty[i-1][0]:
				print '---------------- | ----- | --- | --- | --- | ----'
		if monster[5] > 74:
			logging.info('\033[1;32;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])#,monster[7],monster[8])
		elif monster[5] > 49:
			logging.info('\033[1;33;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])#,monster[7],monster[8])
		else:
			logging.info('\033[1;37;40m %-15s | %-5s | %-3s | %-3s | %-3s | %-3s \033[0m',monster[0],monster[1],monster[2],monster[3],monster[4],monster[5])#,monster[7],monster[8])
		i = i+1

	mainMenu(session)
	
def mainMenu(session):
	print '\n\n  MAIN MENU'
	print '  ---------'
	print '  1: View Pokemon'
	print '  2: View Counts'
	print '  3: Transfer Pokemon'
	print '  4: Rename Pokemon'
	print '  5: Exit'
	
	menuChoice = int(raw_input("\nEnter choice: "))
	if menuChoice == 1: viewPokemon(session)
	elif menuChoice == 2: viewCounts(session)
	elif menuChoice == 3: massRemove(session)
	elif menuChoice == 4: massRename(session)
	elif menuChoice == 5: quit()
	else: quit()
		
		
# Entry point
# Start off authentication and demo
if __name__ == '__main__':
    setupLogger()
    logging.debug('Logger set up')

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="Auth Service", required=True)
    parser.add_argument("-u", "--username", help="Username", required=True)
    parser.add_argument("-p", "--password", help="Password", required=False)
    parser.add_argument("-l", "--location", help="Location", required=True)
    parser.add_argument("-g", "--geo_key", help="GEO API Secret")
    args = parser.parse_args()

    # Check service
    if args.auth not in ['ptc', 'google']:
        logging.error('Invalid auth service {}'.format(args.auth))
        sys.exit(-1)
        
    # Check password
    if args.password == None:
    	args.password = getpass.getpass()

    # Create PokoAuthObject
    poko_session = PokeAuthSession(
        args.username,
        args.password,
        args.auth,
        geo_key=args.geo_key
    )

    # Authenticate with a given location
    # Location is not inherent in authentication
    # But is important to session
    session = poko_session.authenticate(args.location)

    # Time to show off what we can do
    if session:
	
		mainMenu(session)

    else:
        logging.critical('Session not created successfully')
