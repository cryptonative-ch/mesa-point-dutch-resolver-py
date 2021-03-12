// Externals

// Libs
import { parseAuctionData } from './mesa'


const auctionBidsFromCSV = await parseAuctionData(resolve(__dirname, '../data/realistic-bids.csv'))


;(async () => {

  console.log('init')

  // Create 20 random bids - WIP
})()
