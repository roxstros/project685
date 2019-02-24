import pandas as pd
import numpy as np
df = pd.read_csv("sp500_testdata_2.csv")

df["TR"] = ""
df.TR.loc[0] = df.high.loc[0] - df.low.loc[0]    # Initial value for TR
df.TR.loc[1:] = ""
df["N"] = ""
df["N"].loc[0] = df.high.loc[0] - df.low.loc[0]   # Initial value for N
df["N"].loc[1:] = ""
df["NPP"] = ""
df.NPP.loc[0] = 0.00     # Initial value for NPP
df["FL"] = ""
df["SL"] = ""
df.FL.loc[0] = 0.00      # Initial value for FL
df.SL.loc[0] = 0.00      # Initial value for SL
df["Sep"] = ""           # Percentage separation between FL and SL
df.Sep.loc[0] = 0.00
df["TrendDir"] = ""
df["TrendDir"] = df["TrendDir"].astype('str')
df["TrendDay"] = ""
df["FE_FL"] = ""
# df.FE_FL.round(3)
df["AE_FL"] = ""
df["SP"] = ""
df["En_price1"] = ""
df["Position"] = ""
df["Counter1"] = ""
df["Counter2"] = ""
df["a"] = ""
df["b"] = ""
df["c"] = ""
df["RE_CAN"] = ""
# df["EnP2_RE"] = ""
df["En_price2"] = ""
df["Ex_price1"] = ""
df["Ex_price2"] = ""
df["Ex_price3"] = ""
df["Ex_price4"] = ""
df["Ex_price5"] = ""
df["P_L"] = ""

df[["TR", "N", "NPP", "FL", "SL", "Sep", "FE_FL", "AE_FL", "SP", "En_price1", "Position", "a", "b", "c", "En_price2", "Ex_price1", "Ex_price2", "Ex_price3", "Ex_price4", "Ex_price5", "P_L"]] = df[["TR", "N", "NPP", "FL", "SL", "Sep", "FE_FL", "AE_FL", "SP", "En_price1", "Position", "a", "b", "c", "En_price2", "Ex_price1", "Ex_price2", "Ex_price3", "Ex_price4", "Ex_price5", "P_L"]].apply(pd.to_numeric)

df.dtypes

#  3 'for' loops:
#   a) calculate True Range for every row after the first row
#   b) calculate N for every row after the first row
#   c) calculate NPP for every row after first row


# a)
#  True Range = max( absolute value(H - L), absolute value (H - C(previous)), absoulute value (C(previous) - L))
rownum = 1
for rownum in range(1,1500):
    df.TR.loc[rownum:] = max(abs(df.high.loc[rownum] - df.low.loc[rownum]), abs(df.high.loc[rownum] - df.close.loc[rownum-1]), abs(df.close.loc[rownum-1] - df.low.loc[rownum]))
    rownum += 1

#  b)
#  N = N(previous) + (TR-N(previous)) / (0.5 * 20 + 1)
Constant = 20
rownum = 1
for rownum in range(1, 1500):
    df.N.loc[rownum:] = df.N.loc[rownum - 1]+(df.TR.loc[rownum]-df.N.loc[rownum - 1])/(0.5 * (Constant + 1))
    rownum +=1

# c)
df.NPP.loc[rownum:].round(3)
rownum = 1
for rownum in range(1, 1500):
    df.NPP.loc[rownum:] = df.N.loc[rownum]/df.close.loc[rownum-1] * 100
    rownum += 1

# try replacing this with a List Comprehension
# [df.NPP.loc[rownum:] for df.NPP.loc[rownum] in range(1.599) if df.NPP.loc[rownum] is float]

# 3 min 42 sec to finish execution on 1500 rows
# 'for' loop that yields FL values after index position zero

rownum = 1
FL_period = 7
for rownum in range(1, 1500):
    df.FL.loc[rownum:] = df.FL.loc[rownum-1] + (df.close.loc[rownum] - df.FL.loc[rownum-1])/((FL_period+1)/2)
    rownum += 1

