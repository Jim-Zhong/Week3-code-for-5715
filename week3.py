import sys
import numpy as np
import pandas as pd
import seaborn as sns
import pandasql as ps
from matplotlib import pyplot as plt

def main():
    script = sys.argv[0]
    locations = sys.argv[1:]
    df_loaction = pd.DataFrame(locations)
    df_loaction.rename(columns={0:'loaction'},inplace=True)
    df=pd.read_csv('covid-locations.csv')
    list1=[]
    list2=[]
    df_list = df['location'].tolist()
    if sys.argv == ['week3.py']:
        print('Error: No Locations were specified. Cannot proceed.')
        print('Please specify locations like so:')
        print("python3 week3.py 'Australia' 'Brazil' 'New Zealand'")
    else :
        for location in locations:
            if location in df_list:
                list1.append(location)
            else :
                list2.append(location)
        
        if len(list2) == 0:
            print('Generating visualisation for' + str(list1))
            df_covid_data = pd.read_csv('owid-covid-data.csv')
            df_select= ps.sqldf(
	            "SELECT c.location, c.people_fully_vaccinated_per_hundred, c.date "
	            + " FROM df_covid_data as c inner join df_loaction as l"
                + " on c.location = l.loaction "
            )

            df_select = df_select.dropna(subset = ['people_fully_vaccinated_per_hundred'])
            df_select['date'] = pd.to_datetime(df_select['date'])
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(1,1,1)
            sb_lineplot = sns.lineplot(x='date', y='people_fully_vaccinated_per_hundred', hue='location', markers=True, data=df_select)
            ax.set_title("COVID-19 people FULLY vaccinated per hundred: Wallia and Japan/Liechtenstein/Greece/Monaco/Hungary")
            plt.xticks(rotation=20)
            plt.savefig('001.png')
            #df_select.to_csv("chartdata.csv")

        
        else:
            print('Error: Locations' + str(list2) + ' are not found in dataset. Cannot proceed.')

if __name__ == '__main__':
    main()