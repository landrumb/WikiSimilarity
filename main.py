# %% [markdown]
# # Correlation Between Semantic Similarity and Wikipedia Distance
# ### CMSC 320, Spring 2022
# #### Ben Landrum, Gaetan Almela, and Nav Bindra
# 
# 

# %% [markdown]
# The Wikipedia link graph is a graph where vertices represent Wikipedia articles and directed edges from vertex $A$ to vertex $B$ represent a link to $B$ in the text of $A$. We define Wikipedia distance between pages $A$ and $B$ to be the minimum number of links required to get from $A$ to $B$ in the Wikipedia link graph, where the first such link is on page $A$, the second is on the page the first link points to, and so on, until a link to $B$ is found.
# 
# Word2Vec is a popular tool for computing word embeddings, which use a vector space representation of words to place them in an abstract space where similar vectors indicate that words appear in similar contexts. These vectors can then be compared to find a metric of semantic similarity between words. 
# 
# Because pages on Wikipedia contain links which are relevant to the topic the page is covering, similar topics are often closely if not directly linked. Therefore, it stands to reason that if semantic similarity is a valid metric of similarity between topics, a higher semantic similarity between two topics should correspond to a lower Wikipedia distance between said topics. We are looking to test the hypothesis that there exists a negative correlation between Wikipedia distance and Word2Vec semantic similarity. Our null hypothesis is that there does not exist a statistically significant negative correlation between Wikipedia distance and Word2Vec semantic similarity.

# %% [markdown]
# ## Computing Semantic Similarity with Word2Vec

# %% [markdown]
# __This is not hard. If we wanted to pad it we could compute our own embedding, which would probably make it seem a little less trivial and would honestly be really easy, just involves a lot of text being loaded.__

# %% [markdown]
# ## Computing Wikipedia Distance

# %% [markdown]
# __This will be very computationally expensive for articles which are far apart or have particularly high degrees, and will require the loading of a prohibitively large database of links between Wikipedia articles. Said database should probably be on a local SQL server.__

# %% [markdown]
# ## Building a Bot With Semantic Similarity

# %% [markdown]
# __This is virtually already done, but we can make it much better and I would love to compare different iterations a la chess bot comparison grid.__

# %% [markdown]
# ### Using Semantic Similarity to Approximate Wikipedia Distance

# %% [markdown]
# __This seems pointless but makes the statistical analysis straightforward.__

# %% [markdown]
# ## Conclusion

# %% [markdown]
# __We can just compute the two values for random pairs of articles until we have a super low p-value and say boom statistically significant correlation. Will have to consult stat notes to remember what test you're supposed to use for correlation. $\chi^2$?__

# %% [markdown]
# 


