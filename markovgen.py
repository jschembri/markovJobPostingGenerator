# -*- coding: utf-8 -*-

import random
import codecs


class Markov(object):
	def __init__(self, open_file):
		self.cache = {}
		self.open_file = open_file
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.database()
		
	
	def file_to_words(self):
		self.open_file.seek(0)
		data = self.open_file.read()
		words = data.split()
		return words
		
	
	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text(self, sentences):
		gen_words = []
		for n in xrange(sentences):
			seed = random.randint(0, self.word_size-3)
			seed_word, next_word = self.words[seed], self.words[seed+1]

			while (self.words[seed-1][-1] !='.' or seed == 0 or '*' in self.words[seed] ):
				seed = random.randint(0, self.word_size-3)
				seed_word, next_word = self.words[seed], self.words[seed+1]

			w1, w2 = seed_word, next_word
			

			i = 0
			j = 0
			while(i<100):	
				gen_words.append(w1)
				if(w1[-1] == '.'):
					break
				newWord = random.choice(self.cache[(w1, w2)])
				while('*' in newWord and j < 10):
					newWord = random.choice(self.cache[(w1, w2)])
					j = j +1

				w1, w2 = w2, random.choice(self.cache[(w1, w2)])

				i = i +1

		#gen_words.append(w2)
		#print gen_words
		#print "Something is going on there \n"
		gen_words.append( '<br><br>')
		return ' '.join(gen_words)


class MarkovBullets(object):
	def __init__(self, open_file):
		self.cache = {}
		self.open_file = open_file
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.database()
		
	
	def file_to_words(self):
		self.open_file.seek(0)
		data = self.open_file.read()
		words = data.split()
		return words
		
	
	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text(self, sentences):
		gen_words = []
		for n in xrange(sentences):
			seed = random.randint(0, self.word_size-3)
			seed_word, next_word = self.words[seed], self.words[seed+1]

			while (self.words[seed] !='*'):
				seed = random.randint(0, self.word_size-3)
				seed_word, next_word = self.words[seed], self.words[seed+1]

			w1, w2 = seed_word, next_word
			

			i = 0
			#for i in xrange(size):
			while(i<100):	
				gen_words.append(w1)
				if(w1[-1] == ';'):
					gen_words.append( '<br>')
					break
				w1, w2 = w2, random.choice(self.cache[(w1, w2)])
				i = i +1


		return ' '.join(gen_words)
