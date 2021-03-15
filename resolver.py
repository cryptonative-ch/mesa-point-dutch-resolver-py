# !/usr/bin/python3

import csv, sys, json

from decimal import *
getcontext().prec = 18

def csvimport(path):
    reader = csv.DictReader(open(path, 'r'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list

tokenOutAmountTotal = Decimal(50000)

bidsSorted = csvimport('data/realistic-bids-sort.csv') 

bidsUnsorted = csvimport('data/realistic-bids.csv') 

#print(bidsSorted)

# def csvexport(csvfile):


# calc clearingPrice():


for bid in bidsSorted:
	bid['price'] = Decimal(bid['price'])
	bid['tokenInAmount'] = Decimal(bid['tokenInAmount']) 
	bid['amountToBid'] = Decimal(bid['tokenInAmount'] / bid['price'])


for bid in bidsUnsorted:
	bid['price'] = Decimal(bid['price'])
	bid['tokenInAmount'] = Decimal(bid['tokenInAmount']) 
	bid['amountToBid'] = Decimal(bid['tokenInAmount'] / bid['price'])

# print(json.dumps(bids, indent = 4))

def myClearingPrice(bids, tokenOutAmountTotal):
	print('------------------------------------------------------------')
	print('   calculate  myClearingPrice             ')
	print('------------------------------------------------------------')

	currentBidSum = Decimal(0)

	currentTokenOutAmount = tokenOutAmountTotal
	i = 0
	for bid in bids:
		price = bid['price']
		tokenInAmount = bid['tokenInAmount'] 
		amountToBid = bid['amountToBid']

		print('amountToBid: {} $MESA ({} $DAI for {} $DAI per $MESA)'.format(amountToBid, tokenInAmount, price))

		currentTokenOutAmount = currentTokenOutAmount - amountToBid

		# coint back from 0
		currentBidSum = currentBidSum + amountToBid

		bid['currentBidSum'] = currentBidSum

		print('currentTokenOutAmount: {} $MESA (Token left)'.format(currentTokenOutAmount))
		print('currentBidSum: {} $MESA'.format(currentBidSum))
		print('---------------')


		# currentBidSum.mul(amountToBuy) < fullAuctionAmountToSell.mul(amountToBid)
		# currentBidSum * amountToBuy < fullAuctionAmountToSell * amountToBid
		# currentBidSum * tokenInAmount < tokenOutAmountTotal * amountToBid

		# all token taken, the price of the last bid is clearing price
		#if currentBidSum > tokenOutAmountTotal:
		
		#if currentBidSum * tokenInAmount < tokenOutAmountTotal * amountToBid:


		# stop if all token gone and take the clearingPrice last bid

		if currentTokenOutAmount < 0:
			# set clearingPrice to first bid on which all token have sold out
			clearingPrice = bids[i]['price']
			# amountToBid = bids[i-1]['amountToBid']
			# amountToBuy = bids[i-1]['tokenInAmount']

			print('Token left: {} '.format(lastCurrentTokenOutAmount))
			print('ClearingPrice: {} $DAI per $MESA '.format(clearingPrice))

			# uncoveredBids = bids[i-1]['currentBidSum'] - (tokenOutAmountTotal *  amountToBid / amountToBuy)
			# print('uncoveredBids: {}'.format(uncoveredBids))

			# set amountToBid to the token left to sell all tokens
			bids[i]['amountToBid'] = lastCurrentTokenOutAmount

			clearingPrice = price
			return clearingPrice, lastCurrentTokenOutAmount

			break
			
		lastCurrentTokenOutAmount = currentTokenOutAmount
		i += 1

def scClearingPrice(tokenOutAmountTotal):
	currentBidSum = 0
	print(tokenOutAmountTotal)
	# price = amountToBuy/amountToBid 

	condition = True
	while condition:
		for bid in bids:
			price = Decimal(bid['price'])
			tokenInAmount = Decimal(bid['tokenInAmount']) 
			amountToBid = bid['amountToBid']

			print('amountToBid: {} $MESA for {} $DAI for {} $DAI per $MESA'.format(amountToBid, tokenInAmount, price))

			#tokenOutAmountTotal = tokenOutAmountTotal - amountToBid

			currentBidSum = currentBidSum + amountToBid

			print('tokenOutAmountTotal: {} $MESA'.format(tokenOutAmountTotal))
			print('currentBidSum: {} $MESA'.format(currentBidSum))
			print('---------------')
			# currentBidSum.mul(amountToBuy) < fullAuctionAmountToSell.mul(amountToBid)
			# currentBidSum * amountToBuy < fullAuctionAmountToSell * amountToBid
			# currentBidSum * tokenInAmount < tokenOutAmountTotal * amountToBid
			# if tokenOutAmountTotal < 0:  50000 * 
			if currentBidSum * tokenInAmount < tokenOutAmountTotal * amountToBid:
				print('soldout: {} '.format(currentBidSum))
				print('price: {} $DAI'.format(price))
				print('ClearingPrice: {} $DAI per $MESA '.format(price))
				clearingPrice = price
				condition = False


# for the full investemnt token are distributed

def myTokenDistroFull(bids, tokenOutAmountTotal):

	for bid in bids:
		price = bid['price']
		if price > clearingPrice:
			tokenInAmount = bid['tokenInAmount'] 
			# amountToBid = bid['amountToBid']

			tokenOutAmountPerBid = tokenInAmount / clearingPrice

			bid['tokenOutAmount'] = tokenOutAmountPerBid


			tokenOutAmountTotal = tokenOutAmountTotal - tokenOutAmountPerBid
			print('---------------')

			print('tokenOutAmountPerBid: {} $MESA worth {} $DAI, price {}'.format(tokenOutAmountPerBid, tokenInAmount, bid['price']))

			print('Token Left: {} $MESA'.format(tokenOutAmountTotal))


# only order token are distributed for fix price

def myTokenDistroEasyAction(bids, clearingPrice, tokenOutAmountTotal, lastCurrentTokenOutAmount):
	print('------------------------------------------------------------')
	print('          myTokenDistroEasyAction                   ')
	print('------------------------------------------------------------')
	print('clearingPrice: {}'.format(clearingPrice))

	
	print('------------------------------------------------------------')
	for bid in bids:
		price = bid['price']
		if price >= clearingPrice:
			bid['status'] = 1

			# set amountToBid to the token, so that token left to sell exaclty all tokens
			
			if price == clearingPrice:
				bid['amountToBid'] = lastCurrentTokenOutAmount

			tokenInAmount = bid['tokenInAmount'] 
			tokenOutAmount = bid['amountToBid'] # amountToBid in EasyAction
			
			bidCost = tokenOutAmount * clearingPrice

			excessCapital = tokenInAmount - bidCost

			#bid['tokenOutAmount'] = tokenOutAmountPerBid

			tokenOutAmountTotal = tokenOutAmountTotal - tokenOutAmount
			print('')
			print('Bid ID {}'.format(bid['bidid']))
			#print('bidid: {},  addressName: {}'.format(bid['bidid'], bid['addressName'] ))

			print('tokenOutAmount: {} $MESA worth {} $DAI'.format(tokenOutAmount, bidCost))
			print('{} $DAI not invested from {} $DAI, bid price {}'.format(excessCapital, tokenInAmount,  price))

			print('Token Left: {:f} $MESA'.format(tokenOutAmountTotal))
		else:
			print('No token for Bid ID {} with bid price {}'.format( bid['bidid'], price))

	# with sorted csv
			
	if tokenOutAmountTotal == 0 or tokenOutAmountTotal > -1:
		print('------------------------------------------------------------')
		print('         Success - all token distributed')
		print('------------------------------------------------------------')
		
		with open('data/realistic-bids-sorted-result.csv', 'w') as csvfile:
			fieldnames = ['addressName', 'bidid','addressIndex', 'tokenInAmount', 'price', 'amountToBid', 'status', 'currentBidSum' ]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for line in bids:
				writer.writerow(line)
	# with unsorted csv
	elif tokenOutAmountTotal > 0:
		print('------------------------------------------------------------------------')
		print('         Fail! Not all token distributed! Settlement price is too high.')
		print('------------------------------------------------------------------------')
		with open('data/realistic-bids-result-sp-too-high.csv', 'w') as csvfile:
			fieldnames = ['addressName', 'bidid','addressIndex', 'tokenInAmount', 'price', 'amountToBid', 'status', 'currentBidSum' ]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for line in bids:
				writer.writerow(line)

	elif tokenOutAmountTotal < 0:
		print('------------------------------------------------------------------------')
		print('         Fail! To many token distributed! Settlement price is too low.')
		print('------------------------------------------------------------------------')
		with open('data/realistic-bids-result-sp-too-low.csv', 'w') as csvfile:
			fieldnames = ['addressName', 'bidid','addressIndex', 'tokenInAmount', 'price', 'amountToBid', 'status', 'currentBidSum' ]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for line in bids:
				writer.writerow(line)
	# test

	for bid in bids:
		price = bid['price']
		# no other bid can be below the bidding price
		#if price > clearingPrice and tokenOutAmountTotal == 0:
			# print('error')


clearingPrice, lastCurrentTokenOutAmount = myClearingPrice(bidsSorted, tokenOutAmountTotal)

print(clearingPrice)
print(lastCurrentTokenOutAmount)
# myTokenDistroFull(tokenOutAmountTotal)

myTokenDistroEasyAction(bidsSorted, Decimal(clearingPrice), tokenOutAmountTotal, lastCurrentTokenOutAmount)

myTokenDistroEasyAction(bidsUnsorted, Decimal(clearingPrice), tokenOutAmountTotal, lastCurrentTokenOutAmount)


print('------------------------------------------------------------')
print('          test with a wrong settlement price  0.77      ')
print('------------------------------------------------------------')

clearingPrice = Decimal(0.77)
myTokenDistroEasyAction(bidsUnsorted, Decimal(clearingPrice), tokenOutAmountTotal, lastCurrentTokenOutAmount)

print('------------------------------------------------------------')
print('          test with a wrong settlement price  0.75      ')
print('------------------------------------------------------------')

clearingPrice = Decimal(0.75)
myTokenDistroEasyAction(bidsUnsorted, Decimal(clearingPrice), tokenOutAmountTotal, lastCurrentTokenOutAmount)


# distribution of tokens




# print(json.dumps(bids, indent = 4))
