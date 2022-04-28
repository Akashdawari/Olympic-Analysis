import pandas as pd
from logger import App_Logger

class Dataprocess:

    def __init__(self,log_file):
        self.log_file = log_file
        self.log = App_Logger()


    def retriveData(self):

        """
        this method extract and initilize the data
        :return:
        """
        try:
            self.athlete_events_df = pd.read_csv("Data/athlete_events.csv")
            self.noc_regions_df = pd.read_csv("Data/noc_regions.csv")
            self.log.log(self.log_file, " Successfully extract data!!! ")  # log
        except Exception as e:
            self.log.log(self.log_file, " ERROR :: "+str(e))  # log
            raise e

    def preprocess(self,season):

        """
        This method process the data w.r.t. season
        :param season: string
        :return: athlete_df :dataframe
        """
        try:
            self.retriveData()
            self.log.log(self.log_file, " proccessing  data!!! ")  # log
            #filtering for summer olympics
            athlete_df = self.athlete_events_df[self.athlete_events_df['Season']==season]

            #droping duplicate rows
            athlete_df.drop_duplicates(inplace=True)

            #Joining noc_regions_df with the current df to get region
            athlete_df = athlete_df.merge(self.noc_regions_df, on='NOC', how='left')

            #Converting medal column into onhotcoding/dummy column
            athlete_df = pd.concat([athlete_df, pd.get_dummies(athlete_df['Medal'])], axis=1)
            self.log.log(self.log_file, " returning filtered and clean data!!! ")  # log
            return athlete_df
        except Exception as e:
            self.log.log(self.log_file, " ERROR :: " + str(e))  # log
            raise e