# 'for' loop that yields SL values after index position zero

rownum = 1
SL_period = 20
for rownum in range(1, 1500):
    df.SL.loc[rownum:] = df.SL.loc[rownum-1] + (df.close.loc[rownum] - df.SL.loc[rownum-1])/((SL_period+1)/2)
    rownum += 1

# 'for' loop that yields Separation between FL and SL

rownum = 1
for rownum in range(1, 1500):
    df.Sep.loc[rownum] = (df.FL.loc[rownum] - df.SL.loc[rownum])/df.SL.loc[rownum] * 100
    rownum += 1


# Determining TrendDir based on boolean result for question: FL > SL ?
# start at index = 25 to give ramp-up time for lags
rownum = 100
for rownum in range(25, 1500):
    if df.FL.loc[rownum] > df.SL.loc[rownum]:
        df.TrendDir.loc[rownum] = "Up"
    else:
        df.TrendDir.loc[rownum] = "Down"
rownum += 1

# iterate through rows starting at row 101 to find where trends initiate (TrendDay=0) and continue (TrendDay>0)

rownum = 101           # start at index = 101 (TrendDay at index=100 is set to 0)
for rownum in range(25, 1500):
    if df.TrendDir.loc[rownum] == df.TrendDir.loc[rownum-1]:
        df.TrendDay.loc[rownum] = (df.TrendDay.loc[rownum-1] + 1)
    else:
        df.TrendDay.loc[rownum] = 0
rownum += 1




# 1 min 23 sec to finish execution on 1500 rows

rownum = 25   # start after series for TrendDay transitions from blank (string value) to int
for rownum in range(25, 1500):
    if df.TrendDay.loc[rownum] == 0:
        df.FE_FL.loc[rownum] = ""
        df.AE_FL.loc[rownum] = ""
    else:
        if df.TrendDir.loc[rownum] == "Up":

            #Favorable Excursion from FL in terms of N for long position:
            if df.high.loc[rownum] < df.FL.loc[rownum-1]:
                df.FE_FL.loc[rownum] = 0
            else:
                df.FE_FL.loc[rownum] = (df.high.loc[rownum] - df.FL.loc[rownum-1])/df.N.loc[rownum-1]

            #Adverse Excursion from FL in terms of N for for long position (display positive value):
            if df.low.loc[rownum] > df.FL.loc[rownum-1]:
                df.AE_FL.loc[rownum] = 0
            else:
                df.AE_FL.loc[rownum] = abs((df.low.loc[rownum] - df.FL.loc[rownum-1])/df.N.loc[rownum-1])

        elif df.TrendDir.loc[rownum] == "Down":

            #Favorable Excursion from FL in terms of N for Short position:
            if df.low.loc[rownum] > df.FL.loc[rownum-1]:
                df.FE_FL.loc[rownum] = 0
            else:
                df.FE_FL.loc[rownum] = (df.FL.loc[rownum-1] - df.low.loc[rownum])/df.N.loc[rownum-1]

            #Adverse Excursion from FL in terms of N for for Short position (display positive value):
            if df.high.loc[rownum] < df.FL.loc[rownum-1]:
                df.AE_FL.loc[rownum] = 0
            else:
                df.AE_FL.loc[rownum] = abs((df.FL.loc[rownum-1] - df.high.loc[rownum])/df.N.loc[rownum-1])

# increment to next bar
rownum += 1




df["SP"].fillna("", inplace = True)
df["En_price1"].fillna("", inplace = True)
df["Position"].fillna("", inplace = True)
df["Counter1"].fillna("", inplace = True)
df["Counter2"].fillna("", inplace = True)
df["a"].fillna("", inplace = True)
df["b"].fillna("", inplace = True)
df["c"].fillna("", inplace = True)
df["RE_CAN"].fillna("", inplace = True)
df["En_price2"].fillna("", inplace = True)
# df["EnP2_RE"].fillna("", inplace = True)
df["Ex_price1"].fillna("", inplace = True)
df["Ex_price2"].fillna("", inplace = True)
df["Ex_price3"].fillna("", inplace = True)
df["Ex_price4"].fillna("", inplace = True)
df["Ex_price5"].fillna("", inplace = True)
df["P_L"].fillna("", inplace = True)


