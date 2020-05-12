'''
@authors: Sagiv Asraf 312527450
          Liran Katz  204483226
        Project Pandas Show and Analyzing Data Using Pandas
---------------------------------------------------------
  TODO -> Change description for our PANDAS project.
  /*
  module_name, package_name, ClassName, method_name,
   ExceptionName, function_name, GLOBAL_CONSTANT_NAME,
   global_var_name, instance_var_name, function_parameter_name,
   local_var_name.
  */

---------------------------------------------------------
'''
import pandas as pd
from Utils import Constants
from Utils.EmailManagement import EmailManagement
from Utils.PandasLogger import PandasLogger
from tabulate import tabulate
import matplotlib.pyplot as plt
import json


def main():
    plt.close('all')
    set_pd_options(pd)
    pandas_logger = set_logger()
    pandas_logger.info('Start collecting data for seminary project\n')

    data_frame = pd.read_csv('Survey Data Files/survey_results_public.csv')
    schema_data_frame = pd.read_csv("Survey Data Files/survey_results_schema.csv")
    pandas_logger.info('Some basic details (META-DATA) on our data:')

    time_the_graph_will_be_displayed_in_seconds, email, statistical_analysis_type_of_viewing, should_be_displayed = read_configurations_file()

    shape = data_frame.shape;
    rows = shape[0]
    cols = shape[1]

    set_plt_size()

    print_some_meta_data_on_the_data(schema_data_frame, pandas_logger, rows, cols)

    print_general_median_data(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                              statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_hobbies(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                          statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_social_media(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                               statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_participants_countries(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                                         statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_israelis(data_frame, pandas_logger, rows, time_the_graph_will_be_displayed_in_seconds,
                           statistical_analysis_type_of_viewing, should_be_displayed)

    high_salary_results = get_high_salary_results_after_filtered(data_frame)

    print_data_on_participants_high_salary(data_frame, pandas_logger, rows, high_salary_results,
                                           time_the_graph_will_be_displayed_in_seconds,
                                           statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_israelis_whos_have_high_salary(pandas_logger, high_salary_results,
                                                 time_the_graph_will_be_displayed_in_seconds,
                                                 statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_man_vs_women_salaries(pandas_logger, high_salary_results, time_the_graph_will_be_displayed_in_seconds,
                                        statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_participants_salaries_by_countries(data_frame, pandas_logger,
                                                     time_the_graph_will_be_displayed_in_seconds,
                                                     statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_programing_languages_high_salaries(pandas_logger, high_salary_results,
                                                     time_the_graph_will_be_displayed_in_seconds,
                                                     statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_israelis_known_languages(data_frame, pandas_logger,
                                           time_the_graph_will_be_displayed_in_seconds,
                                           statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_hobbies_and_salaries(data_frame, pandas_logger,
                                       time_the_graph_will_be_displayed_in_seconds,
                                       statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_years_of_experience_and_salaries(data_frame, pandas_logger,
                                                   time_the_graph_will_be_displayed_in_seconds,
                                                   statistical_analysis_type_of_viewing, should_be_displayed)

    print_data_on_women_men_salaries_by_countries(data_frame, pandas_logger,
                                                  time_the_graph_will_be_displayed_in_seconds,
                                                  statistical_analysis_type_of_viewing, should_be_displayed)

    # ************* Send the log file to my mail *************
    send_log_file_in_mail(email, pandas_logger)

    print("Finished, you can now watch your results in the log file ! :)")


def read_configurations_file():
    with open('config.json') as json_file:
        data = json.load(json_file)
        configurations = data['configurations']
        time_the_graph_will_be_displayed_in_seconds = int(configurations['time graph will be displayed in seconds'])
        email = configurations['email']
        statistical_analysis_type_of_viewing = configurations['statistical analysis displayed in diagram or pie']
        should_be_displayed = configurations['should be displayed']

    return time_the_graph_will_be_displayed_in_seconds, email, statistical_analysis_type_of_viewing, should_be_displayed


def send_log_file_in_mail(receiver_mail, pandas_logger):
    seminar_mail = "pandasseminar@gmail.com"
    seminar_password = "pandasseminarpython"

    log_file_name = extract_log_file_name(pandas_logger)

    EmailManagement.send_email(seminar_mail, seminar_password, receiver_mail, log_file_name)


def print_some_meta_data_on_the_data(schema_data_frame, pandas_logger, rows, cols):
    pandas_logger.info("We have %d rows and %d columns of data in our survey" % (rows, cols))
    pandas_logger.info("We asked our participants the following questions: \n %s",
                       tabulate(schema_data_frame, headers='keys', tablefmt='psql', showindex=False))


def print_general_median_data(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                              statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Median data on participants participants"

    if should_be_displayed[title] == "yes":
        median = data_frame.median()
        salary_median = round(median['ConvertedComp'] / 12, 2)
        age_median = median['Age']
        work_weeks_hours_median = median['WorkWeekHrs']

        pandas_logger.info("\n\n************* Medians Data: *************\n ")
        pandas_logger.info(
            "The median age of our participants is: %d \nThe median salary of our participants is: %d \nThe median "
            "weekly hours of our participants is: %d" % (
                age_median, salary_median, work_weeks_hours_median))

        labels = ["Age", "Month salary", "Weekly work hours"]
        data = [age_median, salary_median, work_weeks_hours_median]
        colors = ['gold', 'lightskyblue', 'lightcoral']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_hobbies(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                          statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Programming as a hobby"
    if should_be_displayed[title] == "yes":
        programming_as_a_hobby = data_frame["Hobbyist"].value_counts()
        yes = programming_as_a_hobby['Yes']
        no = programming_as_a_hobby['No']

        pandas_logger.info("\n\n************* Hobbies Data: *************\n ")
        pandas_logger.info(
            "\n%d claims they programmingas a hobby \nAnd %d says the does not programming as a hobby" % (
                yes, no))
        pandas_logger.info("\n We can see that most of our participants claim that they are programming as hooby!")

        labels = ["Yes", "No"]
        data = [yes, no]
        colors = ['gold', 'red']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_social_media(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                               statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Social media usage"
    if should_be_displayed[title] == "yes":
        social_media = data_frame["SocialMedia"].value_counts()
        facebook = social_media['Facebook']
        twitter = social_media['Twitter']
        whatsapp = social_media['WhatsApp']
        youtube = social_media['YouTube']
        linkedin = social_media['LinkedIn']
        instagram = social_media['Instagram']
        not_using = social_media["I don't use social media"]

        pandas_logger.info("\n\n************* Social media Data: *************\n ")
        pandas_logger.info(
            "\n%d claims they using Facebook.\n%d claims they using Twitter:,\n%d claims they using WhtasApp:,"
            "\n%d claims they using Youtube:,\n%d claims they using Linkedin:, \n%d claims they using Instagram:,\n%d claims they are not using social media." % (
                facebook, twitter, whatsapp, youtube, linkedin, instagram, not_using))

        labels = ["Facebook", "Twitter", "WhatsApp", "YouTube", "Linkedin", "Instagram", "I don't use social media"]
        data = [facebook, twitter, whatsapp, youtube, linkedin, instagram, not_using]
        colors = ['blue', 'lightskyblue', 'green', 'red', 'gold', 'pink', 'darkgrey']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_participants_countries(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                                         statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Participants came from:"
    if should_be_displayed[title] == "yes":
        participants_counties = data_frame["Country"].value_counts()
        united_states = participants_counties['United States']
        india = participants_counties['India']
        germany = participants_counties['Germany']
        united_kingdom = participants_counties['United Kingdom']
        spain = participants_counties['Spain']
        italy = participants_counties['Italy']
        israel = participants_counties['Israel']

        pandas_logger.info("\n\n************* Participants came from: *************\n ")
        pandas_logger.info(
            "\n%d Says they came from the United States.\n%d Says they came from India\n%d Says they came from Germany."
            "\n%d Says they came from United Kingdom.\n%d Says they came from Spain\n%d Says they came from Italy.\n%d Says they came from Israel.\n" % (
                united_states, india, germany, united_kingdom, spain, italy, israel))
        pandas_logger.info("\nWe can see from the results that a lot of the participants are americans, but we (Israel) have "
                           "respectable representation in this survey")

        labels = ["United States", "India", "Germany", "United Kingdom", "Spain", "Italy", "Israel"]
        data = [united_states, india, germany, united_kingdom, spain, italy, israel]
        colors = ['red', 'lightgrey', 'yellow', 'blue', 'yellow', 'lightgreen', 'lightblue']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_israelis(data_frame, pandas_logger, rows, time_the_graph_will_be_displayed_in_seconds,
                           statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Israelis Participants V.S All other participants"
    if should_be_displayed[title] == "yes":
        israel_filter = (data_frame['Country'] == "Israel");
        israel_participants = data_frame.loc[
            israel_filter, ['Respondent', 'Country', 'Gender', 'Student', 'LanguageWorkedWith', 'ConvertedComp']]
        pandas_logger.info("\n\n************* Israelis participants: *************\n ")
        pandas_logger.info(
            "Due to the fact we have %d Israelis participants we will display the first 100" % (
                len(israel_participants)))
        pandas_logger.info(tabulate(israel_participants.head(100), headers='keys', tablefmt='psql', showindex=False))
        pandas_logger.info(
            "\n***************************** %d From %d of our participants are Israelis! Respect *****************************\n" % (
                len(israel_participants), rows));

        labels = ["Israelis Participant", "All other participants"]
        data = [len(israel_participants), rows - len(israel_participants)]
        colors = ['lightskyblue', 'gold']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_participants_high_salary(data_frame, pandas_logger, rows, high_salary_results,
                                           time_the_graph_will_be_displayed_in_seconds,
                                           statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Participants who earn who earn high salary V.S Other participants"

    if should_be_displayed[title] == "yes":
        pandas_logger.info("\nThe following table contains people who makes more than %s per month -> focused on "
                           "Country, the programming language they worked with and of course the yearly salary\n",
                           Constants.HIGH_SALARY_STRING)

        # Sort our data_frame by salaries!
        data_frame.sort_values(by='ConvertedComp', inplace=True, ascending=False)

        pandas_logger.info(
            "Due to the fact we have %d participants that earn more than %s per month, We will display just the TOP 100 (sorted by salaries!)" % (
                len(high_salary_results), Constants.HIGH_SALARY_STRING))

        pandas_logger.info(tabulate(high_salary_results.head(100), headers='keys', tablefmt='psql', showindex=False))

        pandas_logger.info("lets Analyze this data")
        pandas_logger.info(
            "%d From %d of our participants, earn more than %s per month" % (
                len(high_salary_results), rows, Constants.HIGH_SALARY_STRING));

        pandas_logger.info("In percentage: %d%% from our participants earn more than %s per month" % (
            (len(high_salary_results) * 100) / rows, Constants.HIGH_SALARY_STRING));

        labels = ["Earn more than " + Constants.HIGH_SALARY_STRING + " Participants", "All other participants"]
        data = [len(high_salary_results), rows - len(high_salary_results)]
        colors = ['yellowgreen', 'lightcoral']
        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_israelis_whos_have_high_salary(pandas_logger, high_salary_results,
                                                 time_the_graph_will_be_displayed_in_seconds,
                                                 statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Israelis who earn high salary V.S All other participants who earn high salary"
    if should_be_displayed[title] == "yes":
        pandas_logger.info("\n\n************* Israelis High salary participants: *************\n ")
        israel_high_salary_filter = high_salary_results["Country"].eq("Israel");
        israel_high_salary_results = high_salary_results.loc[israel_high_salary_filter]
        pandas_logger.info(tabulate(israel_high_salary_results, headers='keys', tablefmt='psql', showindex=False))
        pandas_logger.info("\n%d From %d of our participants, which earn more than %s per month are Israelis" % (
            len(israel_high_salary_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

        labels = ["Israelis who earn High Salary", "All other participants who earn high salary"]
        data = [len(israel_high_salary_results), len(high_salary_results) - len(israel_high_salary_results)]
        colors = ['lightskyblue', 'yellowgreen']
        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_man_vs_women_salaries(pandas_logger, high_salary_results,
                                        time_the_graph_will_be_displayed_in_seconds,
                                        statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Men who earn High Salary V.S Women who earn high salary"
    if should_be_displayed[title] == "yes":
        pandas_logger.info("\n\n************* Women VS Men High salary participants: *************\n ")
        women_high_salary_filter = high_salary_results["Gender"].eq("Woman");
        men_high_salary_filter = high_salary_results["Gender"].eq("Man");

        women_high_salary_results = high_salary_results.loc[women_high_salary_filter]
        men_high_salary_results = high_salary_results.loc[men_high_salary_filter]

        pandas_logger.info("%d From %d are women which earn more than %s per month" % (
            len(women_high_salary_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));
        pandas_logger.info("%d From %d are men which earn more than %s per month" % (
            len(men_high_salary_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

        labels = ["Men who earn High Salary", " Women who earn high salary"]
        data = [len(men_high_salary_results), len(women_high_salary_results)]
        colors = ['lightcoral', 'lightskyblue']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def get_high_salary_results_after_filtered(data_frame):
    high_salary_filter = (data_frame['ConvertedComp'] > Constants.HIGH_SALARY * Constants.NUM_OF_MONTH_IN_A_YEAR);
    high_salary_results = data_frame.loc[
        high_salary_filter, ['Respondent', 'Country', 'LanguageWorkedWith', 'ConvertedComp', 'Gender']]

    return high_salary_results


def print_data_on_participants_salaries_by_countries(data_frame, pandas_logger,
                                                     time_the_graph_will_be_displayed_in_seconds,
                                                     statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Participants month salary Median categorized by countries:"
    if should_be_displayed[title] == "yes":
        country_group = data_frame.groupby(["Country"])
        usa = "United States"
        india = "India"
        germany = "Germany"
        united_kingdom = "United Kingdom"
        spain = "Spain"
        italy = "Italy"
        israel = "Israel"

        usa_participants_month_salary_median = round(country_group.get_group(usa)["ConvertedComp"].median() / 12, 2)
        india_participants_month_salary_median = round(country_group.get_group(india)["ConvertedComp"].median() / 12, 2)
        germany_participants_month_salary_median = round(
            country_group.get_group(germany)["ConvertedComp"].median() / 12, 2)
        united_kingdom_participants_month_salary_median = round(country_group.get_group(united_kingdom)[
                                                                    "ConvertedComp"].median() / 12, 2)
        spain_participants_month_salary_median = round(country_group.get_group(spain)["ConvertedComp"].median() / 12, 2)
        italy_participants_month_salary_median = round(country_group.get_group(italy)["ConvertedComp"].median() / 12, 2)
        israel_participants_month_salary_median = round(country_group.get_group(israel)["ConvertedComp"].median() / 12,
                                                        2)

        pandas_logger.info("\n\n************* Participants month salary median by countries Data: *************\n ")
        pandas_logger.info(
            "\nAmericans month salary median is: %d.\nIndian month salary median is: %d.\nGermans month salary median is: %d."
            "\nBritish month salary median is: %d.\nSpanish month salary median is: %d.\nItalians month salary median is: %d.\nIsraelis month salary median is: %d.\n" % (
                usa_participants_month_salary_median, india_participants_month_salary_median,
                germany_participants_month_salary_median,
                united_kingdom_participants_month_salary_median, spain_participants_month_salary_median,
                italy_participants_month_salary_median, israel_participants_month_salary_median))

        pandas_logger.log("\n We can see from the results that Israel are in the second place! The salaries in "
                          "America are ten times bigger than the salaries in India.")

        labels = [usa, india, germany, united_kingdom, spain, italy, israel]
        data = [usa_participants_month_salary_median, india_participants_month_salary_median,
                germany_participants_month_salary_median,
                united_kingdom_participants_month_salary_median, spain_participants_month_salary_median,
                italy_participants_month_salary_median, israel_participants_month_salary_median]
        colors = ['red', 'lightgrey', 'yellow', 'blue', 'yellow', 'lightgreen', 'lightblue']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_programing_languages_high_salaries(pandas_logger, high_salary_results,
                                                     time_the_graph_will_be_displayed_in_seconds,
                                                     statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Participants who earn high salary claim they have knowledge in:"
    if should_be_displayed[title] == "yes":
        pandas_logger.info("\n\n************* Programming languages details: *************\n ")
        python_filter = high_salary_results["LanguageWorkedWith"].str.contains('Python', na=False)
        python_results = high_salary_results.loc[python_filter]
        pandas_logger.info("** %d From %d which earn more than %s per month know Python" % (
            len(python_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));
        java_filter = high_salary_results["LanguageWorkedWith"].str.contains('Java;', na=False)
        java_results = high_salary_results.loc[java_filter]
        pandas_logger.info("** %d From %d which earn more than %s per month know Java" % (
            len(java_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));
        javaScript_filter = high_salary_results["LanguageWorkedWith"].str.contains('JavaScript', na=False)
        javaScript_results = high_salary_results.loc[javaScript_filter]
        pandas_logger.info("** %d From %d which earn more than %s per month know JavaScript" % (
            len(javaScript_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

        scala_filter = high_salary_results["LanguageWorkedWith"].str.contains('Scala', na=False)
        scala_results = high_salary_results.loc[scala_filter]
        pandas_logger.info("** %d From %d which earn more than %s per month know Scala" % (
            len(scala_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

        c_sharp_filter = high_salary_results["LanguageWorkedWith"].str.contains('C#;', na=False)
        c_sharp_results = high_salary_results.loc[c_sharp_filter]
        pandas_logger.info("** %d From %d which earn more than %s per month know C#" % (
            len(c_sharp_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

        c_filter = high_salary_results["LanguageWorkedWith"].str.contains('C;', na=False)
        c_results = high_salary_results.loc[c_filter]
        pandas_logger.info("** %d From %d which earn more than %s per month know C" % (
            len(c_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

        labels = ["Python", "JavaScript", "Java", "Scala", "C#", "C++"]
        data = [len(python_results), len(java_results), len(javaScript_results), len(scala_results),
                len(c_sharp_results),
                len(c_results)]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', "gray", "lightblue"]
        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_israelis_known_languages(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                                           statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Israelis known Programming languages"
    if should_be_displayed[title] == "yes":
        israel_filter = data_frame["Country"] == "Israel"

        israeli_people_know_python = data_frame.loc[israel_filter]['LanguageWorkedWith'].str.contains("Python",
                                                                                                      na=False).sum()
        israeli_people_know_javascript = data_frame.loc[israel_filter]['LanguageWorkedWith'].str.contains("JavaScript",
                                                                                                          na=False).sum()
        israeli_people_know_java = data_frame.loc[israel_filter]['LanguageWorkedWith'].str.contains("Java;",
                                                                                                    na=False).sum()
        israeli_people_know_scala = data_frame.loc[israel_filter]['LanguageWorkedWith'].str.contains("Scala",
                                                                                                     na=False).sum()
        israeli_people_know_c_sharp = data_frame.loc[israel_filter]['LanguageWorkedWith'].str.contains("C#;",
                                                                                                       na=False).sum()
        israeli_people_know_c = data_frame.loc[israel_filter]['LanguageWorkedWith'].str.contains("C;", na=False).sum()
        pandas_logger.info("\n\n************* Israelis Programming languages known details: *************\n ")

        pandas_logger.info("%d From the Israelis participants know Python.\n"
                           "%d From the Israelis participants know JavaScript.\n %d From the Israelis participants know Java."
                           "\n%d From the Israelis participants know Scala."
                           "\n%d From the Israelis participants know C#."
                           "\n%d From the Israelis participants know C." % (
                               israeli_people_know_python, israeli_people_know_javascript, israeli_people_know_java,
                               israeli_people_know_scala, israeli_people_know_c_sharp, israeli_people_know_c));

        labels = ["Python", "JavaScript", "Java", "Scala", "C#", "C++"]
        data = [israeli_people_know_python, israeli_people_know_javascript, israeli_people_know_java,
                israeli_people_know_scala, israeli_people_know_c_sharp, israeli_people_know_c]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', "gray", "lightblue"]
        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_hobbies_and_salaries(data_frame, pandas_logger, time_the_graph_will_be_displayed_in_seconds,
                                       statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Month salary median -> Programming as a hobby"
    if should_be_displayed[title] == "yes":
        hobby_group = data_frame.groupby(["Hobbyist"])

        hobby_median_salary = round(hobby_group.get_group("Yes")["ConvertedComp"].median() / 12, 2)
        no_hobby_median_salary = round(hobby_group.get_group("No")["ConvertedComp"].median() / 12, 2)

        pandas_logger.info(
            "\n\n************* Month salary median categorized by -> is the participant code as a hobby? "
            "*************\n ")
        pandas_logger.info(
            "\nThe month salary median of the people who code as a hobby: %d \nThe month salary median of the people "
            "who don't code as a hobby: %d" % (
                hobby_median_salary, no_hobby_median_salary))

        pandas_logger.info("\n We can see that the participants who said they are programming as hobby, earn a little "
                          "bit more than the others.")

        labels = ["Yes", "No"]
        data = [hobby_median_salary, no_hobby_median_salary]
        colors = ['gold', 'lightcoral']

        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def print_data_on_women_men_salaries_by_countries(data_frame, pandas_logger,
                                                  time_the_graph_will_be_displayed_in_seconds,
                                                  statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Women V.S Men Median Salaries in USA and ISRAEL"
    if should_be_displayed[title] == "yes":
        country_group = data_frame.groupby(["Country"])
        usa = "United States"
        israel = "Israel"

    americans_men_median_salary = round(
        country_group.get_group(usa).groupby(["Gender"]).get_group("Man")["ConvertedComp"].median() / 12, 2)
    americans_women_median_salary = round(
        country_group.get_group(usa).groupby(["Gender"]).get_group("Woman")["ConvertedComp"].median() / 12, 2)

    israelis_men_median_salary = round(
        country_group.get_group(israel).groupby(["Gender"]).get_group("Man")["ConvertedComp"].median() / 12, 2)
    israelis_women_median_salary = round(
        country_group.get_group(israel).groupby(["Gender"]).get_group("Woman")["ConvertedComp"].median() / 12, 2)

    pandas_logger.info("\n\n************* Women V.S Men Median Salaries in USA and ISRAEL*************\n")
    pandas_logger.info(
        "\nAmericans men month salary median is: %d.\nAmericans women month salary median is: %d.\nIsraelis men month salary median is: %d.\nIsraelis women month salary median is: %d." % (
            americans_men_median_salary,americans_women_median_salary,israelis_men_median_salary,israelis_women_median_salary))

    labels = ["Americans Men", "Americans Women" , "Israelis Men", "Israelis Women"]
    data = [americans_men_median_salary,americans_women_median_salary,israelis_men_median_salary,israelis_women_median_salary]
    colors = ['blue', 'red', 'cyan', 'lightcoral']

    display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                          statistical_analysis_type_of_viewing)


def print_data_on_years_of_experience_and_salaries(data_frame, pandas_logger,
                                                   time_the_graph_will_be_displayed_in_seconds,
                                                   statistical_analysis_type_of_viewing, should_be_displayed):
    title = "Participants month salary Median categorized by years of experience:"
    if should_be_displayed[title] == "yes":
        years_of_experience_group = data_frame.groupby(["YearsCodePro"])
        one_year = round(years_of_experience_group.get_group("1")["ConvertedComp"].median() / 12, 2)
        three_years = round(years_of_experience_group.get_group("3")["ConvertedComp"].median() / 12, 2)
        four_years = round(years_of_experience_group.get_group("4")["ConvertedComp"].median() / 12, 2)
        six_years = round(years_of_experience_group.get_group("6")["ConvertedComp"].median() / 12, 2)
        fifteen_years = round(years_of_experience_group.get_group("15")["ConvertedComp"].median() / 12, 2)
        twenty_five_years = round(years_of_experience_group.get_group("25")["ConvertedComp"].median() / 12, 2)

        pandas_logger.info(
            "\n\n************* Participants month salary median by years of Experience: *************\n ")
        pandas_logger.info(
            "\nOne year experience participants month salary median is: %d.\nThree years experience participants month salary median is: %d.\nFour years experience participants month salary median is: %d."
            "\nSix years experience participants month salary median is: %d.\nFifteen years experience participants month salary median is: %d.\nTwenty five years experience participants month salary median is: %d." % (
                one_year, three_years, four_years, six_years, fifteen_years, twenty_five_years))

        pandas_logger.info("\n As expected, the amount of years experience affected directly on the Salary.")

        labels = ["1", "3", "4", "6", "15", "25"]
        data = [one_year, three_years,
                four_years,
                six_years, fifteen_years,
                twenty_five_years]
        colors = ['lightcoral', 'lightgrey', 'lightblue', 'blue', 'yellow', 'lightgreen']
        display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                              statistical_analysis_type_of_viewing)


def get_timer_plt_show_time_with_callback(time_the_graph_will_be_displayed_in_seconds):
    fig = plt.figure()
    timer = fig.canvas.new_timer(
        interval=time_the_graph_will_be_displayed_in_seconds * 1000)  # creating a timer object and setting an interval of time_the_graph_will_be_displayed_in_seconds seconds
    timer.add_callback(close_event)

    return timer


def display_data_visually(title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors,
                          statistical_analysis_type_of_viewing):
    timer = get_timer_plt_show_time_with_callback(time_the_graph_will_be_displayed_in_seconds);
    plt.title(title, fontdict=None, loc='center')

    try:
        diagram_or_pie = statistical_analysis_type_of_viewing[title];
    except:
        diagram_or_pie = "diagram"

    if (diagram_or_pie == "pie"):
        plt.pie(data, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
    else:
        for i in range(len(data)):
            plt.annotate(str(data[i]), xy=(labels[i], data[i]))

        plt.bar(labels, data, color=colors)

    timer.start()

    plt.show()


def close_event():
    plt.close()


def set_pd_options(pd):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    pd.set_option('display.expand_frame_repr', False)


def extract_log_file_name(pandas_logger):
    log_file_full_path = pandas_logger.handlers[0].baseFilename
    log_path_array = log_file_full_path.split("\\")
    return log_path_array[len(log_path_array) - 1]


def set_logger():
    logger = PandasLogger()
    return logger.create_pandas_logger(logger, "Pandas_Seminary.log")


def set_plt_size():
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size


if __name__ == '__main__':
    main()
