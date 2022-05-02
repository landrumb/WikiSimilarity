# %%
import pandas as pd
import os

ENGLISH_WIKIS = ['en', 'en.m']
PAGE_TYPE_REGEX = '^((User)|(Talk)|(Wikipedia)|(Special)|(Portal)):'
N = 10 ** 5
OUTPUT_FILE = 'ten_k_most_viewed_pages.csv'

# looks for pageviews files in the format they appear when downloads from https://dumps.wikimedia.org/other/pageviews/ are unzipped.
datafiles = ["Data/" + f for f in os.listdir('Data') if f.endswith('0000')]
print(f"{len(datafiles)} files found")
# %%
# importing first file to accumulate the others from
all_views = pd.read_csv(datafiles[0], sep=" ", header=None, names=["project", "page", "views", "null"], usecols=["project", "page", "views"])

# filtering to only pages from english wikipedia, both desktop and mobile
en_views = all_views[all_views['project'].isin(ENGLISH_WIKIS)]
# filtering user and talk pages
views = en_views[~(en_views['page'].str.contains(PAGE_TYPE_REGEX, na=False))]

# computing views for each page 
views = views.groupby('page').sum()

print(len(views))
# views.head(50)
# %% 
for path in datafiles[1:]:
    df = pd.read_csv(path, sep=" ", header=None, names=["project", "page", "views", "null"], usecols=["project", "page", "views"])
    df = df[df['project'].isin(ENGLISH_WIKIS)]
    df = df[~(df['page'].str.contains(PAGE_TYPE_REGEX, na=False))]
    df = df.groupby('page').sum()
    # merging with previous dataframe
    views = views.add(df, fill_value=0)
    print(f"{path} added, now {len(views):,} pages")


views.sort_values('views', ascending=False, inplace=True)
# %% 
# saving to csv
views.head(N).to_csv(OUTPUT_FILE, index=True)
# %%
# top 50
views.head(50)
# %%
# last 50 of the top N
views.iloc[(N - 50):(10 ** 5)].head(50)