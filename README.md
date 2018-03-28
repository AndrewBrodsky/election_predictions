U.S. Federal Election Prediction Model

The Federal Election Predictor is a machine learning model that predicts candidates' vote totals for U.S. House of Representatives elections, based on district demographics, campaign funding, and candidate party.

Purpose

Determining the factors which contribute to U.S. elections is important for political scientists and political campaigns. Models that predict election outcomes have typically found that polls are the strongest predictor of election results. However, while polls reflect the current state of a race, they do not uncover the mechanisms or causal relationships at work.

This study uses data on demographic factors -- such as race, age, and income; detailed campaign financing data; and candidate characteristics to predict the number of votes a candidate will receive in a House election.


Data

Data for the project are drawn from three publicly available sources, including the following:
  American Community Survey: demographic and economic data for each U.S. House district in 2012, 2014, and 2016.
  Politico: number of votes and party per candidate for House elections in 2012, 2014, and 2016.
  Federal Election Commission (FEC):
  amount of money contributed to each candidate and committee in 2012, 2014, and 2016


Existing Code

The model uses several existing APIs and Python wrappers, including:
  * VoteSmart API
  * CensusData API


Methodology

Machine learning models often yield impressive predictive results, especially with very complex or high-dimensional data. Because this analysis uses complex data with many predictor variables, several machine learning algorithms were developed, including Random Forests, Artificial Neural Nets, as well as simple logistic regression.