# df[["FE_FL", "AE_FL", "TrendDay", "Counter1", "Counter2", "Position","a", "b", "c", "SP", "En_price1", "En_price2", "Ex_price1", "Ex_price2", "RE_CAN", "Ex_price3", "Ex_price4", "Ex_price5", "P_L"]] = df[["FE_FL", "AE_FL", "TrendDay", "Counter1", "Counter2", "Position", "a", "b", "c", "SP", "En_price1", "En_price2", "Ex_price1", "Ex_price2", "RE_CAN", "Ex_price3", "Ex_price4", "Ex_price5", "P_L"]].apply(pd.to_numeric)
# pd.to_numeric(df["TrendDay", "Counter1", "Counter2"], downcast='integer'))


df.iloc[260:320, 10:33].round({'N': 2, 'NPP': 3, 'FL': 2, 'SL': 2, 'Sep': 2, 'FE_FL': 3, 'AE_FL': 3})








#  daily Volatility Impact functions (Risk Management)

def AP_U():                                                     # Add Position
        if df.NPP.loc[rownum - 1] <= addpos["L"]["1"]:
            return df.FL.loc[rownum - 1] +  X * df.N.loc[rownum - 1]   # NPP=1.10% or less: add position if price retraces 25%N ABOVE FL
        elif df.NPP.loc[rownum - 1] <= addpos["L"]["2"]:
            return df.FL.loc[rownum - 1]                       # NPP=1.50% to 1.10%: add position if price retraces back to FL
        elif df.NPP.loc[rownum - 1] <= addpos["L"]["3"]:
            return df.FL.loc[rownum - 1] - 5 * X * df.N.loc[rownum - 1]   # NPP=1.95% to 1.50%: add position if price retraces back 125%N below FL
        else:
            return df.FL.loc[rownum - 1] - 6.4 * X * df.N.loc[rownum - 1]   # NPP>1.95%: add position if price retraces 160%N below FL

def AP_D():
        if df.NPP.loc[rownum - 1] < addpos["S"]["1"]:
            return df.FL.loc[rownum - 1] - X * df.N.loc[rownum - 1]   # NPP=1.10% or less: add position at 25%N retracement BELOW FL
        elif df.NPP.loc[rownum - 1] >= addpos["S"]["2"]:
            return df.FL.loc[rownum - 1]                      # NPP=1.50% to 1.10%: add position if price retraces back to FL
        elif df.NPP.loc[rownum - 1] >= addpos["S"]["3"]:
            return df.FL.loc[rownum - 1] + 6 * X * df.N.loc[rownum - 1]    # NPP=1.95% to 1.50%: add position if price retraces 150%N above FL
        else:
            return df.FL.loc[rownum - 1] + 7 * X * df.N.loc[rownum - 1]    # NPP>1.95%: add position if price retraces 175%N above FL


def SL_U():                                                         # Stop Loss - must space SL  proportional to AP
        if df.NPP.loc[rownum - 1] <= stoploss["L"]["1"]:
            return df.FL.loc[rownum - 1] - df.N.loc[rownum - 1]     # stop loss when price retraces 1N below FL
        elif df.NPP.loc[rownum - 1] <= stoploss["L"]["2"]:
            return df.FL.loc[rownum - 1] - 6 * X * df.N.loc[rownum - 1]  # stop loss when price retraces 150%N below FL
        elif df.NPP.loc[rownum - 1] <= stoploss["L"]["3"]:
            return df.FL.loc[rownum - 1] - 7 * X * df.N.loc[rownum - 1]   # stop loss when price retraces  175%N below FL
        else:
            return df.FL.loc[rownum - 1] - 8 * X * df.N.loc[rownum - 1]   # stop loss when price retraces 200%N below FL

