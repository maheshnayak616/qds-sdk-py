"""
This is a sample code used for submitting a Spark Python/R/Scala command and getting the result.
"""

from qds_sdk.qubole import Qubole
from qds_sdk.commands import SparkCommand
import time


def get_results_filename(command_id):
    """
    A helper method to generate a file name to write the downloaded result
    :param command_id:
    :return:
    """
    return "/tmp/result_{}.tsv".format(command_id)


def execute_script(cluster_label, cmd_to_run, language, user_program_arguments=None, arguments=None):
    """
    Helper method to execute a script
    :param cluster_label:
    :param cmd_to_run:
    :param language:
    :param user_program_arguments:
    :param arguments:
    :return:
    """
    if script is None or script == "":
        print("script cannot be None or empty")
        return None

    if not language:
        print("language cannot be None or empty")
        return

    # A python, R or scala command needs to be invoked in this fashion.
    cmd = SparkCommand.create(label=cluster_label, program=cmd_to_run, language=language, arguments=arguments,
                              user_program_arguments=user_program_arguments)

    while not SparkCommand.is_done(cmd.status):
        print("Waiting for completion of command : {}".format(cmd.id))
        cmd = SparkCommand.find(cmd.id)
        time.sleep(5)

    if SparkCommand.is_success(cmd.status):
        print("\nCommand Executed: Completed successfully")
    else:
        print("\nCommand Executed: Failed!!!. The status returned is: {}".format(cmd.status))
        print(cmd.get_log())
    return cmd


def get_results(command):
    """
    A helper method to get the results
    :param command:
    :return:
    """
    if command is None:
        return None

    results_file_name = get_results_filename(command.id)
    fp = open(results_file_name, 'w')

    command.get_results(fp, delim="\n")
    print("results are written to {}".format(results_file_name))


if __name__ == '__main__':
    # Set the API token. If you are using any other environment other then api.qubole.com then set api_url to that url
    # as <env_url>/api
    Qubole.configure(api_token='<api_token>')

    script_language = "scala"  # Script language.. Python, R or scala
    user_program_arguments = None  # arguments for your script
    arguments = None  # spark configuration for your program for ex : "--conf spark.executor.memory=1024M"
    cluster_label = "<your cluster label>"  # the cluster on which the command will run

    # Running a python command. In case of scala or R get the script content and then set the langauage field to scala
    # or R as required
    script = """
            import org.apache.spark.sql.SparkSession
            
            object TestMergeBucketIdScenarios {
              def main(args: Array[String]): Unit = {
                val spark = SparkSession.builder().appName("Spark Example").getOrCreate()
                val sampleData = Seq(("John" ,19), ("Smith", 29),("Adam", 35),("Henry", 50))
            
                import spark.implicits._
                val dataFrame = sampleData.toDF("name", "age")
                val output = dataFrame.select("name").where("age < 30").collect
                output.foreach(println)
              }
            }"""
    command = execute_script(cluster_label, script, script_language, user_program_arguments=user_program_arguments,
                             arguments=arguments)
    get_results(command)