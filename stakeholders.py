import pandas as pd
from hiveengine.api import Api
from hiveengine.tokenobject import Token
import datetime

api = Api()

token = input("Enter staked token symbol: ")
decPoint = input("Enter decimal point(.or,): ")

def main():
  
  holders = api.find_all("tokens", "balances", query = {"symbol": token})
  
  df = pd.DataFrame(holders)
  df.drop(columns = ["_id", "balance", "pendingUnstake", "delegationsIn"], inplace = True)
  
  df["pendingUndelegations"] = df["pendingUndelegations"].astype(float)
  df["stake"] = df["stake"].astype(float)
  df["delegationsOut"] = df["delegationsOut"].astype(float)
  
  df = df.assign(ownedStake = df.sum(axis = 1, numeric_only = True))
  
  tk = Token(token, api = api)
  tokenInfo = tk.get_info()
  decNum = tokenInfo["precision"]
  df["ownedStake"] = df["ownedStake"].round(decNum)
  
  indexZero = df[df["ownedStake"] == 0.0].index
  df.drop(indexZero, inplace = True)
  df.drop(columns = ["symbol", "stake", "delegationsOut", "pendingUndelegations"], inplace = True)
  
  df.sort_values(by=["ownedStake"], inplace = True, ascending = False)
  
  sumStake = float(df["ownedStake"].sum().round(decNum))
  print("Sum stake:", sumStake, token, "staked.")
  
  stakeHolders = len(df)
  print("Stake Holders:", stakeHolders, token, "stake holders.")
  
  now = datetime.datetime.now()
  month = now.strftime("%b")
  day = now.strftime("%d")
  year = now.strftime("%y")
  fileName = "ownedStake" + token + "-" + month + day + year + ".csv"
  print("File name:", fileName)
  
  df.to_csv(fileName, decimal = decPoint, index = False)
  
if __name__ == "__main__":
  
  main()
