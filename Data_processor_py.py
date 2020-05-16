#!/usr/bin/env python
# coding: utf-8

# Data processor:

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# In[4]:


#%matplotlib inline

class Summary:
    
    def __init__(self, data):
        self.data = data
        
    def get_pages(self):
        pages = int(np.ceil(len(self.data)/25))
        return pages
        
        
    def basic_summary(self):
        number = self.data.iloc[:,6].count()
        sales = [int(x) for x in self.data.iloc[:,6].dropna()]
        new_price = np.array([x for x in self.data.iloc[:,5].dropna()]).astype(float)
        discount = np.array([x for x in self.data.iloc[:,6].dropna()]).astype(float)
        old_price = self.data[['Normal price (€)','Sale rate (in %)']].dropna().iloc[:,0]
        
        mean_of_review = round(self.data.iloc[:,3].dropna().mean(),1)
        
        return {print('Basic summary: '),
                print(f'The number of items on sale from the first {self.get_pages()} pages is {number}.') ,
                print(f'The mean discount is {round(np.mean(sales),2)}%.'),
                print(f'The average price before sale is {round(np.mean(old_price),2)}€, with the average price after sale being {round(np.mean(new_price),2)}€.'),
                print(f'The average number of reviews on a game from the first {self.get_pages()} pages is {mean_of_review}.')
               }


    def price_hist(self):
        new_price = np.array([x for x in self.data.iloc[:,5].dropna()]).astype(float)
        discount = np.array([x for x in self.data.iloc[:,6].dropna()]).astype(float)
        old_price = self.data[['Normal price (€)','Sale rate (in %)']].dropna().iloc[:,0] #original prices of items on sale
        #all_prices = np.array([x[:-1].replace(',', '.').replace("-","0") for x in self.data.iloc[:,4].dropna()]).astype(float)
        
        #all_price_hist = pd.Series(all_prices).plot(kind="hist",bins=20, alpha=0.8, figsize=(10,5),color="blue", edgecolor = "red",linewidth=3, label="All prices")
        old_price_hist = pd.Series(old_price).plot(kind="hist",
                                                   bins=20, 
                                                   alpha=0.8, 
                                                   figsize=(10,5),
                                                   color="green", 
                                                   edgecolor = "blue",
                               
                                                   linewidth=3, 
                                                   label = "Prices before discount")
        new_price_hist = pd.Series(new_price).plot(kind="hist",
                                                   bins=20, 
                                                   alpha=0.8, 
                                                   figsize=(10,5),
                                                   color="orange", 
                                                   edgecolor = "green",
                                                   linewidth=3, 
                                                   label = "Discounted Prices")
        
        plt.legend()
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('$$$', size='x-large')
        return print(), plt.show() 
    
    def release_hist_total_year(self):
        release = self.data.iloc[:,1].dropna()
        release_all = release.groupby(release.dt.year).count()
        release_all.append
        release_all.plot(kind="bar", 
                         width= 1,
                         color="blue", 
                         alpha=0.8, 
                         figsize=(10,5), 
                         edgecolor = "red",
                         linewidth=3, 
                         label = "Release date of all games")
        
        plt.legend()
        plt.title("Number of games released by Year")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        return print(), plt.show()
    
    def release_hist_sale_year(self):
        release = self.data.iloc[:,1].dropna()
        release_sale = self.data.groupby(release.dt.year)['Discounted price if there is a sale (€)'].count()
        release_sale.plot(kind="bar", 
                          width= 1,
                          color="blue", 
                          alpha=0.8, 
                          figsize=(10,5),
                          edgecolor = "red",
                          linewidth=3, 
                          label = "Release date of items on sale")

        plt.legend()
        plt.title("Number of games on sale released by Year")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        return print(), plt.show()
    
    def release_hist_total_month(self):
        release = self.data.iloc[:,1].dropna()
        release_all = release.groupby(release.dt.month).count()
        release_all.plot(kind="bar",
                         
                         width= 1,
                         color="red",
                         alpha=0.8, 
                         figsize=(10,5),
                         edgecolor = "blue",
                         linewidth=3, 
                         label = "Release date of all games")
        
        plt.legend()
        plt.title("Number of games released by Month")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        return print(), plt.show()
    
    def release_hist_sale_month(self):
        release = self.data.iloc[:,1].dropna()
        release_sale = self.data.groupby(release.dt.month)['Discounted price if there is a sale (€)'].count()
        release_sale.plot(kind="bar", 
                          width= 1,
                          color="red", 
                          alpha=0.8, 
                          figsize=(10,5), 
                          edgecolor = "blue",
                          linewidth=3, 
                          label = "Release date of items on sale")

        plt.legend()
        plt.title("Number of games on sale released by Month")
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (Year)', size='x-large')
        return print(), plt.show()

    
    def release_multiple_hist(self):
        rl = self.data.iloc[:,1].dropna().astype("datetime64")
        rl = rl[rl >= '2010-01-01']
        rl = rl[rl <= '2020-01-01']
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
        rl.groupby(by=[rl.dt.month,rl.dt.year]).count().plot(kind="bar",
                                                              width= 1,
                                                              color = colors,
                                                              alpha=0.8, 
                                                              figsize=(10,5),
                                                              edgecolor = "black",
                                                              linewidth=1,
                                                              label = "Release date of items on sale"
                                                             ).axes.xaxis.set_visible(False)
        
        plt.legend(['2010',
                    '2011',
                    '2012',
                    '2013',
                    '2014',
                    '2015',
                    '2016',
                    '2017',
                    '2018',
                    '2019'])
        plt.ylabel('Frequency', size='x-large')
        plt.xlabel('Release date (by months and years)', size='x-large')
        #rl.axes.xaxis.set_visible(False)
        return plt.show()
    
    def release_tab_year(self):
        release = self.data.iloc[:,1].dropna()
        release_all = release.groupby(release.dt.year).count()
        release_sale = self.data.groupby(release.dt.year)['Discounted price if there is a sale (€)'].count()
        average_discount = round(self.data.groupby(release.dt.year)['Sale rate (in %)'].mean(),2)
        average_rating = round(self.data.groupby(release.dt.year)['Share of positive reviews (in %)'].mean(),2)
        sale_ratio = round(release_sale/release_all,4)
        
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
        return print(), plt.show()
           
    def release_tab_month(self):
        release = self.data.iloc[:,1].dropna()
        release_all = release.groupby(release.dt.month).count()
        release_sale = self.data.groupby(release.dt.month)['Discounted price if there is a sale (€)'].count()
        average_discount = round(self.data.groupby(release.dt.month)['Sale rate (in %)'].mean(),2)
        average_rating = round(self.data.groupby(release.dt.month)['Share of positive reviews (in %)'].mean(),2)
        sale_ratio = round(release_sale/release_all,4)
        
        release_table_month = pd.concat([release_all,
                                         release_sale,
                                         average_discount, 
                                         sale_ratio, 
                                         average_rating],
                                        axis=1
                                       )
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
        
        return print(), plt.show()
        
        
    
    def ratings(self):
        
        counted = self.data.groupby('Share of positive reviews (in %)')['Total number of reviews',
                                                                        'Discounted price if there is a sale (€)'
                                                                       ].count()
        sale_ratio = (counted.iloc[:,1])/counted.iloc[:,0]
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
        fig = plt.figure(figsize = (20, 23))
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
        
        return plt.show()
    
    def sale_ratio_hist(self):
        sale_ratio_hist = pd.Series(self.ratings()['Ratio of games on sale']).plot(kind="bar",
                                                                                   alpha=0.8, 
                                                                                   figsize=(20,5),
                                                                                   color="green", 
                                                                                   edgecolor = "blue",
                                                                                   linewidth=3, 
                                                                                   label = "Prices before discount")
        plt.ylabel('Ratio of games on sale', size='x-large')
        plt.xlabel('Rating', size='x-large')
        plt.gca().invert_xaxis()
        
        return print(),plt.show()
    
    def average_discount_hist(self):
        sale_ratio_hist = pd.Series(self.ratings()['Avg. discount rate (%)']).plot(kind="bar",
                                                                                   alpha=0.8, 
                                                                                   figsize=(20,5),
                                                                                   color="red", 
                                                                                   edgecolor = "blue",
                                                                                   linewidth=3, 
                                                                                   label = "Prices before discount")
        plt.ylabel('Average discount rate (%)', size='x-large')
        plt.xlabel('Rating', size='x-large')
        plt.gca().invert_xaxis()
        
        return print(),plt.show()
    
    
        

