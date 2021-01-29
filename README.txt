Z A C K S

This service publishes the tickers that have ANY news in a given day, together with their Zacks signal.
I don't personally believe in Zacks tbhfam.

How it works:
1. Get a list of NYSE tickers
2. For each ticker, dl from zacks research the news, the date and the level (1,2,3 wanted, 4,5 not)
3. Do one pass through all symbols and only save those that have *any* level.
4. Periodically go through left-over symbols and update website.

Note:
nasdaqlisted and otherlisted are from the official Nasdaq ftp server:
https://quant.stackexchange.com/questions/1640/where-to-download-list-of-all-common-stocks-traded-on-nyse-nasdaq-and-amex
