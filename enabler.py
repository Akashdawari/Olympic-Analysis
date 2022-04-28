
class Medal_Tally:

    """
    This Class handles the "Medal Tally Section".
    It has two methohs:
    1) fetch_medal_tally
    2) country_year_enabler
    """

    def __init__(self, df):
        self.df = df

    def fetch_medal_tally(self,yr, cou):

        """
        this method return a medal tally dataframe according to year and country selected
        :param yr: year
        :param cou: country
        :return: medal_tally: dataframe
        """
        try:
            flag = 0
            if yr == "Overall" and cou == "Overall":
                temp_df = self.df
            elif yr != "Overall" and cou == 'Overall':
                temp_df = self.df[self.df['Year'] == yr]
            elif yr == "Overall" and cou != 'Overall':
                temp_df = self.df[self.df['region'] == cou]
                flag = 1
            else:
                temp_df = self.df[(self.df['region'] == cou) & (self.df['Year'] == yr)]

            medal_df = temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
            if flag == 1:
                medal_tally = medal_df.groupby(by='Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                                          ascending=False).reset_index()
            else:
                medal_tally = medal_df.groupby(by='region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                            ascending=False).reset_index()
            medal_tally['Gold'] = medal_tally['Gold'].astype('int64')
            medal_tally['Silver'] = medal_tally['Silver'].astype('int64')
            medal_tally['Bronze'] = medal_tally['Bronze'].astype('int64')
            medal_tally['Total Medals'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']
            return medal_tally

        except Exception as e:
            raise e

    def country_year_enabler(self):

        """
        This method return two list i.e. of years and countries
        :return: countries, years: both are list
        """
        try:
            countries = sorted((self.df['region'].dropna().unique().tolist()))
            countries.insert(0,'Overall')
            years = sorted(self.df['Year'].unique().tolist())
            years.insert(0, 'Overall')
            return countries, years
        except Exception as e:
            raise e

class Overall:

    """
    This Class handles the "Overall Section".
    It has six methohs:
    1) top_statistic
    2) nation_participation_every_year
    3) events_every_year
    4) athletes_participation_every_year
    5) sports_heatmap
    6) most_achivers
    """
    def __init__(self, df):
        self.df = df

    def top_statistic(self):

        """
        This method calculate the number of editions,host,sports,events,nations,athletes
        :return: editions,host,sports,events,nations,athletes
        """
        try:
            # No. of times olympic held
            editions = self.df.Year.unique().shape[0] - 1
            # No. of city hosted olympic
            host = self.df.City.unique().shape[0]
            # No. of sport played in olympic
            sports = self.df.Sport.unique().shape[0]
            # No. of events held in olympic
            events = self.df.Event.unique().shape[0]
            # No. of nation participated in olympic
            nations = self.df.region.unique().shape[0]
            # No. of atheletes participated in olympic
            athletes = self.df.Name.unique().shape[0]
            return editions,host,sports,events,nations,athletes
        except Exception as e:
            raise e

    def nation_participation_every_year(self):

        """
        This method construct two list
        1) x: Year list when olympic organized
        2) y: number of countries list participated at that year
        :return: x,y
        """
        try:
            x = sorted(self.df['Year'].unique().tolist())
            y = [self.df[self.df['Year'] == i]['region'].unique().shape[0] for i in x]
            return x,y
        except Exception as e:
            raise e

    def events_every_year(self):

        """
            This method construct two list
            1) x: Year list when olympic organized
            2) y: number of Events list held at that year
            :return: x,y
        """
        try:
            x = sorted(self.df['Year'].unique().tolist())
            y = [self.df[self.df['Year'] == i]['Event'].unique().shape[0] for i in x]
            return x, y
        except Exception as e:
            raise e

    def athletes_participation_every_year(self):

        """
            This method construct two list
            1) x: Year list when olympic organized
            2) y: number of athletes list participated at that year
            :return: x,y
        """
        try:
            x = sorted(self.df['Year'].unique().tolist())
            y = [self.df[self.df['Year'] == i]['Name'].unique().shape[0] for i in x]
            return x,y
        except Exception as e:
            raise e

    def sports_heatmap(self):

        """
        This method construct a pivot table
        :return: pt: pivot table
        """
        try:
            x = self.df.drop_duplicates(['Year','Sport','Event'])
            pt = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')

            return pt
        except Exception as e:
            raise e

    def most_achivers(self,sports):


        """
        This method a dataframe of top achivers in their respective sports.
        :param sports: string
        :return: kt: dataframe
        """
        try:
            temp_df = self.df.dropna(subset=['Medal'])

            if sports != 'Overall':
                temp_df = temp_df[temp_df['Sport'] == sports]

            kt = temp_df['Name'].value_counts().reset_index().merge(self.df, left_on='index', right_on='Name', how='left')[
                ['index', 'region', 'Sport', 'Name_x']].drop_duplicates().head(15)
            kt.rename(columns={'Name_x': 'Total Medals', 'index': 'Name'}, inplace=True)
            return kt
        except Exception as e:
            raise e

class CountryWise:
    """
    This Class handles the "CountryWise Section".
    It has three methohs:
    1) medal_tally
    2) sport_analysis_heatmap
    3) most_achivers_countrywise
    """
    def __init__(self, df):
        self.df = df

    def medal_tally(self, country):

        """
        This method construct a dataframe of medals achived by a country every year.
        :param country: string
        :return: temp_df: dataframe
        """
        try:
            temp_df = self.df.dropna(subset=['Medal']).drop_duplicates(['Team', 'Year', 'region', 'Team', 'Games', 'Event'])
            temp_df = temp_df[temp_df['region'] == country]
            temp_df = temp_df.groupby('Year').count()['Medal'].reset_index()
            return temp_df
        except Exception as e:
            raise e

    def sport_analysis(self, country):

        """
        This method construct a pivot table
        :param country: string
        :return: heatmap: pivot table
        """
        try:
            temp_df = self.df.dropna(subset=['Medal']).drop_duplicates(['Team', 'Year', 'region', 'Team', 'Games', 'Event'])
            temp_df = temp_df[temp_df['region'] == country]
            pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
            return pt
        except Exception as e:
            raise e

    def most_achivers_countrywise(self,country):

        """
        This method construct a dataframe of top achivers of their respective countries
        :param country: string
        :return: kt: pd.Dataframe
        """
        try:
            temp_df = self.df.dropna(subset=['Medal'])
            temp_df = temp_df[temp_df['region'] == country]
            kt = temp_df['Name'].value_counts().reset_index().merge(self.df, left_on='index', right_on='Name', how='left')[
                ['index', 'Sport', 'Name_x']].drop_duplicates().head(10)
            kt.rename(columns={'Name_x': 'Total Medals', 'index': 'Name'}, inplace=True)
            return kt
        except Exception as e:
            raise e

class AthletesWise:
    """
    This Class handles the "AthletesWise Section".
    It has four methohs:
    1) age_distripution
    2) age_distribution_wrt_sport
    3) height_weight_distribution
    4) male_female_compare
    """

    def __init__(self,df):
        self.df=df

    def age_distripution(self):

        """
        This method calculate the ages of achiveing medals.
        :return: [x1,x2,x3,x4] : list
        """
        try:
            temp_df = self.df.drop_duplicates(subset=['Name', 'Height', 'Weight', 'region'])
            x1 = temp_df['Age'].dropna()
            x2 = temp_df[temp_df['Gold'] == 1]['Age'].dropna()
            x3 = temp_df[temp_df['Silver'] == 1]['Age'].dropna()
            x4 = temp_df[temp_df['Bronze'] == 1]['Age'].dropna()
            return [x1,x2,x3,x4]

        except Exception as e:
            raise e

    def age_distribution_wrt_sport(self):

        """
        this method calculate the ages of achiveing medals w.r.t. sports
        :return: lt: list
        :return: sport_name: string
        """
        try:
            temp_df = self.df.drop_duplicates(subset=['Name', 'Height', 'Weight', 'region'])
            sports = sorted(self.df['Sport'].unique().tolist())
            lt=[]
            sport_name = []
            for i in sports:
                pre_df = temp_df[temp_df['Sport'] == i]
                x = pre_df[pre_df['Gold'] == 1]['Age'].dropna()
                if len(x) > 2:
                    lt.append(x)
                    sport_name.append(i)
            return lt, sport_name

        except Exception as e:
            raise e

    def height_weight_distribution(self,sport):

        """
        This method filter the dataframe and return filtered dataframe.
        :param sport: string
        :return: fig: dataframe
        """
        try:
            temp_df = self.df.drop_duplicates(subset=['Name', 'Height', 'Weight', 'region'])
            temp_df['Medal'].fillna('No Medal', inplace=True)
            temp_df = temp_df[temp_df['Sport'] == sport]
            # fig = sb.scatterplot(x=temp_df['Height'], y=temp_df['Weight'], hue=temp_df['Medal'], style=temp_df['Sex'], s=500)
            return temp_df
        except Exception as e:
            raise e

    def male_female_compare(self):

        """
        This method construct a dataframe of male and female participated every year.
        :return: sex: dataframe
        """
        try:
            temp_df = self.df.drop_duplicates(subset=['Name', 'Height', 'Weight', 'region', 'Year', 'Event'])
            male = temp_df[temp_df['Sex'] == 'M'].groupby('Year').count()['Sex'].reset_index()
            female = temp_df[temp_df['Sex'] == 'F'].groupby('Year').count()['Sex'].reset_index()
            sex = male.merge(female, how='left', on='Year').rename(columns={'Sex_x': 'Male', 'Sex_y': 'Female'}).fillna(0).astype('int')
            return sex
        except Exception as e:
            raise e