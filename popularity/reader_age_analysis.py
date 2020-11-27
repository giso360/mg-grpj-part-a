import pandas as pd


df_reader_age_analysis = pd.read_csv('../data/rating_matrix.csv', sep=';', encoding="ISO-8859-1")
# df_reader_age_analysis = pd.read_csv('../data/rate_tiny.csv', sep=';', encoding="ISO-8859-1")

print(df_reader_age_analysis.dtypes)
df_reader_age_analysis.Age = df_reader_age_analysis.Age.astype('int64')
print(df_reader_age_analysis.dtypes)

print(df_reader_age_analysis["Age"].min())
print(df_reader_age_analysis["Age"].max())

print(sorted(df_reader_age_analysis["Age"].unique().tolist()))
print(df_reader_age_analysis.shape)

# https://www.reddit.com/r/learnpython/comments/73z4e2/pandas_groupby_or_cut_dataframe_to_bins/

bins = pd.cut(df_reader_age_analysis["Age"], [*range(0, 121, 10)])

df = df_reader_age_analysis.groupby(bins)["Age"].agg(["count"])

print(df.head(100))


# Need Histogram
df.hist()
df.plot.hist()