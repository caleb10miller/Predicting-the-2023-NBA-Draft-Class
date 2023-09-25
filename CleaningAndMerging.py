import pandas as pd

# combine PER files

PER = pd.concat(map(pd.read_csv, ['PER.csv', 'PER2.csv', 'PER3.csv', 'PER4.csv']))
PER = PER.reset_index(drop=True)

# drop dnp, crash, and duplicates
DNP = PER.loc[PER['PER'] == 'DNP'].index
CRASH = PER.loc[PER['PER'] == 'CRASH'].index
PER = PER.drop(DNP)
PER = PER.drop(CRASH)
DUPLICATES = PER.loc[PER.duplicated() == True].index
PER = PER.drop(DUPLICATES)

AGE = pd.concat(map(pd.read_csv ,['NBAStats.csv']))
AGE.drop_duplicates(subset=['Names'],inplace=True)

# combine college stats files

College = pd.concat(map(pd.read_csv, ['CollegeStats.csv', 'CollegeStats2.csv', 'CollegeStats3.csv', 'CollegeStats4.csv']))
College = College.reset_index(drop=True)

# remove dnp and missing stats

DNP = College[College.Games == 'DNP'].index
College = College.drop(DNP)

NoThreeTracked = College[College['3pa'].isna()].index
College = College.drop(NoThreeTracked)
College['3p%'] = College['3p%'].fillna(0)

NoOffRebTracked = College[College['OffRebounds'].isna()].index
# 404 players played at a time where offensive rebounds were not tracked. Removing these rows would make our dataset too small.
# To combat this, offensive rebounds will be dropped
College = College.drop('OffRebounds', axis=1)
College = College.reset_index(drop=True)

# combine files into one df

MergedDf = pd.merge(PER, AGE, on='Names')
FinalDf = pd.merge(MergedDf, College, on='Names')
FinalDf.drop_duplicates(subset=['Names'], inplace=True)
FinalDf.to_csv('FinalData.csv', index=False, encoding='utf-8')