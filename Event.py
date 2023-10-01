import re
import string

DESCRIPTION_PATTERN = re.compile(r"DESCRIPTION:(.*)TRANSP:OPAQUE", re.DOTALL)
SUMMARY_PATTERN = re.compile(r"SUMMARY:(.*)LOCATION", re.DOTALL)

class Event:
    def __init__(self, event):
        self.event = event
        self.fixedEvent = event

    def fix(self):
        self.fix_description()
        self.fix_location()

    def fix_description(self):
        description = DESCRIPTION_PATTERN.search(self.event).group(1)
        newDescription = description.replace("\r\n ", "")
        newDescription = newDescription.replace(r"\n\n", r"\n\n ")

        elements = newDescription.split(r"\n\n")

        for element in elements:
            if "Activity" in element:
                activity = element.split(":")[1].strip()
                self.fix_summary(activity)

        #manual changes
        newDescription = newDescription.replace("Activity description", "Activity")
        newDescription = newDescription.replace("Location(s)", "Location")
        newDescription = newDescription.replace("Staff member(s)", "Staff")
        newDescription = newDescription.replace("Student group(s)", "Student")
        newDescription = newDescription.replace(r"This appointment is managed by MyTimetable.\n\n", "")

        #replace the old description with the new one
        self.fixedEvent = self.fixedEvent.replace(description, newDescription)

    def fix_summary(self, activity):
        summary = SUMMARY_PATTERN.search(self.event).group(1)
        newSummary = activity

        #Current summary is all caps, so we need to make it title case
        newSummary = string.capwords(newSummary) + '\n\n'

        self.fixedEvent = self.fixedEvent.replace(summary, newSummary)

    def fix_location(self):
        return