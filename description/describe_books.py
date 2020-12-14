import pandas as pd
from util.part_a_util import report_if_field_is_unique


def make_copy_df_for_db(dataframe):
    dataframe = dataframe.drop(columns=['Image-URL-S', 'Image-URL-M', 'Image-URL-L'])
    dataframe.dropna(
        axis=0,
        how='any',
        thresh=None,
        subset=["Book-Author"],
        inplace=True
    )
    dataframe_to_db = dataframe
    dataframe_to_db = dataframe_to_db.drop_duplicates(subset='ISBN', keep='first')
    # indexNames = dataframe_to_db[((dataframe_to_db['Year-Of-Publication']) > 9999)].index
    # dataframe_to_db.drop(indexNames, inplace=True)
    dataframe_to_db.to_csv("../migration/books_to_db.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")
    return dataframe_to_db


df_books = pd.read_csv('../data/BX-Books.csv', sep=';', encoding="ISO-8859-1")
# df_users = pd.read_csv('../data/user_tiny.csv', sep=';', encoding="ISO-8859-1")
pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)
print(df_books.head(10))
years = df_books["Year-Of-Publication"].unique().tolist()
print(years)
print("=====COLUMNS/FIELDS=====")
print(df_books.columns, "\n")
df_fields = df_books.columns.tolist()
print("=====SHAPE=====")
print(df_books.shape, "\n")
print("=====DESCRIBE=====")
print(df_books.describe(), "\n")
print("=====INFO=====")
print(df_books.info, "\n")
print("=====MEMORY USAGE=====")
print(df_books.info(memory_usage="deep"), "\n")
print("=====D-TYPES=====")
print(df_books.dtypes, "\n")
print("=====UNIQUES=====")
print("=====WHAT FIELDS ARE UNIQUE??====")
df_books['ISBN'] = df_books['ISBN'].apply(lambda x: x.lower())
report_if_field_is_unique(df_books)
print("\n")
df_users_duplicates = df_books.drop_duplicates()
if df_users_duplicates.shape[0] == df_books.shape[0]:
    print("There are no duplicate records in dataframe")
else:
    print("There are duplicate records in dataframe: \n")
    print("Number of dupicate records: ", df_users_duplicates.shape[0] - df_books.shape[0])
print("\n=====NULL VALUES=====\n")

for field in df_fields:
    df_of_field = df_books[df_books[field].isnull()]
    print("Field ", field, " contains ", df_of_field.shape[0], " null records")
    print(df_of_field.head())

print("LOAD TO CSV")

df_to_db = make_copy_df_for_db(df_books)

print("LOAD TO CSV")
df_books = df_books.drop(columns=['Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L'])

df_books.dropna(
    axis=0,
    how='any',
    thresh=None,
    subset=None,
    inplace=True
)

print(df_books.describe())
print(df_books.shape)