def SL_D():
        if df.NPP.loc[rownum - 1] < SL["S"]["1"]:
            return df.FL.loc[rownum - 1] + 5 * X * df.N.loc[rownum - 1]      # stop loss when price retraces 125%N above FL
        elif df.NPP.loc[rownum - 1] >= SL["S"]["2"]:
            return df.FL.loc[rownum - 1] + 6.4 * X * df.N.loc[rownum - 1]      # stop loss when price retraces 160%N (6.4*x) above FL
        elif df.NPP.loc[rownum - 1] >= SL["S"]["3"]:
            return df.FL.loc[rownum - 1] + 7 * X * df.N.loc[rownum - 1]      # stop loss when price retraces 175%N above FL
        else:
            return df.FL.loc[rownum - 1] + 8 * X * df.N.loc[rownum - 1]      # stop loss when price retraces 200%N above FL


def TP_U():                                                # Take Profit
        if df.NPP.loc[rownum - 1] <= takeprof["L"]["1"]:
            return df.FL.loc[rownum - 1] + 5 * X * df.N.loc[rownum - 1]   # for NPP < 1.10%: take profit when price exceeds 125%N above previous FL
        elif df.NPP.loc[rownum - 1] <= takeprof["L"]["2"]:
            return df.FL.loc[rownum - 1] + 5.6 * X * df.N.loc[rownum - 1]    # for NPP < 1.50%: take profit when price exceeds 140%N (5.6 * X) above previous FL
        elif df.NPP.loc[rownum - 1] <= takeprof["L"]["3"]:
            return df.FL.loc[rownum - 1] + 7 * X * df.N.loc[rownum - 1]    # for NPP < 1.95%: take profit when price exceeds 175%N (7*X*N) above previous FL
        else:
            return df.FL.loc[rownum - 1] + 7.5 * X * df.N.loc[rownum - 1]     # for NPP > 1.95%: take profit when price exceeds 188%N (7.5*X*N) above previous FL

def TP_D():
        if df.NPP.loc[rownum - 1] < takeprof["S"]["1"]:
            return df.FL.loc[rownum - 1] - 5 * X * df.N.loc[rownum - 1]     # for NPP < 1.05%: take profit when price exceeds 1.5N (6*0.25N) below previous FL
        elif df.NPP.loc[rownum - 1] >= takeprof["S"]["2"]:
            return df.FL.loc[rownum - 1] - 5.6 * X * df.N.loc[rownum - 1]       # for NPP < 1.30%: take profit when price exceeds 1.25N (5*0.25N) below previous FL
        elif df.NPP.loc[rownum - 1] >= takeprof["S"]["3"]:
            return df.FL.loc[rownum - 1] - 7.5 * X * df.N.loc[rownum - 1]
        else:
            return df.FL.loc[rownum - 1] - 8 * X * df.N.loc[rownum - 1]    # for NPP > 1.95%: take profit when price exceeds 200%N (8*X*N) below previous FL


def RE_U():                                                    # Re-enter trend after AP, SL, or TP
        if df.NPP.loc[rownum - 1] <= re_entry["L"]["1"]:
            return df.FL.loc[rownum - 1] + 0.5 * X * df.N.loc[rownum - 1]   # Re-enter when price retraces within 12.5%N above FL
        elif df.NPP.loc[rownum - 1] <= re_entry["L"]["2"]:
            return df.FL.loc[rownum - 1] + 0.5 * X * df.N.loc[rownum - 1]   # Re-enter when price retraces within 12.5%N above FL
        elif df.NPP.loc[rownum - 1] <= re_entry["L"]["3"]:
            return df.FL.loc[rownum - 1] - 2 * X * df.N.loc[rownum - 1]     # Re-enter when price retraces below 50%N below FL
        else:
            return df.FL.loc[rownum - 1] - 2.25 * X * df.N.loc[rownum - 1]  #  RE-enter when price retraces below 56%N below FL

