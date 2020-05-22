#!/usr/bin/env python
# coding: utf-8

# Data processor:

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as mpatches


# In[4]:

class Summary:
    
    def __init__(self, data):
        self.data = data
        #define self.release in init because it is used multiple times in the class (also in the following classes)
        self.release = self.data.iloc[:,1].dropna()

        
    def get_pages(self):
        pages = int(np.ceil(len(self.data)/25))
        return pages
        
        
    def basic_summary(self):
        #function generating basic summary of discounts, prices and reviews
        number = self.data.iloc[:,6].count()
        sales = [int(x) for x in self.data.iloc[:,6].dropna()]
        new_price = np.array([x for x in self.data.iloc[:,5].dropna()]).astype(float)
        discount = np.array([x for x in self.data.iloc[:,6].dropna()]).astype(float)
        old_price = self.data[['Normal price (€)','Sale rate (in %)']].dropna().iloc[:,0]
        
        mean_of_review = round(self.data.iloc[:,3].dropna().mean(),1)
        
        print('Basic summary: '),
        print(f'The number of items on sale from the first {self.get_pages()} pages is {number}.') ,
        print(f'The mean discount is {round(np.mean(sales),2)}%.'),
        print(f'The average price before sale is {round(np.mean(old_price),2)}€, with the average price after sale being {round(np.mean(new_price),2)}€.'),
        print(f'The average number of reviews on a game from the first {self.get_pages()} pages is {mean_of_review}.')
            
        return

    def price_hist(self):
        #find discounted prices and the prices before discount
        new_price = np.array([x for x in self.data.iloc[:,5].dropna()]).astype(float)
        discount = np.array([x for x in self.data.iloc[:,6].dropna()]).astype(float)
        old_price = self.data[['Normal price (€)','Sale rate (in %)']].dropna().iloc[:,0] #original prices of items on sale
        #histograms for both the old and new prices
        old_price_hist = pd.Series(old_price).plot(kind="hist",
                                                   bins=400, 
                                                   alpha=0.8, 
                                                   figsize=(15,5),
                                                   color="green", 
                                                   edgecolor = "blue",
                                                   linewidth=3, 
                                                   label = "Prices before discount")
        new_price_hist = pd.Series(new_price).plot(kind="hist",
                                                   bins=400, 
                                                   alpha=0.8, 
                                                   figsize=(15,5),
                                                   color="orange", 
                                                   edgecolor = "red",
                                                   linewidth=3, 
                                                   label = "Discounted Prices")
        
        plt.legend()
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Price (€)', size='x-large')
        plt.gca().set_xlim([0,100])
        plt.show()
    
    def release_hist_total_year(self):
        #group data by year and count the number of games released by year
        release_all = self.release.groupby(self.release.dt.year).count()
        release_all.append
        release_all.plot(kind="bar", 
                         width= 1,
                         color="blue", 
                         alpha=0.5, 
                         figsize=(15,5), 
                         edgecolor = "red",
                         linewidth=3, 
                         label = "Release date of all games")
        
        plt.legend()
        plt.title("Number of games released by Year")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        plt.show()
    
    def release_hist_sale_year(self):
        #group data by year and count the number of discounted games released by year
        release_sale = self.data.groupby(self.release.dt.year)['Discounted price if there is a sale (€)'].count()
        release_sale.plot(kind="bar", 
                          width= 1,
                          color="blue", 
                          alpha=0.5, 
                          figsize=(15,5),
                          edgecolor = "red",
                          linewidth=3, 
                          label = "Release date of items on sale")

        plt.legend()
        plt.title("Number of games on sale released by Year")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        plt.show()
    
    def release_hist_total_month(self):
        #group data by month and count the number of games released by month
        release_all = self.release.groupby(self.release.dt.month).count()
        release_all.plot(kind="bar", 
                         width= 1,
                         color="red",
                         alpha=0.5, 
                         figsize=(15,5),
                         edgecolor = "blue",
                         linewidth=3, 
                         label = "Release date of all games")
        
        plt.legend()
        plt.title("Number of games released by Month")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Month)', size='x-large')
        plt.show()
    
    def release_hist_sale_month(self):
        #group data by month and count the number of discounted games released by month
        release_sale = self.data.groupby(self.release.dt.month)['Discounted price if there is a sale (€)'].count()
        release_sale.plot(kind="bar", 
                          width= 1,
                          color="red", 
                          alpha=0.5, 
                          figsize=(15,5), 
                          edgecolor = "blue",
                          linewidth=3, 
                          label = "Release date of items on sale")

        plt.legend()
        plt.title("Number of games on sale released by Month")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Month)', size='x-large')
        plt.show()
    
    
    def release_multiple_hist(self):
        #get release dates and select the relevant ones 
        rl = self.release
        rl = rl[rl >= '2010-01-01']
        rl = rl[rl <= '2019-12-31']
        #choosing colors of bars
        colors = np.array(["lightgrey", 
                           "skyblue", 
                           "dodgerblue", 
                           "gold",
                           "lightpink",
                           "mediumorchid", 
                           "lightcoral", 
                           "limegreen", 
                           "indigo", 
                           "chocolate"])
        #group the data by month and year and plotting the number of games for years and months
        my_plot = rl.groupby(by=[rl.dt.month,rl.dt.year]).count()
        
        my_plot.plot(kind="bar",
                  width= 1,
                  color = colors,
                  alpha=0.8, 
                  figsize=(15,5),
                  edgecolor = "black",
                  linewidth=1,
                 )

        #changing the x axis labels to months (otherwise the labels are unreadable)
        ax = plt.gca()
        pos = [5,15,25,35,45,55,65,75,85,95,105,115]
        l = ['January', 
            'February', 
            'March', 
            'April', 
            'May', 
            'June', 
            'July', 
            'August', 
            'September', 
            'October', 
            'November',
            'December']
        ax.set(xticks=pos, xticklabels=l)
        
        #creating legend of the plot
        years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        #dictionary for legend values
        dictionary = dict(zip(years, colors))
        patchList = []
        #making handles for each color so plt.legend can recognize the input
        for key in dictionary:
            data_key = mpatches.Patch(color=dictionary[key], label=key)
            patchList.append(data_key)

        plt.legend(handles=patchList,bbox_to_anchor=(1.03, 1))
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (by months and years)', size='x-large')
        plt.title('Number of games released (by months and years)')
        plt.show()
    
    
    def runAll(self):
        #a function to run all methods of the class
        self.basic_summary()
        self.price_hist()
        self.release_hist_total_year()
        self.release_hist_sale_year()
        self.release_hist_total_month()
        self.release_hist_sale_month()
        self.release_multiple_hist()

        
