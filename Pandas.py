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


def main():
    plt.close('all')
    set_pd_options(pd)
    pandas_logger = set_logger()
    pandas_logger.info('Start collecting data for seminary project\n')

    data_frame = pd.read_csv('Survey Data Files/survey_results_public.csv')
    schema_data_frame = pd.read_csv("Survey Data Files/survey_results_schema.csv")
    pandas_logger.info('Some basic details (META-DATA) on our data:')

    shape = data_frame.shape;
    rows = shape[0]
    cols = shape[1]

    time_the_graph_will_be_displayed_in_seconds = 2;

    print_some_meta_data_on_the_data(schema_data_frame, pandas_logger, rows, cols)

    print_data_on_israelis(data_frame, pandas_logger, plt, rows, time_the_graph_will_be_displayed_in_seconds)

    high_salary_results = get_high_salary_results_after_filtered(data_frame)

    print_data_on_participants_high_salary(data_frame, pandas_logger, rows, high_salary_results,
                                           time_the_graph_will_be_displayed_in_seconds)

    print_data_on_israelis_whos_have_high_salary(pandas_logger, high_salary_results,
                                                 time_the_graph_will_be_displayed_in_seconds)

    print_data_on_man_vs_women_salaries(pandas_logger, high_salary_results, time_the_graph_will_be_displayed_in_seconds)

    print_data_on_programing_languages_high_salaries(pandas_logger, high_salary_results,
                                                     time_the_graph_will_be_displayed_in_seconds)

    # pandas_logger.info("%d From %d", len(high_salary_results), rows);

    # ************* Send the log file to my mail *************
    send_log_file_in_mail("sagivasraf23@gmail.com", pandas_logger)

    print("Finished, you can now watch your results in the log file ! :)")


def send_log_file_in_mail(receiver_mail, pandas_logger):
    seminar_mail = "pandasseminar@gmail.com"
    seminar_password = "pandasseminarpython"

    log_file_name = extract_log_file_name(pandas_logger)

    EmailManagement.send_email(seminar_mail, seminar_password, receiver_mail, log_file_name)


def print_some_meta_data_on_the_data(schema_data_frame, pandas_logger, rows, cols):
    pandas_logger.info("We have %d rows and %d columns of data in our survey" % (rows, cols))
    pandas_logger.info("We asked our participants the following questions: \n %s",
                       tabulate(schema_data_frame, headers='keys', tablefmt='psql'))


def print_data_on_israelis(data_frame, pandas_logger, plt, rows, time_the_graph_will_be_displayed_in_seconds):
    israel_filter = (data_frame['Country'] == "Israel");
    israel_participants = data_frame.loc[
        israel_filter, ['Country', 'Gender', 'Student', 'LanguageWorkedWith', 'ConvertedComp']]
    pandas_logger.info("\n\n************* Israelis participants: *************\n ")
    pandas_logger.info(
        "Due to the fact we have %d Israelis participants we will display the first 100" % (len(israel_participants)))
    pandas_logger.info(tabulate(israel_participants.head(100), headers='keys', tablefmt='psql'))
    pandas_logger.info(
        "\n***************************** %d From %d of our participants are Israelis! Respect *****************************\n" % (
            len(israel_participants), rows));

    title = "Israelis Participants V.S All other participants"
    labels = ["Israelis Participant", "All other participants"]
    data = [len(israel_participants), rows - len(israel_participants)]
    colors = ['lightskyblue','gold']

    display_data_visually(plt, title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors)


def print_data_on_participants_high_salary(data_frame, pandas_logger, rows, high_salary_results,
                                           time_the_graph_will_be_displayed_in_seconds):
    pandas_logger.info("\nThe following table contains people who makes more than %s per month -> focused on "
                       "Country, the programming language they worked with and of course the yearly salary\n",
                       Constants.HIGH_SALARY_STRING)

    # Sort our data_frame by salaries!
    data_frame.sort_values(by='ConvertedComp', inplace=True, ascending=False)

    pandas_logger.info(
        "Due to the fact we have %d participants that earn more than %s per month, We will display just the TOP 100 (sorted by salaries!)" % (
            len(high_salary_results), Constants.HIGH_SALARY_STRING))

    pandas_logger.info(tabulate(high_salary_results.head(100), headers='keys', tablefmt='psql'))

    pandas_logger.info("lets Analyze this data")
    pandas_logger.info(
        "%d From %d of our participants, earn more than %s per month" % (
            len(high_salary_results), rows, Constants.HIGH_SALARY_STRING));

    pandas_logger.info("In percentage: %d%% from our participants earn more than %s per month" % (
        (len(high_salary_results) * 100) / rows, Constants.HIGH_SALARY_STRING));

    title = "Participants who earn more than " + Constants.HIGH_SALARY_STRING + "per month V.S Other participants"
    labels = ["Earn more than " + Constants.HIGH_SALARY_STRING + " Participants", "All other participants"]
    data = [len(high_salary_results), rows - len(high_salary_results)]
    colors = ['yellowgreen', 'lightcoral']
    display_data_visually(plt, title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors)


