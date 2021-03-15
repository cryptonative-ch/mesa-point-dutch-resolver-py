# !/usr/bin/python3
import csv, sys, json

from decimal import *
getcontext().prec = 18

class pointDutch():

	def __init__(self):
		helper = helperTools()
		self.bidsUnsorted = helper.csvimport('data/realistic-bids.csv')
		self.bidsSorted = helper.csvimport('data/realistic-bids-sort.csv')
		self.tokenOutAmountTotal = 50000
		self.clearingPrice = 0

		for bid in self.bidsSorted:
			bid['price'] = Decimal(bid['price'])
			bid['tokenInAmount'] = Decimal(bid['tokenInAmount']) 
			bid['tokenOutAmount'] = bid['tokenInAmount'] / bid['price']

		for bid in self.bidsUnsorted:
			bid['price'] = Decimal(bid['price'])
			bid['tokenInAmount'] = Decimal(bid['tokenInAmount']) 
			bid['tokenOutAmount'] = bid['tokenInAmount'] / bid['price']


	def calcClearingPrice(self, bids):
		print('------------------------------------------------------------')
		print('   calculate  calcClearingPrice             ')
		print('------------------------------------------------------------')

		currentTokenOutAmount = self.tokenOutAmountTotal
		i = 0

		for bid in bids:
			price = bid['price']
			tokenInAmount = bid['tokenInAmount'] 
			tokenOutAmount = bid['tokenOutAmount']

			print('tokenOutAmount: {} $MESA ({} $DAI for {} $DAI per $MESA)'.format(tokenOutAmount, tokenInAmount, price))

			currentTokenOutAmount = currentTokenOutAmount - tokenOutAmount

			print('currentTokenOutAmount: {} $MESA (Token left)'.format(currentTokenOutAmount))
			print('---------------')


			# currentBidSum.mul(amountToBuy) < fullAuctionAmountToSell.mul(tokenOutAmount)
			# currentBidSum * amountToBuy < fullAuctionAmountToSell * tokenOutAmount
			# currentBidSum * tokenInAmount < self.tokenOutAmountTotal * tokenOutAmount

			# all token taken, the price of the last bid is clearing price
			#if currentBidSum > self.tokenOutAmountTotal:
			
			#if currentBidSum * tokenInAmount < self.tokenOutAmountTotal * tokenOutAmount:


			# stop if all token gone and take the clearingPrice last bid

			if currentTokenOutAmount < 0:
				# set clearingPrice to first bid on which all token have sold out
				clearingPrice = bids[i]['price']
				# tokenOutAmount = bids[i-1]['tokenOutAmount']
				# amountToBuy = bids[i-1]['tokenInAmount']

				print('Token left: {} '.format(lastCurrentTokenOutAmount))
				print('ClearingPrice: {} $DAI per $MESA '.format(clearingPrice))

				# uncoveredBids = bids[i-1]['currentBidSum'] - (tokenOutAmountTotal *  tokenOutAmount / amountToBuy)
				# print('uncoveredBids: {}'.format(uncoveredBids))

				# set tokenOutAmount to the token left to sell all tokens
				bids[i]['tokenOutAmount'] = lastCurrentTokenOutAmount

				self.clearingPrice = price
				self.lastCurrentTokenOutAmount = lastCurrentTokenOutAmount

				break
				
			lastCurrentTokenOutAmount = currentTokenOutAmount
			i += 1


	def tokenDistroEasyAction(self, bids, clearingPrice):
		print('------------------------------------------------------------')
		print('          tokenDistroEasyAction                   ')
		print('------------------------------------------------------------')
		print('clearingPrice: {}'.format(clearingPrice))

		tokenOutAmountToDistribute = self.tokenOutAmountTotal

		print('------------------------------------------------------------')
		for bid in bids:
			print('')
			print('Bid ID {}'.format(bid['bidid']))

			price = bid['price']
			if price >= clearingPrice:
				bid['status'] = 1
				# set tokenOutAmount to the token, so that token left to sell exaclty all tokens
			
				if price == self.clearingPrice:
					bid['tokenOutAmount'] = self.lastCurrentTokenOutAmount

				tokenInAmount = bid['tokenInAmount'] 
				tokenOutAmount = bid['tokenOutAmount'] # tokenOutAmount in EasyAction
				
				bidCost = tokenOutAmount * clearingPrice

				excessCapital = tokenInAmount - bidCost

				#bid['tokenOutAmount'] = tokenOutAmountPerBid

				tokenOutAmountToDistribute = tokenOutAmountToDistribute - tokenOutAmount

				#print('bidid: {},  addressName: {}'.format(bid['bidid'], bid['addressName'] ))

				print('tokenOutAmount: {} $MESA worth {} $DAI'.format(tokenOutAmount, bidCost))
				print('{} $DAI not invested from {} $DAI, bid price {}'.format(excessCapital, tokenInAmount,  price))

				print('Token Left: {:f} $MESA'.format(tokenOutAmountToDistribute))
			else:
				print('No token for bid price {}'.format( price))

		# with sorted csv
				
		if self.tokenOutAmountTotal == 0 or self.tokenOutAmountTotal > -1:
			print('------------------------------------------------------------')
			print('         Success - all token distributed')
			print('------------------------------------------------------------')
			
			with open('data/realistic-bids-sorted-result.csv', 'w') as csvfile:
				fieldnames = ['addressName', 'bidid','addressIndex', 'tokenInAmount', 'price', 'tokenOutAmount', 'status']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writeheader()
				for line in bids:
					writer.writerow(line)
		# with unsorted csv
		elif self.tokenOutAmountTotal > 0:
			print('------------------------------------------------------------------------')
			print('         Fail! Not all token distributed! Settlement price is too high.')
			print('------------------------------------------------------------------------')
			with open('data/realistic-bids-result-sp-too-high.csv', 'w') as csvfile:
				fieldnames = ['addressName', 'bidid','addressIndex', 'tokenInAmount', 'price', 'tokenOutAmount', 'status']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writeheader()
				for line in bids:
					writer.writerow(line)

		elif self.tokenOutAmountTotal < 0:
			print('------------------------------------------------------------------------')
			print('         Fail! To many token distributed! Settlement price is too low.')
			print('------------------------------------------------------------------------')
			with open('data/realistic-bids-result-sp-too-low.csv', 'w') as csvfile:
				fieldnames = ['addressName', 'bidid','addressIndex', 'tokenInAmount', 'price', 'tokenOutAmount', 'status']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writeheader()
				for line in bids:
					writer.writerow(line)
		# test

		for bid in bids:
			price = bid['price']
			# no other bid can be below the bidding price
			#if price > clearingPrice and self.tokenOutAmountTotal == 0:
				# print('error')


class helperTools():
	def csvimport(self, path):
	    reader = csv.DictReader(open(path, 'r'))
	    dict_list = []
	    for line in reader:
	        dict_list.append(line)
	    return dict_list

# print(json.dumps(bids, indent = 4))

sim = pointDutch()

sim.calcClearingPrice(sim.bidsSorted)

sim.tokenDistroEasyAction(sim.bidsUnsorted, sim.clearingPrice)


sim.tokenDistroEasyAction(sim.bidsUnsorted, sim.clearingPrice)

print('------------------------------------------------------------')
print('          test with a wrong settlement price  0.77      ')
print('------------------------------------------------------------')

clearingPrice = Decimal(0.77)
sim.tokenDistroEasyAction(sim.bidsSorted, clearingPrice)

print('------------------------------------------------------------')
print('          test with a wrong settlement price  0.75      ')
print('------------------------------------------------------------')

clearingPrice = Decimal(0.75)
sim.tokenDistroEasyAction(sim.bidsSorted, clearingPrice)

print(sim.clearingPrice)
print(sim.lastCurrentTokenOutAmount)
# print(json.dumps(bids, indent = 4))
