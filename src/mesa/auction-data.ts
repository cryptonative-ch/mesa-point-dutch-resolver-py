// Externals
import { isAbsolute } from 'path'
import csv from 'csvtojson'

// Interfaces
import { AuctionBidData } from 'src/interfaces/Auction'

export const fixFieldTypes = ({ addressIndex, addressName, price, tokenInAmount }: AuctionBidData): AuctionBidData => ({
  addressName,
  price: parseFloat(price.toString()),
  tokenInAmount: parseFloat(tokenInAmount.toString()),
  addressIndex: parseFloat(addressIndex.toString()),
})

export async function parseAuctionData(csvFilePath: string) {
  console.log(csvFilePath)
  if (!isAbsolute(csvFilePath)) {
    throw new Error('CSV file path must be absolute')
  }

  const auctionBids = await csv().fromFile(csvFilePath)

  return auctionBids.map(fixFieldTypes)
}
