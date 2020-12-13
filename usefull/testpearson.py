import pandas as pd
import numpy as np
from util.PearsonsMetric import PearsonsMetric

df = pd.read_csv("./testusers.csv")
# result from sql for users
users = [100,101,102,103]
# result from sql for isbns
isbns = ["1111x", "1112x", "1113x", "1114x"]
df_out = pd.DataFrame(index=users, columns=isbns)
# opportunity fillna !!!
for index, row in df.iterrows():
    df_out.loc[row["userid"], row["isbn"]] = row["rating"]

df_out = df_out.fillna(value=0)

nUsers = len(users)
nItems = len(isbns)


def findKSimilar2(r, k):
    # similarUsers is 2-D matrix
    similarities = np.ones((nUsers, nUsers))
    similarUsers = -1 * np.ones((nUsers, k))
    counter = 0
    for i in range(0, nUsers - 1):
        for j in range(i, nUsers):
            sim = np.corrcoef(r[i], r[j])[0][1]
            similarities[i][j] = sim
            similarities[j][i] = sim
    for i in range(0, nUsers):
        simUsersIdxs = np.argsort(similarities[:, i])
        l = 0
        # find its most similar users
        for j in range(simUsersIdxs.size - 2, simUsersIdxs.size - k - 2, -1):
            simUsersIdxs[-k + 1:]
            similarUsers[i, l] = simUsersIdxs[j]
            l = l + 1
    return similarUsers, similarities


def findKSimilarPearson(r, k):
    # similarUsers is 2-D matrix
    similarities = np.ones((nUsers, nUsers))
    similarUsers = -1 * np.ones((nUsers, k))
    counter = 0
    for i in range(0, nUsers - 1):
        for j in range(i, nUsers):
            sim = PearsonsMetric(r[i], r[j]).get_pearson()
            similarities[i][j] = sim
            similarities[j][i] = sim
    for i in range(0, nUsers):
        simUsersIdxs = np.argsort(similarities[:, i])
        l = 0
        # find its most similar users
        for j in range(simUsersIdxs.size - 2, simUsersIdxs.size - k - 2, -1):
            simUsersIdxs[-k + 1:]
            similarUsers[i, l] = simUsersIdxs[j]
            l = l + 1
    return similarUsers, similarities



r = df_out.to_numpy()

# similarUsers, similarities = findKSimilar2(r, 2)
similarUsers, similarities = findKSimilarPearson(r, 2)








