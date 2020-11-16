import sys
import numpy as np
import book_popularity

sys.path.append('../popularity')

# 5. Book Outliers:
# # 	i. dict{ISBN, count of book ratings regardless of value} (of number 2) => {ISBN_1: 1,ISBN_2: 5,ISBN_3: 7}
book_popularity_result_dictionary = book_popularity.book_popularity_result_dictionary
print(book_popularity_result_dictionary)
# #    ii. dict.values => [4,5,7] => X_bar, sigma => Z = X-X_bar/sigma > 3 OR <-3, Z>40 OR Z<2
ratings = list(book_popularity_result_dictionary.values())
ratings = np.array(ratings)
avg = np.mean(ratings)
std = np.std(ratings)
print(avg)
print(std)

# #    iv. Decision rule for upper tail: X-X_bar/std <= 3
upper_limit = avg + 3*std
upper_outliers = {}
for (isbn, no_of_ratings) in book_popularity_result_dictionary.items():
    if no_of_ratings >= upper_limit:
        upper_outliers[isbn] = no_of_ratings

# #     v. Decision rule for lower tail: X-X_bar/std >= -3
lower_limit = avg - 3*std
lower_outliers = {}
for (isbn, no_of_ratings) in book_popularity_result_dictionary.items():
    if no_of_ratings <= lower_limit:
        lower_outliers[isbn] = no_of_ratings
print(len(upper_outliers) + len(lower_outliers))
print(len(book_popularity_result_dictionary))
print(upper_outliers)
print(len(upper_outliers))

# #   iii. loop dict/filter with decision rule
# #    vi. 6 sigma (saltses + references)
