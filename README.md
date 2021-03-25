# Mesa Point Dutch Resolver

This is experimental code to find out if we can move on-chain computing of the finial price off-chain and save a lot of gas. Final settelment price is then pushed 
on-chain, only the right solution will resolve and settle the auction.

# How Point Dutch Sale Mechanics works:

1. Imaging a pile of all token which are to sell
2. Sort all the bids by the price, with the highest on the top
3. Start virtually distribute to the bidders, starting with the highest bid.
4. If all tokens are gone, the price of the bid which is taking the last token from the pile, is the final settlement price
5. Distribute all the tokens for the final settlement price

# Example

1. Pile has 10 token
2. You have 4 bids, in ordered by price: 4 token for $2.5 ($10), 3 token for $2.2 ($6.6), 3 token for $2 ($6),  1 token for 1$ (1$)
3. 
   ```
   10 (pile) - 4 (bid) = 6 (4 token for $2.5)
   6  (pile) - 3 (bid) = 3 (3 token for $2.2)
   3  (pile) - 3 (bid) = 0 (3 token for $2) // all token gone
   ```
4. Pile is gone, so final settlement price is $2
5. Distribute:
   ```
   4 tokens for $2 each, price to pay is $8, $2 back
   3 tokens for $2 each, price to pay is $6, $0.6 back
   3 tokens for $2 each, price to pay is $6, $0 back
   ```

# Drawback

* If not the whole pile is allocated, no current price can be calculated.
* If not the whole pile is sold, no final settlement price can be calculated. (Sold for minimal price)



# Installation


## Run the resolver

```
$ python resolver.py 
```

