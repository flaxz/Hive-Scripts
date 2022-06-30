import pandas as pd
from hiveengine.api import Api
from hiveengine.tokenobject import Token
import datetime

api = Api()

token = input("Enter token symbol: ")
decPoint = input("Enter decimal point(.or,): ")
getHolders = input("Enter accounts to remove (separate with , and no spaces: ")

holders = api.find_all("tokens", "balances", query = {"symbol": token})

df = pd.DataFrame(holders)
df.drop(columns = ["_id", "pendingUnstake", "delegationsIn", "pendingUndelegations", "stake", "delegationsOut"], inplace = True)

df["balance"] = df["balance"].astype(float)

tk = Token(token)
tokenInfo = tk.get_info()
decNum = tokenInfo["precision"]
df["balance"] = df["balance"].round(decNum)

indexZero = df[df["balance"] == 0.0].index
df.drop(indexZero, inplace = True)
df.drop(columns = ["symbol"], inplace = True)

dropHolders = getHolders.split(',')
while len(dropHolders) >= 1:
  indexHolder = df[df["account"] == dropHolders[0]].index
  df.drop(indexHolder, inplace = True)
  print("Successfully removed:", dropHolders[0])
  del dropHolders[0]

df.sort_values(by=["balance"], inplace = True, ascending = False)

sumBalance = float(df["balance"].sum())
print("Sum balance:", sumBalance, token, "in liquid balance.")

balanceHolders = len(df)
print("Balance Holders:", balanceHolders, token, "balance holders.")

now = datetime.datetime.now()
month = now.strftime("%b")
day = now.strftime("%d")
year = now.strftime("%y")
fileName = token + month + day + year + ".csv"
print("File name:", fileName)

df.to_csv(fileName, decimal = decPoint, index = False)
