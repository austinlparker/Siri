from util import hook
 
import random
 
# the .markov <user> command
@hook.command
def markov(inp, nick='', chan='', db=None):
    ".markov <user> -- markov gen for user based on previous chat logs"
    if nick == '':
        return
 
        # try to generate sentence
        quote = construct_quote(nick, chan, db)
 
        # return result if we have one!
        if quote is None:
                return "[can't markov that person (maybe no history)]"
        else:
                return str(nick) + " once said, " + '"' + str(quote).strip() + '"'
 
 
 
# builds the sentence
def construct_quote(nick, chan, db):
        start_phrases = db.execute("select w1, w2, w3 from chat_markov where chan=? and lower(nick)=lower(?) and start='Y' ", (chan, nick)).fetchall()
 
        # no start phrases
        if len(start_phrases) == 0:
                return None
 
        # grab a start phrase
        i = random.randint(0, len(start_phrases) -1)
        w1,w2,w3 = start_phrases[i]
        
        # will store all our words for our sentence
        words = []
        words.append(w1)
        words.append(w2)
        words.append(w3)
 
        # lets go until we grab 7 more (total of 10)
        for i in (xrange(7)):
                # grab matches where our w2,w3 = other w1,w2
                phrases = db.execute("select w3 from chat_markov where chan=? and lower(nick)=lower(?) and start='N' and w1=? and w2=? ", (chan, nick, w2, w3)).fetchall()
 
                # hit a dead end, just return with what we have already
                if len(phrases) == 0:
                        sentence = ' '.join(words)
                        return sentence
                else:
                        # grab random w3 and append to our sentence
                        j = random.randint(0, len(phrases) -1)
                        # moving everything over
                        w2 = w3
                        word = phrases[j]
                        w3 = word[0][0]
                        words.append(w3)
 
        # appends all the words with space inbetween
        sentence = ' '.join(words)
	return sentence
 
# watching the chat and parsing to db
@hook.regex(".")
def watch_chat(inp, nick='', chan='', db=None, match='', msg=''):
	
	msg_words = msg.split()
 
	if msg_words.count < 3:
		return None
 
	# try to create table if first time running
	db.execute("create table if not exists chat_markov (a INTEGER PRIMARY KEY, chan, nick, w1, w2, w3, start)")
	db.commit()
 
    
    # add set of 3 to table
	for w1, w2, w3, start in triples(msg_words):
		db.execute('''insert or fail into chat_markov (chan, nick, w1, w2, w3, start) values(?,?,?,?,?,?)''', (chan, nick, w1, w2, w3, start))
 
	# save to db
	db.commit()
 
 
 
# returns message in sets of 3 words with flag if words start sentence
def triples(split_msg):
 
	for i in range(len(split_msg) -2):
 
		w1 = split_msg[i]
		w2 = split_msg[i + 1]
		w3 = split_msg[i + 2]
 
		if (w1 != "\n" and w2 != "\n" and w3 != "\n"):
			if (i == 0):
				yield (w1,w2,w3,'Y')
			else:
				yield (w1,w2,w3,'N')
		else:
			return
