import re

###################
#### CONSTANTS ####
###################

## Change these strings to whatever you choose to name your piles from the XML

deck = "Deck"
discard = "Discard"

## Change this HEX string value to customize the highlight color
highlight = "#ff0000"

# Change this positive integer value to customize the default Draw Many count
drawManyDefault = 5

# Change this tuple if you want to create a specific default marker (not recommended)
StandardMarker = ("Marker", "d9851c6f-2ed7-4ca9-82d2-f22e4e12114c")

######################
#### PILE ACTIONS ####
######################

def shuffle(group, x = 0, y = 0):
    mute()
    group.shuffle()
    notify("{} shuffles their {}.".format(me, group.name))

def draw(group, x = 0, y = 0):
    mute()
    if len(group) < 1:
        return
    card = group.top()
    for card in group.top(5):
        card.moveTo(card.owner.hand)
    notify("{} puts his {} into his hand.".format(me, group.name))

def drawMany(group, x = 0, y = 0):
    if len(group) < 1:
        return
    mute()
    global drawManyDefault
    count = askInteger("Draw how many cards?", drawManyDefault)
    drawManyDefault = count
    for card in group.top(count):
        card.moveTo(card.owner.hand)
    notify("{} draws {} cards from {}.".format(me, count, group.name))

def discardMany(group, x = 0, y = 0):
    if len(group) < 1:
        return
    mute()
    count = askInteger("Discard how many cards?", 1)
    for card in group.top(count):
        card.moveTo(card.owner.piles[discard])
    notify("{} discards {} cards from {}.".format(me, count, group.name))

def allToDeck(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles[deck])
    notify("{} moves all cards from {} to {}.".format(me, group.name, me.piles[deck].name))

######################
#### HAND ACTIONS ####
######################

def randomDiscard(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    card.moveTo(me.piles[discard])
    notify("{} randomly discards {} from {}.".format(me, card, group.name))

def randomPick(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    if confirm("Reveal randomly-picked {}?".format(card.Name)):
        index = card.index
        card.moveTo(me.piles[discard])
        notify("{} randomly picks {} from their {}.".format(me, card, group.name))
        card.moveTo(me.hand, index)
    else:
        notify("{} randomly picks {} (hidden) from their {}.".format(me, card, group.name))
    card.select()
    card.target(True)

#######################
#### TABLE ACTIONS ####
#######################

def rollDice(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def rollTwoDice(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    v = rnd(1, 6)
    p = n + v
    if n == v:
        notify("DOUBLES! {} rolls {} and {}, totalling {}.".format(me, n, v, p))
    else:
        notify("{} rolls {} and {}, totalling {}.".format(me, n, v, p))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def interrupt(group, x = 0, y = 0):
    notify('{} interrupts the game.'.format(me))

def passTurn(group, x = 0, y = 0):
    notify('{} passes.'.format(me))

def addAnyMarker(cards, x = 0, y = 0):
    mute()
    marker, quantity = askMarker()
    if quantity == 0: return
    for card in cards:
        card.markers[marker] += quantity
        notify("{} adds {} {} marker(s) to {}.".format(me, quantity, marker[0], card))

def addMarker(cards, x = 0, y = 0):
    mute()
    for card in cards:
        card.markers[StandardMarker] += 1
        notify("{} adds a marker to {}.".format(me, card))

def removeMarker(cards, x = 0, y = 0):
    mute()
    for card in cards:
        if card.markers[StandardMarker] < 1:
            return
        card.markers[StandardMarker] -= 1
        notify("{} removes a marker from {}.".format(me, card))

def rotate(cards, x = 0, y = 0):
  mute()
  for card in cards:
      if card.orientation == 3:
          card.orientation = 0
      else:
          card.orientation += Rot90
      #if card.orientation == Rot90:
        #  card.orientation = Rot180
      #if card.orientation == Rot180:
        #  card.orientation = Rot270
      #if card.orientation == Rot270:
        #  card.orientation ^= Rot90
      notify('{} rotates {}'.format(me, card))
      #else:
        #notify('{} turns {} upright'.format(me, card))

def flip(cards, x = 0, y = 0):
    mute()
    for card in cards:
        if card.isFaceUp == True:
          notify("{} flips {} face down.".format(me, card))
          card.isFaceUp = False
        else:
          card.isFaceUp = True
          notify("{} flips {} face up.".format(me, card))

def highlightCard(cards, x = 0, y = 0):
  mute()
  for card in cards:
      if card.highlight == highlight:
        card.highlight = None
        notify('{} removes highlight from {}'.format(me, card))
      else:
        card.highlight = highlight
        notify('{} highlights {}'.format(me, card))


####################
### CARDS ELCIOS ###
####################


'''
class Warrior:
    def __init__(self,nam, cult, trt,elm, hp, spd, xp, dmg,grd):
        self.name = nam
        self.culture = cult
        self.trait = trt
        self.element = elm
        self.life = hp
        self.speed = spd
        self.experience = xp
        self.damage = dmg
        self.grid = grd
    column = 0
    line = 0
    orientation = 'nowhere'

class Suport:
    def __init__(self,typ,nam,init,cult,trt):
        self.name = nam
        self.initiative = init
        self.type = typ
        self.culture = cult
        self.trait = trt

class Inspiration(Suport):
    def __init__(self, elm):
        self.element = elm

class Weapon(Suport):
    def __init__(self,dmg,grd):
        self.damage = dmg
        self.grid = grd
        '''

#------------------------------------------------------------------------------
# New Events
#------------------------------------------------------------------------------
'''def on_table_load():
	mute()
	setGlobalVariable("automode","0")

def onloaddeck(args):
	mute()
	# if args.player == me:
	# 	if getGlobalVariable("selectgamemode") =="1":afterload(me)
	# 	else:
	# 		setGlobalVariable("Invertedloaddeck","1")
	# 		notify("waiting for host select game mode")
	if args.player == me:afterload(me)
'''
