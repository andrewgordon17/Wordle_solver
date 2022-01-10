#andrew gordon
import json

#Computes what feedback you receive if you guess 'guess' and the answer is 'target' 
#Most difficult part is handling double letters
#feedback is given as a string of '0' (grey) '1' (yellow) and '2' (green)
def distance(guess,target):
	if len(guess)!=len(target):
		raise ValueError
	dist = []
	for i in range(len(guess)):
		dist.append(0)
	for i in range(len(target)):
		if target[i] == guess[i]:
			if dist[i] == 1:
				for j in range(i+1, len(guess)):
					if guess[j] == target[i]:
						dist[j] = 1
						break
			dist[i] = 2
		else:
			for j in range(len(guess)):
				if guess[j] == target[i]:
					if dist[j] == 0:
						dist[j] = 1
						break
	return ''.join([str(x) for x in dist])
	

#finds the best guess gievn a list of words that are legal guesses and words that can be solutions
#Exhaustive search. this will run slowly if both lists are long
#returns a tuple containing the best word and all target words sorted into a dict keyed by distance to the best word	
def find_best(guesswords, targetwords):
	
	best = (-1,'', {})
	avg = len(targetwords)/(3**len(guesswords[0]) - len(guesswords[0]))
	
	for guess in guesswords:
		responses = {}
		for target in targetwords:
			d = distance(guess, target)
			if d in responses:
				
				responses[d].append(target)
			else:
				responses[d] = [target]
				
		score = sum([abs(avg - len(responses[key])) for key in responses.keys()]) 
		score += avg*(3**len(guesswords[0]) - len(guesswords[0]) - len(responses.keys()))

		if best[0] > score or best[0] < 0:
			best = (score, guess, responses.copy())
		elif best[0] == score and guess in targetwords:
			best = (score, guess, responses.copy())
	return (best[1], best[2])
	
#creates a tree-like data structure that describes optimal play. Uses recursion
#Every node of the tree contains a word, the guess
#	and a dict holding child nodes keyed by feedback strings
#	i.e. If after guessing 'AAAAA' your distance is '01200', then looking up '01200' 
#	in the corresponding dict gives a tuple containging the next best guess and a new dict
#inputs
#	word- the initial guess
#	responses- dict containing all possible solutions as values, keyed by distance to 'word'. Edited in place by this function!
#	total- list of all words legal as guesses. Not necessary in hard mode
def create_tree(word, responses, guesslist):
	if len(responses.keys()) == 0:
		return((word, {}))
	elif len(responses.keys()) == 1:
		k = list(responses.keys())[0]
		return ( (responses[k][0], {}) )
	else:
		for key in responses.keys():
			best = find_best(guesslist, responses[key]) #for hard mode use find_best(responses[key], responses[key])
			responses[key] = create_tree(best[0], best[1], guesslist)
		return (word, responses)


#creates a decision tree for the game
#inputs
#	guesslist- list of legal guesses
#	targetlist- list of possible solutions
#	word1- initial guess. If left as '' this function computes the best choice of word1. This computation is slow and not recommended
def create_master(guesslist, targetlist, word1='reast'):
	if word1 == '':
		(word1, responses) = find_best(guesslist, targetlist)
	else:
		responses = {}
		for target in targetlist:
			d = distance(word1, target)
			if d in responses:
				responses[d].append(target)
			else:
				responses[d] = [target]
	mt = create_tree(word1, responses, guesslist)
	return mt
	
	
#inputs a tree and answer, computes the number of guesses to find that answer in the tree
def play(tree, answer):
	if tree[0] == answer:
		return 1
	else:
		d = distance(tree[0], answer)
		return play(tree[1][d], answer)+1

#Statistics on how well a tree does
#The 'html_mastertree.json' tree yields {2: 29, 3: 971, 4: 1203, 5: 112}
def statistics(mt, solnlist):
	lengths = {}
	for word in solnlist:
		p = play(mt, word)
		if p not in lengths:
			lengths[p] = 1
		else:
			lengths[p] += 1
	return(lengths)

#----------------------------------------------------
#These lines will make a tree and save it as a json:

	#guesslist = json.load(open("htmlguesses.json", "r"))
	#solnlist =  json.load(open("htmlsolns.json", "r"))
	#mt = create_master(guesslist ,solnlist)
	#json.dump(mt, open('html_mastertree.json', 'w'))
#-----------------------------------------------------

#main method. Runs an interactive wordle solver
def main():
	print('Welcome to Andy\'s Wordle Solver!')
	print('Please think of a target word')

	mt = json.load(open('html_mastertree.json', 'r'))
	print('Score guesses by using strings of 0 (wrong letter), 1 (wrong place) and 2 (right letter)')
	print('For example, if the answer is APPLE, the guess BELLS scores 01020')
	print('------------------------------------')


	count = 0
	tree = mt
	while True:
		print('I guess: ' + tree[0])
		count += 1
		score = input('Score: ')

		while (len(score) != len(tree[0])) or (not set(score).issubset(set('012'))) or (not score in tree[1].keys()):
			if score == '22222':
				print('I win! It took ' + str(count) + ' guesses!')
				return()
			input('Invalid Score. Try again: ')
		if score == '22222':
			print('I win! It took ' + str(count) + ' guesses!')
			return()
		tree = tree[1][score]

if __name__ == "__main__":
	main()


	








		
	
	
	
			
	
