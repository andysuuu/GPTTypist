from uiautomator2 import Device
import subprocess
import os
import re
import platform
from exception.exit_app_exception import ExitAppException


class Task:
    def __init__(self):
        # basic variables
        self.app_name = Device().info['currentPackageName']
        self.activityLst = []
        self.visitedActivityLst = []
        self.system = platform.system() == 'Darwin'

    def get_app_tasks(self):
        current_app_name = Device().info['currentPackageName']
        if current_app_name != self.app_name:
            adb_command = f"adb shell monkey -p {self.app_name} -c android.intent.category.LAUNCHER 1"
            try:
                subprocess.run(adb_command, shell=True, check=True, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print(f"Cannot start {self.app_name}：{e}")
            raise ExitAppException

        if self.system:
            command = "grep"
        else:
            command = "findstr"
        current_focus_cmd = os.popen("adb shell dumpsys window displays").read()
        current_focus_activity = re.search(r'mCurrentFocus=Window{[^}]*\/(\S+)}', current_focus_cmd)
        previous_focus_cmd = os.popen("adb shell dumpsys activity activities | " + command + " ActivityRecord").read()
        previous_focus_activities = re.findall(rf"ActivityRecord{{[^}}]*{re.escape(self.app_name)}/([^\s]+)",
                                               previous_focus_cmd)
        previous_focus_activities = get_unique_activities(previous_focus_activities)

        if current_focus_activity:
            activities = self.get_activities(command)
            for activity in activities:
                if activity not in self.activityLst:
                    self.activityLst.append(activity)

            for previous_focus_activity in previous_focus_activities:
                if previous_focus_activity not in self.visitedActivityLst:
                    self.visitedActivityLst.append(previous_focus_activity)

            current_focus_activity_name = re.search(r'\.(\w+)$', current_focus_activity.group(1)).group(1)
            if current_focus_activity_name not in self.visitedActivityLst:
                self.visitedActivityLst.append(current_focus_activity_name)

    def get_activities(self, command):

        try:
            pattern = fr'{self.app_name}.*Activity'
            process_activity_cmd = subprocess.check_output(["adb", "shell", "dumpsys", "activity"]).decode('utf-8')
            adb_command = ["adb", "shell", "dumpsys", "package", self.app_name, "|", command, "-i", "activity"]
            package_activity_cmd = subprocess.check_output(adb_command, shell=True, stderr=subprocess.STDOUT, text=True)

            all_activities = re.findall(pattern, process_activity_cmd) + re.findall(pattern, package_activity_cmd)
            all_activities = get_unique_activities(all_activities)

            return all_activities
        except subprocess.CalledProcessError:
            return []


def get_unique_activities(activities: list):
    unique_activity_names = set()
    for activity_string in activities:
        match = re.search(r'[^/\.]+$', activity_string)
        if match:
            activity_name = match.group()
            unique_activity_names.add(activity_name)
    return list(unique_activity_names)
