import pandas as pd

try:
    athlete_events_df = pd.read_csv("Data/athlete_events.csv")
    noc_regions_df = pd.read_csv("Data/noc_regions.csv")

    def preprocess(season):

        """
        This function process the data w.r.t. season
        :param season: string
        :return: athlete_df :dataframe
        """
        try:
            global athlete_events_df, noc_regions_df

            #filtering for summer olympics
            athlete_df = athlete_events_df[athlete_events_df['Season']==season]

            #droping duplicate rows
            athlete_df.drop_duplicates(inplace=True)

            #Joining noc_regions_df with the current df to get region
            athlete_df = athlete_df.merge(noc_regions_df, on='NOC', how='left')

            #Converting medal column into onhotcoding/dummy column
            athlete_df = pd.concat([athlete_df, pd.get_dummies(athlete_df['Medal'])], axis=1)

            return athlete_df
        except Exception as e:
            raise e
except Exception as e:
    raise e