class Summary_time:
    
    def __init__(self, data):
        self.data = data
        self.release = self.data.iloc[:,1].dropna()
        
    def release_tab_year(self):
        #grouping data by year of release
        release_all = self.release.groupby(self.release.dt.year).count()
        #finding different values for the grouped data
        release_sale = self.data.groupby(self.release.dt.year)['Discounted price if there is a sale (€)'].count()
        average_discount = round(self.data.groupby(self.release.dt.year)['Sale rate (in %)'].mean(),2)
        average_rating = round(self.data.groupby(self.release.dt.year)['Share of positive reviews (in %)'].mean(),2)
        sale_ratio = round(release_sale/release_all,4)
        #concating and thus creating a pandas DataFrame from the values for better manipulation with data
        release_table_year = pd.concat([release_all,
                                        release_sale,
                                        average_discount, 
                                        sale_ratio, 
                                        average_rating],
                                       axis=1)
        release_table_year = release_table_year.set_axis(['Games',
                                                          'Discounted games',
                                                          'Average discount (%)',
                                                          'Ratio of games on sale',
                                                          'Average rating (%)'],
                                                         axis=1 ,inplace=False
                                                        )
        
        #creating a table for data vizualization
        fig = plt.figure(figsize = (15, 6))
        ax = fig.add_subplot(111)

        the_table = ax.table(cellText = release_table_year.values,
                    rowLabels = release_table_year.index,
                    colLabels = release_table_year.columns,
                    loc = "center",
                    bbox=[0, -1.03, 1.5, 2]
                    )
        ax.set_title("Summary of the offered games by year of release",
                     fontsize=23, 
                     loc="center"
                    )
        ax.axis("off")
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(20)
        plt.show()
    
    
    def average_rating_year(self):
        #creating a plot out of the average ratings throughout the years
        rl = self.release
        #only taking a portion of the data due to low number of games from previous years
        rl = rl[rl >= '2005-01-01']
        average_rating = round(self.data.groupby(rl.dt.year)['Share of positive reviews (in %)'].mean(),2)
        average_rating.plot(kind="line", figsize=(15,5), color = "red", alpha=0.3, linewidth = 4)
        
        plt.title('Game rating throughout the years')
        plt.ylabel('Rating', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        plt.show()
     
        
    def release_tab_month(self):
        #creating a table to summarize the data based on months (grouping by month of release)
        release_all = self.release.groupby(self.release.dt.month).count()
        #getting wanted values
        release_sale = self.data.groupby(self.release.dt.month)['Discounted price if there is a sale (€)'].count()
        average_discount = round(self.data.groupby(self.release.dt.month)['Sale rate (in %)'].mean(),2)
        average_rating = round(self.data.groupby(self.release.dt.month)['Share of positive reviews (in %)'].mean(),2)
        sale_ratio = round(release_sale/release_all,4)
        #concate to pandas DataFrame
        release_table_month = pd.concat([release_all,
                                         release_sale,
                                         average_discount, 
                                         sale_ratio, 
                                         average_rating],
                                        axis=1
                                       )
        #creating a table for vizualization 
        release_table_month = release_table_month.set_axis(['Games', 
                                                            'Discounted games', 
                                                            'Average discount (%)', 
                                                            'Ratio of games on sale',
                                                            'Average rating (%)'],
                                                           axis=1 ,
                                                           inplace=False
                                                          )
        release_table_month = release_table_month.set_axis(['January', 
                                                            'February', 
                                                            'March', 
                                                            'April', 
                                                            'May', 
                                                            'June', 
                                                            'July', 
                                                            'August', 
                                                            'September', 
                                                            'October', 
                                                            'November',
                                                            'December'],
                                                           axis=0 ,
                                                           inplace=False
                                                          )
        
        fig = plt.figure(figsize = (15, 4.5))
        ax = fig.add_subplot(111)

        the_table = ax.table(cellText = release_table_month.values,
                    rowLabels = release_table_month.index,
                    colLabels = release_table_month.columns,
                    loc = "center",
                    bbox=[0, -1.04, 1.5, 2]
                            )
        ax.set_title("Summary of the offered games by month of release", fontsize=25)

        ax.axis("off")
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(20)
        plt.show()

         
    def runAll(self):
        #a function to run all methods of the class
        self.release_tab_year()
        self.average_rating_year()
        self.release_tab_month()
        
    
    
    
class Summary_ratings:
    
    def __init__(self, data):
        self.data = data
        
    
    def ratings(self):
        #group data by ratings and getting numbers of total games and games on sale
        counted = self.data.groupby('Share of positive reviews (in %)')['Total number of reviews',
                                                                        'Discounted price if there is a sale (€)'
                                                                       ].count()
        #generating ratio of games on sale for each rating
        sale_ratio = (counted.iloc[:,1])/counted.iloc[:,0]
        #group by rating and getting averages of prices, discounts and total reviews
        means = self.data.groupby('Share of positive reviews (in %)')['Total number of reviews',
                                                                      'Normal price (€)',
                                                                      'Discounted price if there is a sale (€)',
                                                                      'Sale rate (in %)'
                                                                     ].mean()
         
        rating_table = pd.concat([counted,round(sale_ratio,4),round(means,2)], axis=1).sort_index(ascending=False)
        rating_table = rating_table.set_axis(['Games',
                                              'Discounted games',
                                              'Ratio of games on sale',
                                              'Avg. review count', 
                                              'Avg. price (€)', 
                                              'Avg. discounted price (€)',
                                              'Avg. discount rate (%)'],
                                             axis=1 ,
                                             inplace=False)
        return rating_table
    
    def summary_table(self):
        #creating a table from the data obtained in previous function (self.ratings())
        fig = plt.figure(figsize = (20, 22))
        ax = fig.add_subplot(111)
        
        the_table = ax.table(cellText = self.ratings().values,
                    rowLabels = self.ratings().index,
                    colLabels = self.ratings().columns,
                    loc = "center"
                    )
        ax.set_title("Summary of offered games by the share of positive reviews from Steam users",
                     fontsize=20,
                     loc= "center"
                    )

        ax.axis("off")
        plt.show()

    
    def sale_ratio_hist(self):
        #plotting bar chart of ratio of games in sale while groupped by rating
        sale_ratio_hist = pd.Series(self.ratings()['Ratio of games on sale']).plot(kind="bar",
                                                                                   alpha=0.8, 
                                                                                   figsize=(20,5),
                                                                                   color="green", 
                                                                                   edgecolor = "yellow",
                                                                                   linewidth=3, 
                                                                                   label = "Ratio of games on sale")
        plt.title('Ratio of games on sale for different Steam ratings')
        plt.ylabel('Ratio of games on sale', size='x-large')
        plt.xlabel('Rating', size='x-large')
        plt.gca().invert_xaxis()
        plt.show()

    
    def average_discount_hist(self):
        #plotting bar chart of average discount while groupped by rating
        sale_ratio_hist = pd.Series(self.ratings()['Avg. discount rate (%)']).plot(kind="bar",
                                                                                   alpha=0.8, 
                                                                                   figsize=(20,5),
                                                                                   color="red", 
                                                                                   edgecolor = "blue",
                                                                                   linewidth=3, 
                                                                                   label = "Average discount rate")
        plt.title('Average discount rates for different Steam ratings')
        plt.ylabel('Average discount rate (%)', size='x-large')
        plt.xlabel('Rating', size='x-large')
        plt.gca().invert_xaxis()
        plt.show()
    
    def n_of_games(self):
        #plotting bar chart of the total number of games while groupped by rating
        sale_ratio_hist = pd.Series(self.ratings()['Games']).plot(kind="bar",
                                                                                   alpha=0.8, 
                                                                                   figsize=(20,5),
                                                                                   color="yellow", 
                                                                                   edgecolor = "red",
                                                                                   linewidth=3, 
                                                                                   label = "Number of games")
        plt.title('Number of games for different Steam ratings')
        plt.ylabel('Number of games', size='x-large')
        plt.xlabel('Rating', size='x-large')
        plt.gca().invert_xaxis()
        plt.show()

    
    def runAll(self):
        #a function to run all methods of the class
        self.summary_table()
        self.n_of_games()
        self.sale_ratio_hist()
        self.average_discount_hist()
        



