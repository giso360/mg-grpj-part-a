import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# Find the k-most similar users for each user
#
# r is the ratings matrix
# k is the number of most similar users
#
# returns: '
#similarUsers: contains the indices of the most similar users to each user
# similarities: is the pairwise similarities, i.e. similarities between users
def findKSimilar (r, k):
    
    # similarUsers is 2-D matrix
    similarUsers=-1*np.ones((nUsers,k))
    
    similarities=cosine_similarity(r)
       
    # for each user
    for i in range(0, nUsers):
        simUsersIdxs= np.argsort(similarities[:,i])
        
        l=0
        #find its most similar users    
        for j in range(simUsersIdxs.size-2, simUsersIdxs.size-k-2,-1):
            simUsersIdxs[-k+1:]
            similarUsers[i,l]=simUsersIdxs[j]
            l=l+1
            
    return similarUsers, similarities
    


# Predict for 'userId', the rating of 'itemId'. 
# A trivial implementation of a collaboarative system
#
#'r': is the ratings matrix
#'userId': is the userId, and 
#'itemID': is the item id    
#'similarUsers': contains for each user his most similar users
#'similarities': are th pairwise cosine similarities between the users
# returns the prediction.     
def predict(userId, itemId, r,similarUsers,similarities):

    # number of neighbours to consider
    nCols=similarUsers.shape[1]
    
    sum=0.0;
    simSum=0.0;
    for l in range(0,nCols):    
        neighbor=int(similarUsers[userId, l])
        #weighted sum
        sum= sum+ r[neighbor,itemId]*similarities[neighbor,userId]
        simSum = simSum + similarities[neighbor,userId]
    
    return  sum/simSum
    
    
    


nUsers=4
nItems=4
r=np.array([[3,0,3,3],[5,4,0,2],[1,2,4,2],[2,2,0,1]])
#r=np.random.rand(nUsers, nItems)

similarUsers, similarities=findKSimilar (r,2)

mae=0
for i in range(0,nUsers):
    for j in range(0, nItems):
        rhat=predict (i,j,r, similarUsers, similarities)
        print ('prediction, real',rhat,r[i,j])
        mae=mae+np.abs(rhat-r[i,j])
print ('MAE=',mae)