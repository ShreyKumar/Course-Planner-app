# Assignment 2 - Course Planning!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# Shreyansh Kumar, kumarsh6
# Jingcheng Niu, niujingc
# Yiyang Liu, liuyiya4
# ---------------------------------------------
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import Course


def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.

    See assignment handout for details.
    """
    created_courses = {}
    with open(filename, 'r') as open_file:

        for line in open_file:
            line = line.strip()
            courses = line.split()
            if line != "" and len(courses) == 2:
                # If the course does not exist, create a new course
                if courses[1] not in created_courses:
                    # Create Course object and store in dictionary
                    created_courses[courses[1]] = Course(courses[1])
                if courses[0] not in created_courses:
                    created_courses[courses[0]] = Course(courses[0])

                # If courses[0] is not a prereq of courses[1], add courses[0]
                # as a prereq to courses[1]
                if not created_courses[courses[0]].\
                   is_prereq(created_courses[courses[1]]):
                    created_courses[courses[1]].\
                        add_prereq(created_courses[courses[0]])

    # Return the root course
    return get_root_course(created_courses)


def get_root_course(created_courses):
    """(dict) -> Course

    Return the course which is not prerequisite for any other courses to be
    the root
    """
    for course_name in created_courses:
        course_is_req = False
        for other_course_name in created_courses:
            # Search through every course
            if course_name != other_course_name:
                # Get the other course from created_coruses
                other_course = created_courses[other_course_name]
                if created_courses[course_name].is_prereq(other_course):
                    # If course is prereq of any other course
                    course_is_req = True
                    break
        if not course_is_req:
            return created_courses[course_name]
    # return an empty course when the file is blank and no courses are created
    return Course(None)


class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.

        You may not change this method in any way!
        """
        self.course = parse_course_data(filename)

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        for course_list in schedule:

            # Check if there is duplicated courses
            if not self.check_no_duplicate(self.all_courses(schedule)):
                return False
            for course in course_list:
                # Checks if:
                # Every course in the schedule exists in the Course tree.
                # Every course is taken after all of its prerequisite
                # courses have been taken.
                if course not in self.course\
                   or not self.course.get_course(course).is_takeable():
                    self.course.reset_course()
                    return False
            self.course.set_courses_taken(course_list)

        # Reset everything to default
        self.course.reset_course()
        return True

    def all_courses(self, schedule):
        """
        (TermPlanner, list of (list of str)) -> list of str
        Add all courses in schedule to all_courses, converting nested_list
        into list
        """
        all_courses = []

        for course_list in schedule:
            # Add all the course in each nested list into the all_courses list
            # for checking duplicate courses.
            all_courses += course_list

        return all_courses

    def check_no_duplicate(self, selected_courses):
        """(TermPlanner, list of str) -> boolean
        Return True if there are no duplicate courses.
        """
        copy = list(selected_courses)
        # get rid of duplicates
        copy = list(set(copy))
        # if copy is same as original, means no duplicate courses
        return len(copy) == len(selected_courses)

# -------------------------------------------------------------
    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.
        """
        schedule = []

        if self.selected_courses_are_valid(selected_courses):

            while len(selected_courses) > 0:

                # get all takable courses
                takeable_courses = self.get_takeable_courses(selected_courses)
                takeable_courses.sort()

                # append 5 takeable courses to schedule, since limit is 5
                schedule.append(takeable_courses[:5])
                self.course.set_courses_taken(takeable_courses[:5])
                for course in takeable_courses[:5]:
                    selected_courses.remove(course)

        # reset all courses to make sure no error
        self.course.reset_course()
        return schedule

    def selected_courses_are_valid(self, s_courses):
        """(TermPlanner, list of str) -> boolean
        Return True if all the courses selected are vaild.
        Courses are valid if:
        1) They all exist in the course tree.
        2) Their prerequisites exists in the selected courses list.
        3) If there are no duplicate in selected courses list.
        """
        if self.all_exist(s_courses) and self.prereqs_exist(s_courses)\
           and self.check_no_duplicate(s_courses):
            return True
        return False

    def all_exist(self, s_courses):
        """(TermPlanner, list of str) -> boolean
        Return True if all the courses selected exist in the course tree.
        """
        for course in s_courses:
            if course not in self.course:
                return False
        return True

    def prereqs_exist(self, s_courses):
        """(TermPlanner, list of str) -> boolean
        Return True if all the courses selected have prereqs also selected.
        """
        for course in s_courses:
            # get course's missing prereqs
            course_prereqs = self.course.get_course(course).missing_prereqs()
            for prereq in course_prereqs:
                # if some untaken prereq is not in selected courses
                if prereq not in s_courses:
                    return False
        return True

    def get_takeable_courses(self, selected_courses):
        """
        (TermPlanner, list of str) -> list of str
        Return a list of all takable courses if requirements are passed
        """
        takeable_courses = []
        for course in selected_courses:
            if self.course.get_course(course).is_takeable():
                # If course is takeable, append to takeable_courses
                takeable_courses.append(course)
        # finally return
        return takeable_courses
