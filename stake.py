import hiveengine.wallet

name = input('Enter account name: ')

token = input('Enter token symbol: ')

wallet = hiveengine.wallet.Wallet(name).get_token(token)

stake = (wallet['stake'], wallet['delegationsOut'], wallet['pendingUndelegations'])

print('Stake parts: ' + str(stake))

total = 0

for element in stake:

	total += float(element)

print('$%s stake owned by @%s: %s' % (token, name, total))