def get_high_salary_results_after_filtered(data_frame):
    high_salary_filter = (data_frame['ConvertedComp'] > Constants.HIGH_SALARY * Constants.NUM_OF_MONTH_IN_A_YEAR);
    high_salary_results = data_frame.loc[
        high_salary_filter, ['Country', 'LanguageWorkedWith', 'ConvertedComp', 'Gender']]

    return high_salary_results


def print_data_on_israelis_whos_have_high_salary(pandas_logger, high_salary_results,
                                                 time_the_graph_will_be_displayed_in_seconds):
    pandas_logger.info("\n\n************* Israelis High salary participants: *************\n ")
    israel_high_salary_filter = high_salary_results["Country"].eq("Israel");
    israel_high_salary_results = high_salary_results.loc[israel_high_salary_filter]
    pandas_logger.info(tabulate(israel_high_salary_results, headers='keys', tablefmt='psql'))
    pandas_logger.info("\n%d From %d of our participants, which earn more than %s per month are Israelis" % (
        len(israel_high_salary_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

    title = "Israelis who earn High Salary V.S All other participants who earn high salary"
    labels = ["Israelis who earn High Salary", "All other participants who earn high salary"]
    data = [len(israel_high_salary_results), len(high_salary_results) - len(israel_high_salary_results)]
    colors = ['lightskyblue', 'yellowgreen']
    display_data_visually(plt, title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors)


def print_data_on_man_vs_women_salaries(pandas_logger, high_salary_results,
                                        time_the_graph_will_be_displayed_in_seconds):
    pandas_logger.info("\n\n************* Women VS Men High salary participants: *************\n ")
    women_high_salary_filter = high_salary_results["Gender"].eq("Woman");
    men_high_salary_filter = high_salary_results["Gender"].eq("Man");

    women_high_salary_results = high_salary_results.loc[women_high_salary_filter]
    men_high_salary_results = high_salary_results.loc[men_high_salary_filter]

    pandas_logger.info("%d From %d are women which earn more than %s per month" % (
        len(women_high_salary_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));
    pandas_logger.info("%d From %d are men which earn more than %s per month" % (
        len(men_high_salary_results), len(high_salary_results), Constants.HIGH_SALARY_STRING));

    title = "Men who earn High Salary V.S Women who earn high salary"
    labels = ["Men who earn High Salary", " Women who earn high salary"]
    data = [len(men_high_salary_results), len(women_high_salary_results)]
    colors = ['lightcoral', 'lightskyblue']

    display_data_visually(plt, title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors)


def print_data_on_programing_languages_high_salaries(pandas_logger, high_salary_results,
                                                     time_the_graph_will_be_displayed_in_seconds):
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

    title = "Participants who earn high salary claim they have knowledge in:"
    labels = ["Python", "Java", "JavaScript", "Scala"]
    data = [len(python_results), len(java_results), len(javaScript_results), len(scala_results)]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    display_data_visually(plt, title, labels, data, time_the_graph_will_be_displayed_in_seconds * 2, colors)


def get_timer_plt_show_time_with_callback(plt, time_the_graph_will_be_displayed_in_seconds):
    fig = plt.figure()
    timer = fig.canvas.new_timer(
        interval=time_the_graph_will_be_displayed_in_seconds * 1000)  # creating a timer object and setting an interval of time_the_graph_will_be_displayed_in_seconds seconds
    timer.add_callback(close_event)

    return timer


def display_data_visually(plt, title, labels, data, time_the_graph_will_be_displayed_in_seconds, colors):
    timer = get_timer_plt_show_time_with_callback(plt, time_the_graph_will_be_displayed_in_seconds);
    plt.title(title, fontdict=None, loc='center')
    #plt.bar(labels, data, color=colors)

    plt.pie(data, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')

    # fig_size = plt.rcParams["figure.figsize"]
    # fig_size[0] = 15
    # fig_size[1] = 12
    # plt.rcParams["figure.figsize"] = fig_size

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

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


if __name__ == '__main__':
    main()
