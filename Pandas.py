'''
@authors: Sagiv Asraf 312527450
          Liran Katz  204483226
        Project Pandas Show and Analyzing Data Usin Pandas
---------------------------------------------------------
We downloaded the data from here: https://drive.google.com/file/d/1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV/view
This is the famous Stack Overflow Annual Developer Survey of 2019.

We built a project that represent a pert managment system.
The pert itself is represent in Pert_Graph class, that is implement dictionary.

  Pert_Graph Class has a dictionary attribute, that has keys and values per key.

        Key -> an activity (implement by activity class)
        Value -> a list of activities

  Pert_Graph Class has an attribute that represent project duration

  Activity Class has a name and duration attributes that represent an activity.
    *Name - name of the activity
    *Duration - the time that take to the activity to finish
  The graph include nodes that represent as activity.
  For your convenience we added a main function that check every function that we wrote for solving the exercise.

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
from Utils.EmailManagement import EmailManagement
from Utils.PandasLogger import PandasLogger
from tabulate import tabulate


def main():
    set_pd_options(pd)
    pandas_logger = set_logger()
    pandas_logger.info('Start collecting data for seminary project\n')

    data_frame = pd.read_csv('Survey Data Files/survey_results_public.csv')
    schema_data_frame = pd.read_csv("Survey Data Files/survey_results_schema.csv")
    pandas_logger.info('Some basic details (META-DATA) on our data:')

    shape = data_frame.shape;
    rows = shape[0]
    cols = shape[1]

    pandas_logger.info("We have %d rows and %d columns of data in our survey" % (rows, cols))
    pandas_logger.info("We asked our participants the following questions: \n %s",
                       tabulate(schema_data_frame, headers='keys', tablefmt='psql'))


    israel_filter = (data_frame['Country'] == "Israel");
    israel_participants = data_frame.loc[israel_filter, ['Country','Gender','Student', 'LanguageWorkedWith', 'ConvertedComp']]
    pandas_logger.info("\n\n************* Israelis participants: *************\n ")
    pandas_logger.info("Due to the fact we have %d Israelis participants we will display the first 100" % (len(israel_participants)))
    pandas_logger.info(tabulate(israel_participants.head(100), headers='keys', tablefmt='psql'))
    pandas_logger.info("\n***************************** %d From %d of our participants are Israelis! Respect *****************************\n" % (len(israel_participants), rows));

    pandas_logger.info("\nThe following table contains people who makes more than 10,000$ per month -> focused on "
                       "Country, the programming language they worked with and of course the yearly salary\n")

    #Sort our data_frame by salaries!
    data_frame.sort_values(by='ConvertedComp',inplace=True, ascending=False)
    high_salary_filter = (data_frame['ConvertedComp'] > 10000 * 12);
    high_salary_results = data_frame.loc[high_salary_filter, ['Country', 'LanguageWorkedWith', 'ConvertedComp','Gender']]

    pandas_logger.info(
        "Due to the fact we have %d participants that earn more than 10,000$ per month, We will display just the TOP 100 (sorted by salaries!)" % (
            len(high_salary_results)))

    pandas_logger.info(tabulate(high_salary_results.head(100), headers='keys', tablefmt='psql'))

    pandas_logger.info("lets Analyze this data")
    pandas_logger.info(
        "%d From %d of our participants, earn more than 10,000$ per month" % (len(high_salary_results), rows));

    pandas_logger.info("In percentage: %d%% from our participants earn more than 10,000$ per month" % (
            (len(high_salary_results) * 100) / rows));

    pandas_logger.info("\n\n************* Israelis High salary participants: *************\n ")
    israel_high_salary_filter = high_salary_results["Country"].eq("Israel");
    israel_high_salary_results = high_salary_results.loc[israel_high_salary_filter]
    pandas_logger.info(tabulate(israel_high_salary_results, headers='keys', tablefmt='psql'))
    pandas_logger.info("\n%d From %d of our participants, which earn more than 10,000$ per month are Israelis" % (len(israel_high_salary_results), len(high_salary_results)));

    pandas_logger.info("\n\n************* Women VS Men High salary participants: *************\n ")
    women_high_salary_filter = high_salary_results["Gender"].eq("Woman");
    men_high_salary_filter = high_salary_results["Gender"].eq("Man");

    women_high_salary_results = high_salary_results.loc[women_high_salary_filter]
    men_high_salary_results = high_salary_results.loc[men_high_salary_filter]

    pandas_logger.info("%d From %d are women which earn more than 10,00$ per month" %(len(women_high_salary_results), len(high_salary_results)));
    pandas_logger.info("%d From %d are men which earn more than 10,00$ per month" %(len(men_high_salary_results), len(high_salary_results)));

    pandas_logger.info("\n\n************* Programming languages details: *************\n ")
    python_filter = high_salary_results["LanguageWorkedWith"].str.contains('Python', na=False)
    python_results = high_salary_results.loc[python_filter]
    pandas_logger.info("** %d From %d which earn more than 10,00$ per month know Python" % (len(python_results),len(high_salary_results)));
    java_filter = high_salary_results["LanguageWorkedWith"].str.contains('Java;', na=False)
    java_results = high_salary_results.loc[java_filter]
    pandas_logger.info("** %d From %d which earn more than 10,00$ per month know Java" % (len(java_results),len(high_salary_results)));
    javaScript_filter = high_salary_results["LanguageWorkedWith"].str.contains('JavaScript', na=False)
    javaScript_results = high_salary_results.loc[javaScript_filter]
    pandas_logger.info("** %d From %d which earn more than 10,00$ per month know JavaScript" % (len(javaScript_results),len(high_salary_results)));

    scala_filter = high_salary_results["LanguageWorkedWith"].str.contains('Scala', na=False)
    scala_results = high_salary_results.loc[scala_filter]
    pandas_logger.info("** %d From %d which earn more than 10,00$ per month know Scala" % (
    len(scala_results), len(high_salary_results)));

    # pandas_logger.info("%d From %d", len(high_salary_results), rows);

    # ************* Send the log file to my mail *************

    # seminar_mail = "pandasseminar@gmail.com"
    # seminar_password = "pandasseminarpython"
    # receiver_mail = "sagivasraf23@gmail.com"
    #
    # log_file_name = extract_log_file_name(pandas_logger)
    #
    # EmailManagement.send_email(seminar_mail, seminar_password, receiver_mail, log_file_name)

    print("Finished, you can now watch your results in the log file ! :)")


def set_pd_options(pd):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', None)


def extract_log_file_name(pandas_logger):
    log_file_full_path = pandas_logger.handlers[0].baseFilename
    log_path_array = log_file_full_path.split("\\")
    return log_path_array[len(log_path_array) - 1]


def set_logger():
    logger = PandasLogger()
    return logger.create_pandas_logger(logger, "Pandas_Seminary.log")


if __name__ == '__main__':
    main()
