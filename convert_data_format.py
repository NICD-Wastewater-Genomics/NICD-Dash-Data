import pandas as pd

df2 = pd.read_csv("merged_data.tsv",sep='\t',index_col=0)

df2['Sample'] = df2.index
df2 = df2.rename(columns={"SampleCollectionDate":"Date","SiteProvince": "Province",
                            "DistrictName": "District","SiteName":"Site"})

# Convert the 'lineages' column to a list of lists
df2['Lineages'] = df2['Lineages'].apply(lambda x: x.split() if isinstance(x, str) else [])

# Convert the 'abundances' column to a list of lists
df2['Abundances'] = df2['Abundances'].apply(lambda x: x.replace('[','').replace(']',''))
df2['Abundances'] = df2['Abundances'].apply(lambda x: [float(val) for val in x.split(',')] if isinstance(x, str) else [])

# Explode the 'lineages' and 'abundances' columns to separate rows
df2_exploded = df2.explode(['Lineages','Abundances'])
# Reset the index after exploding
df2_exploded = df2_exploded.reset_index(drop=True)

df2_exploded.to_feather('merged_data_exploded.feather')

### convert the rest of the files to feather format. 
df = pd.read_csv("rsa_cases_vs_levels.csv")
df.to_feather('rsa_cases_vs_levels.feather')
df = pd.read_csv("NICD_monthly.csv",index_col=0)
df.to_feather('NICD_monthly.feather')
df = pd.read_csv("NICD_daily_smoothed.csv",index_col=0)
df.to_feather('NICD_daily_smoothed.feather')
df = pd.read_csv("provincial_cases_vs_levels.csv")
df.to_feather('provincial_cases_vs_levels.feather')
