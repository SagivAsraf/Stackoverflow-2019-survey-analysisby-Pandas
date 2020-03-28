'''
@authors: Sagiv Asraf 312527450
          Liran Katz  204483226
        Project Pandas Show and Analyzing Data Usin Pandas
---------------------------------------------------------
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
from Utils.PandasLogger import PandasLogger


def main():
    pandas_logger = set_logger()

    pandas_logger.info('Start collecting data for seminary project\n')

    data_frame = pd.read_csv('Survey Data Files/survey_results_public.csv')
    schema_data_frame = pd.read_csv("Survey Data Files/survey_results_schema.csv")
    pandas_logger.info('Some basic details (META-DATA) on our data:')

    shape = data_frame.shape;
    rows = shape[0]
    cols = shape[1]

    pandas_logger.info("We have %d rows and %d columns of data in our survey" % (rows, cols))
    # We want to print all the columns (questions) of the survey!
    pd.set_option("display.max_rows", cols);
    pandas_logger.info("We asked our participants the following questions: \n %s" , schema_data_frame)


def set_logger():
    logger = PandasLogger()
    return logger.create_pandas_logger(logger, "Pandas_Seminary.log")

if __name__ == '__main__':
    main()
