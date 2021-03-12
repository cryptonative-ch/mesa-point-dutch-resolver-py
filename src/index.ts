// Externals
import { BigNumber, utils } from 'ethers'
import { resolve } from 'path'
import web3 from 'web3'

// Interfaces
import { AuctionBid } from './interfaces/Auction'

// Libs
import { parseAuctionData } from './mesa/auction-data'
import { calculateClearingPrice } from './mesa/price'

// IIFE
;(async () => {
  console.log('init')

  // Resolves the relative CSV file to absolute
  const absoluteCsvFilePath = resolve(__dirname, '../data/realistic-bids.csv')
  // Parses the CSV file and returns an array of AuctionBidData
  const auctionBidsFromCSV = await parseAuctionData(absoluteCsvFilePath)

  // Maps AuctionBidData to AuctionBid. See the difference in src/interfaces/Auction.ts
  const auctionBids = auctionBidsFromCSV.map(({ price, addressName, tokenInAmount }) => {
    return {
      address: addressName,
      buyAmount: BigNumber.from(web3.utils.toWei(tokenInAmount.toString(), 'ether')),
      sellAmount: BigNumber.from(web3.utils.toWei(price.toString(), 'ether')),
    } as AuctionBid
  })

  // Find the virtual settlment price
  const { buyAmount, sellAmount } = calculateClearingPrice(auctionBids)

  console.log(`The virtual settlment price is $${web3.utils.fromWei(BigNumber.from(sellAmount).toString(), 'ether')}`)
  console.log(`The virtual settlment price is $${web3.utils.fromWei(BigNumber.from(buyAmount).toString(), 'ether')}`)
})()
