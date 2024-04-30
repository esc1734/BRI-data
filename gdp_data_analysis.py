# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# %%
# dataset: https://greenfdc.org/countries-of-the-belt-and-road-initiative-bri/
BR_countries = pd.read_excel('/Users/emma/Desktop/gened_1068/23_12_BRI-countries-public.xlsx', sheet_name='BRI countries')

# Drop rows with NaT values in the 'Likely date of joining' column
BR_countries = BR_countries.dropna(subset=['Likely date of joining'])
BR_countries = BR_countries.reset_index(drop=True)

# # Display the DataFrame after dropping rows
# print(BR_countries.head(10))
print(BR_countries['Country'].head(10))


# %%
print(BR_countries['IncomeGroup'].unique())

# %%
# dataset: https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
GDP = pd.read_excel('/Users/emma/Desktop/gened_1068/GDP_data.xlsx', sheet_name='Data')

# Drop the first two rows
GDP = GDP.drop([0,1])
GDP = GDP.reset_index(drop=True)

## Drop 'Country Code', 'Indicator Name', and 'Indicator Code' columns
GDP = GDP.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

# # Display the DataFrame after dropping rows
# print(GDP.head())
print(GDP.columns)


# %%
## add columns 1960 through 2023 to the BR_countries DataFrame
years = [str(year) for year in range(2000, 2024)]
for year in years:
    BR_countries[year] = None

# For each country in BR_countries, find the corresponding row in GDP and copy the GDP growth rate for each year
for i in range(len(BR_countries)):
    country = BR_countries['Country'][i]
    row = GDP[GDP['Country Name'] == country]
    if row.empty:
        continue
    for year in years:
        BR_countries.at[i, year] = row[year].values[0]

# %%
## drop rows corresponding to BR countries from the GDP DataFrame
non_BR = GDP[~GDP['Country Name'].isin(BR_countries['Country'])]


# %%
# get average GDP growth rates

years = np.linspace(2000, 2023, 24)
BR_avgs = []
non_BR_avgs = []
BR_low = []
BR_lowmed = []
BR_upmed = []
BR_high = []

for year in years:
    BR_avgs.append(BR_countries[str(int(year))].mean())
    non_BR_avgs.append(non_BR[str(int(year))].mean())
    BR_low.append(BR_countries[BR_countries['IncomeGroup'] == 'Low income'][str(int(year))].mean())
    BR_lowmed.append(BR_countries[BR_countries['IncomeGroup'] == 'Lower middle income'][str(int(year))].mean())
    BR_upmed.append(BR_countries[BR_countries['IncomeGroup'] == 'Upper middle income'][str(int(year))].mean())
    BR_high.append(BR_countries[BR_countries['IncomeGroup'] == 'High income'][str(int(year))].mean())

# %%
# ## find average year of joining for BR countries
# dates = []
# for date in BR_countries['Likely date of joining']:
#     dates.append(datetime.strptime(str(date), '%Y-%m-%d'))
# average_date = sum(dates, datetime(1, 1, 1)) / len(dates)
join_date_avgs = []

for i in ['Low income', 'Lower middle income', 'Upper middle income', 'High income']:
    join_date_avgs.append(BR_countries[BR_countries['IncomeGroup'] == i]['Likely date of joining'].mean())

join_date_avgs.append(BR_countries['Likely date of joining'].mean())
print(join_date_avgs)

# %%
## plot years from 2008 to 2023 on the x-axis and the average GDP growth rate on the y-axis
plt.xlabel('Year')
plt.ylabel('Average GDP Growth Rate (%)')
plt.title('Average GDP Growth Rate (%) of BRI Countries by Income Group')
plt.plot(years[8:], BR_low[8:], color='m',label='Low Income BRI countries')
# plt.plot(years[8:], BR_lowmed[8:], color='c',label='Lower Middle Income Income BRI countries')
# plt.plot(years[8:], BR_upmed[8:], color='g',label='Upper Middle Income Income BRI countries')
plt.plot(years[8:], BR_high[8:], color='y',label='High Income Income BRI countries')
plt.plot(years[8:], non_BR_avgs[8:], color='b',label='Non-BRI countries')
# plt.plot(years[8:], non_BR_avgs[8:], color='blue',label='Non-BRI countries')
plt.legend()
plt.show()

# %%
## plot years from 2008 to 2023 on the x-axis and the average GDP growth rate on the y-axis
plt.xlabel('Year')
plt.ylabel('Average GDP Growth Rate (%)')
plt.title('Average GDP Growth Rate (%) for BRI and Non-BRI Countries')
plt.plot(years[8:], BR_avgs[8:], color='r',label='All BRI countries')
plt.plot(years[8:], non_BR_avgs[8:], color='blue',label='Non-BRI countries')
plt.legend()
plt.show()

# %%


# %%
gdp_specific = GDP[GDP['Country Name'] == 'Pakistan']
country = 'Pakistan'

pre = []
post = []

# Check if the country is found in the GDP dataset
if not gdp_specific.empty:
  # Extract years and percent change in GDP
  years = gdp_specific.columns[4:]  # Assuming the first four columns are not years
  percent_change_gdp = gdp_specific.iloc[0, 4:]

  # Remove missing values
  years = [year for year, gdp in zip(years, percent_change_gdp) if pd.notnull(gdp)]
  percent_change_gdp = [gdp for gdp in percent_change_gdp if pd.notnull(gdp)]

  # Get the joining date of the country and extract the year
  join_date = BR_countries[BR_countries['Country'] == country]['Likely date of joining'].values[0]
  join_year = pd.to_datetime(join_date, format='%m/%d/%y').year

  # Adjust to start plotting from 2000 onwards
  start_year = 2005

  # Plotting
plt.figure(figsize=(12,6))
plt.title('Pakistan')
plt.xlabel('Year')
plt.ylabel('Change in GDP (%)')
plt.plot(years[start_year - 1960:join_year - 1960], percent_change_gdp[start_year - 1960:join_year - 1960], marker='o', label='Before joining BRI', color='blue')
plt.plot(years[join_year - 1960 - 1:], percent_change_gdp[join_year - 1960 - 1:], marker='o', label='After joining BRI', color='red')
plt.legend()
# add horizontal lines to indicate average growth before and after joining
plt.axhline(y=np.mean(percent_change_gdp[start_year - 1960:join_year - 1960]), color='blue', linestyle='--')
plt.axhline(y=np.mean(percent_change_gdp[join_year - 1960 - 1:]), color='red', linestyle='--')
plt.show()


# %%
print("Pakistan average 2008 - 2014 (before joining BRI): " + str(np.mean(percent_change_gdp[start_year - 1960:join_year - 1960])))
print("Pakistan average 2015 - 2022 (after joining BRI): " + str(np.mean(percent_change_gdp[join_year - 1960 - 1:])))

# %%



