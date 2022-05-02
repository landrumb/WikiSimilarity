# %%
import pandas as pd
import os

ENGLISH_WIKIS = ['en', 'en.m']

# looks for pageviews files in the format they appear when downloads from https://dumps.wikimedia.org/other/pageviews/ are unzipped.
datafiles = ["Data/" + f for f in os.listdir('Data') if f.endswith('0000')]
print(f"{len(datafiles)} files found")
# %%
# importing first file to accumulate the others from
all_views = pd.read_csv(datafiles[0], sep=" ", header=None, names=["project", "page", "views", "null"], usecols=["project", "page", "views"])

# filtering to only pages from english wikipedia, both desktop and mobile
en_views = all_views[all_views['project'].isin(ENGLISH_WIKIS)]

# computing views for each page 
en_views = en_views.groupby('page').sum()

en_views.head()
# %% 
for path in datafiles[1:]:
    df = pd.read_csv(path, sep=" ", header=None, names=["project", "page", "views", "null"], usecols=["project", "page", "views"])
    df = df[df['project'].isin(ENGLISH_WIKIS)]
    df = df.groupby('page').sum()
    # merging with previous dataframe
    en_views = en_views.add(df, fill_value=0)
    print(f"{path} added, now {len(en_views):,} pages")


en_views.sort_values('views', ascending=False, inplace=True)
# %% 
# saving to csv
# en_views.iloc[0:(10**5)].to_csv('ten_k_most_viewed_pages.csv', index=True)
# %%
# top 50
en_views.head(50)
# %%
# last 50 of the top 10k
en_views.iloc[(10**5 - 50):(10 ** 5)].head(50)