def RE_D():
        if df.NPP.loc[rownum - 1] < RE["S"]["1"]:
            return df.FL.loc[rownum - 1] - 0.25 * X * df.N.loc[rownum - 1]  # get back in when price approaches 6%N still below FL
        elif df.NPP.loc[rownum - 1] >= RE["S"]["2"]:
            return df.FL.loc[rownum - 1]                                   # get back in when price retraces to the FL
        elif df.NPP.loc[rownum - 1] >= RE["S"]["3"]:
            return df.FL.loc[rownum - 1] + 4 * X * df.N.loc[rownum - 1]    # get back in when price retraces 100%N above FL
        else:
            return df.FL.loc[rownum - 1] + 5 * df.N.loc[rownum - 1]  #get back in when price retraces 125%N above FL



tick = input("The minimum tick for this contract is: ")
tick = float(tick)
print("Tick is:", float(tick))
tick_val = input("The USD value for a tick is: ")
tick_val = float(tick_val)
print("Each tick is: $", float(tick_val))
rownum = input("Start with this rownum: ")
print("Analysis code starts with row ", rownum)

type(tick)
type(tick_val)
type(SP)


addpos = {"L" : {"1" : 1.10, "2" : 1.50, "3" : 1.95},                            # syntax to call, enter script as follows:
          "S" : {"1" : 1.10, "2" : 1.50, "3" : 1.95}                             # AP["L"]["2"]  yields: 0.015
          }                                                                        # SL["S"]["3"]  yields: 0.0195

stoploss = {"L" : {"1" : 1.10, "2" : 1.50, "3" : 1.95},
            "S" : {"1" : 1.10, "2" : 1.50, "3" : 1.95}
            }

takeprof = {"L" : {"1" : 1.10, "2" : 1.50, "3" : 1.95},
            "S" : {"1" : 1.10, "2" : 1.50, "3" : 1.95}
            }

re_entry = {"L" : {"1" : 1.10, "2" : 1.50, "3" : 1.95},
            "S" : {"1" : 1.10, "2" : 1.50, "3" : 1.95}
            }

#tick = 0.25
#tick_val = 12.50
#rownum = 10

