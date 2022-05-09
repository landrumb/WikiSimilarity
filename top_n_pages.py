# %%
import pandas as pd
import os
import requests
import gzip
from faker import Faker
import datetime
import warnings

ENGLISH_WIKIS = ['en', 'en.m']
PAGE_TYPE_REGEX = '^((User)|(Talk)|(Wikipedia)|(Special)|(Portal)):'
N = 10 ** 5
OUTPUT_FILE = 'ten_k_most_viewed_pages.csv'
DATA_DIR = 'testdata'
RANDOM_FILES = 1000 # Number of random files to generate

fake = Faker()

# suppressing a warning caused by use of match groups in a regex 
warnings.filterwarnings('ignore', message="This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.")

# looks for pageviews files in the format they appear when downloaded from https://dumps.wikimedia.org/other/pageviews/ 
datafiles = [DATA_DIR + "/" + f for f in os.listdir(DATA_DIR)]
print(f"{len(datafiles)} files found")
if len(datafiles) == 0:
    print("downloading an initial file")
    # generate a random datetime for which there exists a pageview file
    date = fake.date_time_between(start_date=datetime.datetime(year=2015, month=5, day=1, hour=1), end_date='now')

    # get the url of the corresponding pageview file
    url = f"https://dumps.wikimedia.org/other/pageviews/{date.year}/{date.year}-{date.month:02d}/pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz"

    # download and save the file
    r = requests.get(url)
    with open(DATA_DIR + "/" + f"pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz", 'wb') as f:
        f.write(r.content)
    
    datafiles = [DATA_DIR + "/" + f"pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz"]
    RANDOM_FILES -= 1 # modifying constants is a convenient abuse of the fact they don't properly exist in python
# %%
# importing first file to accumulate the others from
all_views = pd.read_csv(datafiles[0], sep=" ", header=None, names=["project", "page", "views", "null"], usecols=["project", "page", "views"])

# filtering to only pages from english wikipedia, both desktop and mobile
en_views = all_views[all_views['project'].isin(ENGLISH_WIKIS)]
# filtering user and talk pages
views = en_views[~(en_views['page'].str.contains(PAGE_TYPE_REGEX, na=False))]

# computing views for each page 
views = views.groupby('page').sum()

print(f"{len(views):,}")
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
# %%
print("getting random files")
start_time = datetime.datetime.now()
for i in range(RANDOM_FILES):
    # generate a random datetime for which there exists a pageview file
    date = fake.date_time_between(start_date=datetime.datetime(year=2015, month=5, day=1, hour=1), end_date='now')

    # get the url of the corresponding pageview file
    url = f"https://dumps.wikimedia.org/other/pageviews/{date.year}/{date.year}-{date.month:02d}/pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz"

    # download and save the file
    r = requests.get(url)
    with open(DATA_DIR + "/" + f"pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz", 'wb') as f:
        f.write(r.content)
    print(f"{date.strftime('%Y/%m/%d:%H')}")
    # read the file (pandas can handle gzip directly) and perform same operations as above
    try:
        df = pd.read_csv(DATA_DIR + "/" + f"pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz", compression='gzip', sep=" ", header=None, names=["project", "page", "views", "null"], usecols=["project", "page", "views"])
    except: # handling error caused by pandas' "C" CSV engine
        print(f"{date.strftime('%Y/%m/%d:%H')} failed" )
        os.remove(DATA_DIR + "/" + f"pageviews-{date.strftime('%Y%m%d')}-{date.hour:02d}0000.gz")
        continue
    df = df[df['project'].isin(ENGLISH_WIKIS)]
    df = df[~(df['page'].str.contains(PAGE_TYPE_REGEX, na=False))]
    df = df.groupby('page').sum()
    # merging with previous dataframe
    views = views.add(df, fill_value=0)
    print(f"[{len(datafiles) + i + 1}]\t{date.strftime('%Y/%m/%d:%H')}\t{len(views):,} pages\t[{datetime.datetime.now() - start_time} elapsed, {(i * 100) // RANDOM_FILES}% complete, {(datetime.timedelta(seconds=((datetime.datetime.now() - start_time).total_seconds() / (i + 1)) * (RANDOM_FILES - i - 1)))} remaining]")

views.sort_values('views', ascending=False, inplace=True)

print(f"A total of {len(datafiles) + RANDOM_FILES:,} files were used to generate the data")
# %% 
# saving to csv
# views.head(N).to_csv(OUTPUT_FILE, index=True)
# %%
# top 50
views.head(50)
# %%
# last 50 of the top N
views.iloc[(N - 50):(10 ** 5)].head(50)