import { BigNumber } from '@ethersproject/bignumber'

export interface AuctionBidData {
  addressName: string
  addressIndex: number
  tokenInAmount: number
  price: number
}

/**
 * Source: https://github.com/cryptonative-ch/mesa-interface/blob/main/src/interfaces/Auction.ts
 */
export interface AuctionBid {
  sellAmount: BigNumber // Number of tokens the investor wants to buy
  buyAmount: BigNumber // Price at which they wish to buy
  address: string // Their Ethereum address
}