X = 0.25   # General Risk Mgmt. multiplier
for rownum in range(1, 1500):
    if df.TrendDay.loc[rownum] == 0 and df.TrendDir.loc[rownum] == "Up":
        SP = df.high.loc[rownum]                            # assign the 'high' slice to the SP variable
        df.SP.loc[rownum] = SP                              # equate the SP slice with the SP variable
        rownum += 1
        while df.TrendDay.loc[rownum] > 0:              # this 'while' loop finds initial entry, records initial P_L, then advances to next day
            if df.high.loc[rownum] > SP:
                En_price1 = SP + tick
                df.En_price1.loc[rownum] = En_price1
                df.Counter1.loc[rownum] = 1                  # initialize Counter1
                df.Position.loc[rownum] = 1                  # 'position' variable
                # df.Position.loc[rownum] = Position         # this [rownum] dataframe slice equal to this [rownum] value for position variable
                df.P_L.loc[rownum] = df.close.loc[rownum] - En_price1        # yes, you can add a value contained in dataframe slice with a local variable that's a float!
                rownum += 1
                break
            else:
                SP = df.high.loc[rownum]
                df.SP.loc[rownum] = SP
                rownum += 1

        while df.TrendDay.loc[rownum] > 0:
            a = AP_U()
            b = SL_U()
            c = TP_U()

            # case 1: price retraces - look to add to initial position
            if df.Position.loc[rownum] == 1 and df.low.loc[rownum] < a:
                En_price2 = a - tick
                df.En_price2.loc[rownum] = En_price2
                df.Counter1.loc[rownum] = df.Counter1.loc[rownum-1] + 1
                df.Counter2.loc[rownum] = 1
                df.Position.loc[rownum] = 2
                df.P_L.loc[rownum] = (df.close.loc[rownum] - En_price1) + (df.close.loc[rownum] - En_price2)
                rownum += 1
                continue

            # case 2:  take profit on initial position
            elif df.Position.loc[rownum] == 1 and df.high.loc[rownum] > c:
                Ex_price1 = c + tick
                df.Ex_price1.loc[rownum] = Ex_price1
                df.Counter1.loc[rownum] = 0
                df.Position.loc[rownum] = 0
                RE_CAN = True
                df.RE_CAN.loc[rownum] = RE_CAN
                df.P_L.loc[rownum] = Ex_price1 - En_price1
                rownum += 1
                continue

            # case 3:  take profit on two positions
            elif df.Position.loc[rownum] == 2 and df.high.loc[rownum] > c:
                Ex_price1 = c + tick
                Ex_price2 = c + tick
                df.Counter1.loc[rownum] = 0
                df.Counter2.loc[rownum] = 0
                df.Position.loc[rownum] = 0
                RE_CAN = True
                df.RE_CAN.loc[rownum] = RE_CAN
                df.P_L.loc[rownum] = (Ex_price1 - En_price1) + (Ex_price2 - En_price2)
                rownum += 1
                continue

             # case 4:  RM functions do not impact initial position so carry to next day
            elif df.Position.loc[rownum] == 1 and df.high.loc[rownum] <=c and df.low.loc[rownum] >= a:
                df.Counter1.loc[rownum] = df.Counter1.loc[rownum-1] + 1
                df.Position.loc[rownum] = 1
                df.P_L.loc[rownum] = df.close.loc[rownum] - En_price1
                rownum += 1
                continue

            # case 5: RM functions do no impact position with TWO contracts so carry to next day
            elif df.Position.loc[rownum] == 2 and df.high.loc[rownum] <= c and df.low.loc[rownum] >= a:
                df.Counter1.loc[rownum] = df.Counter1.loc[rownum-1] + 1
                df.Counter2.loc[rownum] = df.Counter2.loc[rownum-1] + 1
                df.Position.loc[rownum] = 2
                df.P_L.loc[rownum] = (df.close.loc[rownum] - En_price1) + (df.close.loc[rownum] - En_price2)
                rownum += 1
                continue

            # case 6:  zero positions due to TP trigger and looking for Re-entry on TWO positions
            elif df.Position.loc[rownum] == 0 and df.RE_CAN.loc[rownum] == True:
                d = RE_U()
                if low <= d:
                    En_price1 = d
                    En_price2 = d
                    df.En_price1.loc[rownum] = En_price1
                    df.En_price2_AP.loc[rownum] = En_price2
                    df.Counter1.loc[rownum] = 1
                    df.Counter2.loc[rownum] = 1
                    df.Position.loc[rownum] = 2
                    df.P_L.loc[rowum] = df.close.loc[rownum] - En_price1 + df.close.loc[rownum] - En_price2
                    RE_CAN = False
                    df.RE_CAN.loc[rownum] = RE_CAN
                    rownum += 1
                else:
                    df.RE_CAN.loc[rownum] = df.RE_CAN.loc[rownum-1]
                    continue

            # case 7:  stop out both positions and iterate until next TrendDay=0 instance
            elif df.Position.loc[rownum] == 2 and df.low.loc[rownum] < b:
                Ex_price3 = b - tick
                Ex_price4 = b - tick
                df.Ex_price3.loc[rownum] = Ex_price3
                df.Ex_price4.loc[rownum] = Ex_price4
                #SL = True
                df.P_L.loc[rownum] = (Ex_price3 - En_price1) + (Ex_price4 - En_price2)
                rownum += 1
                while df.TrendDay.loc[rownum] != 0:
                    rownum += 1
                break
            break

    else:
        rownum += 1
