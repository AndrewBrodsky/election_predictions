## How To Buy An Election: A Machine-Learning Approach to Predicting Federal Elections Through Campaign Funding

Determining the factors which contribute to U.S. elections is important for political scientists and political campaigns. Models that predict election outcomes have typically found that polls are the strongest predictor of election results <sup>.5</sup>. However, while polls reflect the current state of a race, they do not uncover the mechanisms or causal relationships at work.

This project uses machine learning to predict candidates' vote totals for U.S. House of Representatives elections, based on district demographics, campaign funding, and candidate party.

<img src = https://commons.wikimedia.org/wiki/File:1988_US_House_Election_Map.png> image </image>

### <span style="color:navy">Background</span>

Academic research has used national economic and political indicators such as GNP per capita growth and Presidential popularity to predict House elections<sup>1</sup>

Popular news sites such as  <a href = https://projects.fivethirtyeight.com/congress-generic-ballot-polls/> FiveThirtyEight </a>, <a href = https://www.politico.com/news/2018-house-elections>Politico</a> and <a href = https://www.realclearpolitics.com/epolls/writeup/battle_for_the_house_of_representatives-51.html>Real Clear Politics</a> offered election predictions during recent electoral cycles. However, these models are primarily based on polls results. The more sophisticated of these models use some additional data. For example, FiveThirtyEight's <a href = https://projects.fivethirtyeight.com/2016-election-forecast/senate/>2016 Senate model </a>uses a probabilistic, model that incorporates each candidate's ideology and state fundamentals including generic approval ratings and fundraising totals.

Many prediction models use regression models, particularly regression discontinuity (RDD) designs.<sup>1.5</sup> However, few existing election prediction models leverage the power of machine learning techniques to predict results. Those that do frequently use analyses of social media sites such as Twitter.<sup>2</sup>

One study used Random Forest and Support Vector Machines to develop a model to predict election results based on age, gender, and race of invividual voters and achieved results that wree accurate within 1%.<sup>3</sup>

For example, <a href = http://www.jstor.org/stable/439492?seq=1#page_scan_tab_contents> </a>Kaggle</a> includes examples of some machine learning algorithms to predict 2016 election results, including K-means clustering.

### Data

Data for the project are drawn from four publicly available sources, including:
  * <a href = https://www.census.gov/programs-surveys/acs/><b>American Community Survey</b></a>: demographic and economic data for each U.S. House district in 2014 and 2016.
  * <a href=politico.com><b>Politico</b></a>: number of votes and party per candidate for House elections in 2014 and 2016.
  * <a href="fec.gov"><b>Federal Election Commission</b></a>:
  amount of money contributed to each candidate and each committee in 2012, 2014, and 2016
  * <a href="www.opensecrets.org"><b>Open Secrets</b></a>: "Dark money" spent for or against each candiate during the 2014 and 2016 election cycles

### Methodology

Machine learning models often yield impressive predictive results, especially with very complex or high-dimensional data. Because this analysis uses complex data with many predictor variables, several machine learning algorithms were developed, including Random Forests, Artificial Neural Nets, as well as simple logistic regression.

### Code

Code for the project is organized into five main scripts: one for each of the four data sources, and one to combine the data together and run the machine learning algorithms.
* <a href = "https://github.com/AndrewBrodsky/election_predictions/blob/master/predictions.py"> <b>predictions.py</b></a> does this and that.
* <a href = "https://github.com/AndrewBrodsky/election_predictions/blob/master/politico.py"> <b>politico.py</b></a> does this and that.
* <a href = "https://github.com/AndrewBrodsky/election_predictions/blob/master/acs.py"> <b>acs.py</b></a> does this and that.
* <a href = "https://github.com/AndrewBrodsky/election_predictions/blob/master/fec.py"> <b>fec.py</b></a> does this and that.
* <a href = "https://github.com/AndrewBrodsky/election_predictions/blob/master/open_secrets.py"> <b>open_secrets.py</b></a> does this and that.





The project also leverages an existing Python wrapper, <a href = "https://jtleider.github.io/censusdata/"> <b>CensusData</b></a>, which accesses the Census Data API provided by the U.S. Census Bureau.




### Notes

<sup>.5</sup> <a href = http://science.sciencemag.org/content/355/6324/515>Kennedy, Wojcik, and Lazer (2017).</a><br>
<sup>1</sup> See <a href = http://www.jstor.org/stable/439492?seq=1#page_scan_tab_contents>Lewis-Beck and Rice (1984)</a>.<br>
<sup>1.5</sup> See <a href = https://www.sciencedirect.com/science/article/pii/S0169207008000289>Lewis-Beck and Tien (2008),<a> <a href= https://onlinelibrary.wiley.com/doi/full/10.1111/ajps.12127> Eggers, Fowler, Hinmueller, Hall, and Snyder (2014)</a> and <a href = https://www.sciencedirect.com/science/article/pii/S0304407607001121>Lee (2008)</a>.<br>
<sup>2</sup> See Beauchamp, 2017; Huberty, 2013; Saleiro, Gomes, and Soares, 2016.<br>
<sup>3</sup> See <a href = https://www.liebertpub.com/doi/full/10.1089/big.2017.0047> Sathiaraj, Cassidy, and Rohli (2017) </a>.
