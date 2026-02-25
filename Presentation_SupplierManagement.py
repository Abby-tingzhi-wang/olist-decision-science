#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf


# In[2]:


from olist.seller import Seller
sellers = Seller().get_training_data()
sellers.describe()


# # Supplier Management
# ## Reducing bad suppliers can significantly increase Olist profits and profit margins

# ## To get the highest profits, after removing 855 bad suppliers, Olist's Profit would increase  403,367 BRL, Profit Margin would increase 1% 
# 

# In[18]:


table = pd.DataFrame(columns=['index','Current','After removing bad suppliers','Changes'])
row1 = pd.DataFrame([['Profit', '667,609 BRL', '1070,976 BRL', '403,367 BRL']], columns=['index', 'Current', 'After removing bad suppliers', 'Changes'])
row2 = pd.DataFrame([['Profit Margin', 23.96, 24.97, 1.01]], columns=['index', 'Current', 'After removing bad suppliers', 'Changes'])

# Concatenate the rows to the table DataFrame
table = pd.concat([table, row1, row2], axis=0)
table = table.set_index('index')
table


# ## Why removing the bad suppliers will increase our Profits?
# ### There are 2 reasons:
# ###  1. Bad suppliers will cost us more Reputation fees 
# #### Consumers prone to give lower review score for the bad suppliers, which would cost Olist more money to fix the reputation and win back the market. It would cost Olist avarage 393 BRL more to fix the reputation for the bad suppliers.
# ###  2. Less items/ less suppliers we use would save us the IT cost fee

# In[4]:


sellers[['review_score','cost_of_reviews','revenues','profits']].describe().loc[['mean','min','max']]


# In[13]:


check = seller_sorted[0:855]
check[['review_score','cost_of_reviews','revenues','profits']].describe().loc[['mean','min','max']]


# In[14]:


sales_after = check['sales'].sum()*0.1
sales_after


# ###  Less items/ less suppliers we use would save us the IT cost fee
# #### Using 2967 supplier would cost Olist around 500K BRL, while removing 855 bad suppliers, it saves around 104K BRL in the IT Cost fees
# * Current IT Cost is 500K BRL
# * After removing bad suppliers the IT cost is around 396K BRL

# # Reducing the suppliers of course will reduce our subscription fee and sales fee
# * Each supplier's subscribe fee is 80 BRL per month 
# * As the reduction of the product and orders, Sales fee will reduce around 335K BRL
# 
# ## Need to find the maximum profits by balancing the cost and revenue

# In[6]:


seller_sorted = sellers.sort_values(by='profits')
IT_cost = 3157.27 * (2967**0.5) + 978.23 * (seller_sorted['quantity'].sum() ** 0.5)
print(f"IT_cost is {IT_cost}")
print(f"Current Profit is {seller_sorted['profits'].sum()-IT_cost}")
print(f"Current Profit Margin is {(seller_sorted['profits'].sum()-IT_cost)/seller_sorted['revenues'].sum()*100}")


# In[7]:


def better_profit(remove_num):
    seller_test = seller_sorted[remove_num:]
    IT_cost = 3157.27 * (len(seller_test)**0.5) + 978.23 * (seller_test['quantity'].sum() ** 0.5)
    adjust_profit = seller_test['profits'].sum()-IT_cost
    return adjust_profit
    
def better_profit_margin(remove_num):
    seller_test = seller_sorted[remove_num:]
    IT_cost = 3157.27 * (len(seller_test)**0.5) + 978.23 * (seller_test['quantity'].sum() ** 0.5)
    profit_margin = (seller_test['profits'].sum()-IT_cost)/ (seller_test['revenues'].sum()) * 100
    return profit_margin       


# In[8]:


def IT_cost(remove_num):
   seller_test = seller_sorted[remove_num:]
   IT_cost_fee = 3157.27 * (len(seller_test)**0.5) + 978.23 * (seller_test['quantity'].sum() ** 0.5)
   return IT_cost_fee  


# In[9]:


print(IT_cost(855))


# In[10]:


numbers = list(range(1,len(seller_sorted)))
adjusted_profits = [better_profit(num) for num in numbers]
profit_margin = [better_profit_margin(num) for num in numbers]
df = pd.DataFrame({'removed_seller': numbers, 'profits':adjusted_profits,'Profit_Margin':profit_margin})

df


# In[11]:


df_sorted = df.sort_values(by='profits', ascending=False)
df_sorted


# In[41]:


# Plot the results
fig, ax1 = plt.subplots(figsize=(10,5))


# Plotting the first line chart on the left axis
ax1.plot(df['removed_seller'],df['profits'], color='tab:blue', label='Profits')
ax1.set_xlabel('Removed number of sellers')
ax1.set_ylabel('Total Profits', color='tab:blue')

# Create a second y-axis on the right side
ax2 = ax1.twinx()
ax2.plot(df['removed_seller'],df['Profit_Margin'], color='tab:red', label='Profit Margin')
ax2.set_ylabel('Profit Margin', color='tab:red')

# Adding legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

# Mark the maximum profit
max_profit_index = df['profits'].idxmax()
max_profit = df.loc[max_profit_index, 'profits'].round(0)
max_profit_x = df.loc[max_profit_index, 'removed_seller'].round(0)
ax1.scatter(max_profit_x, max_profit, color='green', label=f'Max Profit: {max_profit}', zorder=5)
ax1.annotate(f'Max Profit: {max_profit}', xy=(max_profit_x, max_profit), xytext=(max_profit_x + 0.5, max_profit),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

# Title
plt.title('Profit & Profit Margin with the changing number of sellers')

# Show plot
plt.show()


# In[37]:


import plotly.express as px

# Create figure with two y-axes
fig = px.line(df, x='removed_seller', y='profits', title='Profit & Profit Margin with the changing number of sellers')

# Add Profit Margin to the same plot
fig.add_scatter(x=df['removed_seller'], y=df['Profit_Margin'], mode='lines', name='Profit Margin', yaxis='y2')

# Update x-axis label
fig.update_xaxes(title_text='Removed number of sellers')

# Update y-axis labels
fig.update_yaxes(title_text='Total Profits', side='left', secondary_y=False)
fig.update_yaxes(title_text='Profit Margin', side='right', secondary_y=True)

# Show plot
fig.show()

