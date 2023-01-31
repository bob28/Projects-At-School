# Network Data Analysis
#### Network Data Analysis - final project
#### April 18, 2022
**Title:**
Network Analysis of Wikipedia Categorization and the Influence of Article Quality

**Goal:**
The goal was to create a report analyzing Wikipedia by both researching related papers that investigated the site and performing analysis on the graphical dataset of Wikipedia page links.

**Technologies Used:**
Python, Numpy, NetworkX, Matplotlib, Excel

**Result:**
First, we defined the problem and stated the questions that we would like to answer in this report, which was both understanding how editors on Wikipedia works, and also look at the community categorization among pages on the site. 

The first section dealt with the 10 related papers that previously looked at Wikipedia and tried to understand contributions, quality, and how big data could help understand the quality of articles that we being written. We read and summarized them in the report. 

After that, we had to clean and validate the data that we received from [Stanford Wikispeedia](https://snap.stanford.edu/data/wikispeedia.html). This contains a graphical dataset made up of nodes which showcases the link between articles across Wikipedia. 

We imported the files into NetworkX, a Python library that is made to analyze graphical datasets. This library also allowed us to find statistics of the network, like: 
- PageRank
- degrees of centrality
- degree distribution
- number of edges
- edge density
- notions of centrality
- community assessments. 

We used Matplotlib to graph the degree distribution and how it showcased numerous large hubs which many pages linked to. 

We investigated the various statistical variables which allowed us to view the data better, like notions of centrality, PageRank, closeness and betweenness. 

We then looked at the community assessment and used NetworkX to create communities across the network made up of 8722 nodes (websites). We analyzed those results and drew up a table that showcased which group was tied to what community. This was where we used Excel spreadsheets. 

At the end, we discussed all 10 related papers and also explored what our experiment led us to believe. 