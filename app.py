import streamlit as st
import plotly.express as px
import plotly.figure_factory as ft
from DataPreproccessing import Dataprocess
import enabler
from datetime import datetime
from logger import App_Logger


def application():
    try:

        log = App_Logger()
        obj = datetime.now()
        date = ''.join(map(str, str(obj.date()).split('-')))
        time = ''.join(map(str, str(obj.time()).split(':')))
        log_file = open('logs/log-' + date + '-' + time + '.txt', 'w+')
        log.log(log_file, " Starting App ")  #log
        st.sidebar.title("Olympic Analysis")
        st.sidebar.image('Olympic_Logo.png')


        seasons = ["Summer","Winter"]
        season = st.sidebar.radio("Season", seasons)
        log.log(log_file, " DataProccessing Step!! ") #log
        Dproccess = Dataprocess(log_file)
        df = Dproccess.preprocess(season)
        log.log(log_file, " Successfully get the dataframe!! ")  # log
        user_menu = st.sidebar.radio(
            'Select as option',
            ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
        )


        if user_menu == 'Medal Tally':

            try:
                log.log(log_file, " Medal Tally Section ")  # log
                medalTally = enabler.Medal_Tally(df,log_file)
                st.sidebar.header("Medal Tally")
                countries, years = medalTally.country_year_enabler()
                year_dropdown = st.sidebar.selectbox("Select Year", years)
                countries_dropdown = st.sidebar.selectbox("Select Country", countries)
                if countries_dropdown !="Overall":
                    st.title("Medal Tally of "+countries_dropdown)
                else:
                    st.title("Overall Medal Tally")
                medal_tally = medalTally.fetch_medal_tally(year_dropdown, countries_dropdown)
                st.table(medal_tally)
            except Exception as e:
                raise e

        elif user_menu == 'Overall Analysis':
            try:
                log.log(log_file, " Overall Analysis Section ")  # log
                st.title("Top Statistic")
                topstat = enabler.Overall(df,log_file)
                editions,host,sports,events,nations,athletes = topstat.top_statistic()

                col1,col2,col3 = st.columns(3)
                with col1:
                    st.header("Editions")
                    st.title(editions)
                with col2:
                    st.header("Hosts")
                    st.title(host)
                with col3:
                    st.header("Sports")
                    st.title(sports)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.header("Events")
                    st.title(events)
                with col2:
                    st.header("Nations")
                    st.title(nations)
                with col3:
                    st.header("Athletes")
                    st.title(athletes)

                x,y = topstat.nation_participation_every_year()
                fig = px.line(x=x, y=y, labels={'x': "Year", 'y': "Nations participated"})
                st.title("Participating countries over the years")
                st.plotly_chart(fig)

                x, y = topstat.events_every_year()
                fig = px.line(x=x, y=y, labels={'x': "Year", 'y': "Events"})
                st.title("Events over the years")
                st.plotly_chart(fig)

                x, y = topstat.athletes_participation_every_year()
                fig = px.line(x=x, y=y, labels={'x': "Year", 'y': "Athletes"})
                st.title("Athletes participated over the years")
                st.plotly_chart(fig)

                st.title("No.of Events over years (Every Sports)")
                ax = topstat.sports_heatmap()
                fig = px.imshow(ax, text_auto=True, aspect="auto",  color_continuous_scale='RdBu_r', origin='lower')
                fig.update_layout(autosize=False, width=900, height=1000)
                st.plotly_chart(fig)

                st.title("Most Successful Athletes")
                sports = df['Sport'].drop_duplicates().tolist()
                sports.sort()
                sports.insert(0, 'Overall')
                selected_sport = st.selectbox("Select Sport",sports)
                achivers = topstat.most_achivers(selected_sport)
                st.table(achivers)
            except Exception as e:
                raise e

        elif user_menu == 'Country-wise Analysis':
            try:
                log.log(log_file, " Country-wise Analysis Section ")  # log
                cwa = enabler.CountryWise(df,log_file)

                st.sidebar.title("Country Wise Medal Tally")
                temp_df = df.dropna(subset=['Medal'])
                country = temp_df['region'].dropna().unique().tolist()
                country.sort()
                selected_country = st.sidebar.selectbox("Select country", country)

                st.title(selected_country+ " Medal Tally Over The Years")
                medaltally = cwa.medal_tally(selected_country)
                fig = px.line(medaltally, x='Year', y='Medal', labels={'x': "Year", 'y': "Medal"})
                st.plotly_chart(fig)

                st.title(selected_country + " performance in different sports over the year")
                ax = cwa.sport_analysis(selected_country)
                fig = px.imshow(ax, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', origin='lower')
                fig.update_layout(autosize=False, width=900, height=1000)
                st.plotly_chart(fig)

                st.title(selected_country + " most medal winners athletes")
                st.table(cwa.most_achivers_countrywise(selected_country))
            except Exception as e:
                raise e

        else:
            try:
                log.log(log_file, "AthletesWise Analysis Section ")  # log
                athl = enabler.AthletesWise(df,log_file)

                lt = athl.age_distripution()

                st.title("Distribution of Age")
                fig = ft.create_distplot(lt,['Overall Age','Gold Age','Silver age', 'Bronze age'], show_hist=False,show_rug=False )
                fig.update_layout(autosize=False, width=900, height=500)
                st.plotly_chart(fig)

                lt,sports = athl.age_distribution_wrt_sport()
                st.title("Distribution of Age w.r.t. Sports(Gold Medalist)")
                fig = ft.create_distplot(lt, sports, show_hist=False,
                                         show_rug=False)
                fig.update_layout(autosize=False, width=900, height=500)
                st.plotly_chart(fig)

                st.title("Distribution of Age w.r.t. Sports(Gold Medalist)")
                sport = st.selectbox("select sport",sorted(df['Sport'].unique().tolist()))
                ax = athl.height_weight_distribution(sport)
                fig = px.scatter(ax, x='Height', y='Weight', color="Medal",
                                 symbol="Sex",color_discrete_sequence=['lightskyblue','brown','silver', 'goldenrod' ],
                                 symbol_sequence= ['circle', 'cross'])
                fig.update_layout(autosize=False, width=900, height=600)

                st.plotly_chart(fig)

                st.title("Compare Male & Female participation over year")
                sex_df = athl.male_female_compare()
                fig = px.line(sex_df, x='Year', y=['Male', 'Female'], )
                fig.update_layout(autosize=False, width=900, height=500)
                st.plotly_chart(fig)
            except Exception as e:
                log.log(log_file, " ERROR :: " + str(e))  # log
                raise e

    except Exception as e:
        raise e

if __name__ == "__main__":

    application()
