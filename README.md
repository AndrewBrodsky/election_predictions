## <span style="color:blue">U.S. Federal Election Prediction Model</span>

The Federal Election Predictor is a machine learning model that predicts candidates' vote totals for U.S. House of Representatives elections, based on district demographics, campaign funding, and candidate party.

#### <span style="color:navy">Purpose</span>

Determining the factors which contribute to U.S. elections is important for political scientists and political campaigns. Models that predict election outcomes have typically found that polls are the strongest predictor of election results. However, while polls reflect the current state of a race, they do not uncover the mechanisms or causal relationships at work.

This study uses data on demographic factors -- such as race, age, and income; detailed campaign financing data; and candidate characteristics to predict the number of votes a candidate will receive in a House election.


#### <span style="color:navy">Background</span>

Academic research has used national economic and political indicators such as GNP per capita growth and Presidential popularity to predict House elections (Lewis-Beck and Rice, 1984).

Popular news sites such as  <a href = https://projects.fivethirtyeight.com/congress-generic-ballot-polls/> FiveThirtyEight </a>, <a href = https://www.politico.com/news/2018-house-elections>Politico</a> and <a href = https://www.realclearpolitics.com/epolls/writeup/battle_for_the_house_of_representatives-51.html>Real Clear Politics</a> offered election predictions during recent electoral cycles. However, these models are primarily based on polls results. The more sophisticated of these models use some additional data. For example, FiveThirtyEight's <a href = https://projects.fivethirtyeight.com/2016-election-forecast/senate/>2016 Senate model </a>uses a probabilistic, model that incorporates each candidate's ideology and state fundamentals including generic approval ratings and fundraising totals.

##### Methodology in the literature


However, few existing election prediction models leverage the power of machine learning techniques to predict results. Those that do frequently use analyses of social media sites such as Twitter (Beauchamp, 2017; Huberty, 2013; Saleiro, Gomes, and Soares, 2016).  


#### Data

Data for the project are drawn from three publicly available sources, including the following:
  * American Community Survey: demographic and economic data for each U.S. House district in 2012, 2014, and 2016.
  * Politico: number of votes and party per candidate for House elections in 2012, 2014, and 2016.
  * Federal Election Commission (FEC):
  amount of money contributed to each candidate and committee in 2012, 2014, and 2016

#### Existing Code

The model uses several existing APIs and Python wrappers, including:
  * VoteSmart API
  * CensusData API


#### Methodology

Machine learning models often yield impressive predictive results, especially with very complex or high-dimensional data. Because this analysis uses complex data with many predictor variables, several machine learning algorithms were developed, including Random Forests, Artificial Neural Nets, as well as simple logistic regression.

### References

Lewis-Beck, M.S. and Rice, T.W. .  <i> Legislative Studies Quarterly</i>.  Vol. 9, No. 3 (Aug 1984), pp. 475-486. Available at:
http://www.jstor.org/stable/439492?seq=1#page_scan_tab_contents
