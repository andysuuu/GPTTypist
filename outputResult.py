import platform
import task


class OutputResult:
    def __init__(self):
        # basic variables
        self.file = None
        self.path = None

    def init_configuration(self, language_selection, app_name):
        os_version = platform.system()
        if os_version == 'Darwin':
            output_directory = r"/Users/andysu/Documents/Monash/FIT4701/text_files"
        else:
            output_directory = r"C:\Users\13261\Desktop\Y4S1\FIT4702\Result"

        # app_name = task.get_current_app_package()
        file_name = "\\" + app_name + ".txt"
        full_path = output_directory + file_name
        self.path = full_path

        # Write the basic information
        self.file = open(self.path, "a")
        self.file.write("This is the result file of the application " + app_name + "\n")
        self.file.write("Current mode is in ")
        if language_selection == '1':
            self.file.write("English")
        else:
            self.file.write("Chinese")

        self.file.write(
            "\n#############################################\n#############################################\n\n\n\n")
        self.file.close()

    def write_info(self, iteration_count, activityLst, visitedActivityLst):
        # Open the output file
        self.file = open(self.path, "a")
        self.file.write("Iteration: " + str(iteration_count) + "\n")
        iteration_count += 1

        self.file.write("All activities count: " + str(len(activityLst)) + "\n")
        self.file.write("All activities: \n")
        self.file.write(str(activityLst) + "\n###################################\n")

        self.file.write("All visited activities count: " + str(len(visitedActivityLst)) + "\n")
        self.file.write("Visited activities: \n")
        self.file.write(str(visitedActivityLst) + "\n###################################\n")

        cover_count = 0
        for v in range(len(visitedActivityLst)):
            for a in range(len(activityLst)):
                if visitedActivityLst[v] in activityLst[a]:
                    cover_count += 1
                    break

        self.file.write("Cover rate of activities: " + str(cover_count / len(activityLst)) + "\n\n\n\n\n\n\n")

        self.file.close()

    def summary_info(self, history):
        self.file = open(self.path, "a")

        self.file.write("\n###################################")
        self.file.write("\n###################################")
        self.file.write("\n###################################\n")
        self.file.write("Summary:\n")
        self.file.write("Total page changed: " + str(len(history.pages)) + "\n")
        self.file.write("Total operated components: " + str(len(history.operated_components)) + "\n")
        self.file.write("\n\n\n\n\n\n\n\n")

        self.file.close()
