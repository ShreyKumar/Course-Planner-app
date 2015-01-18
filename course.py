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
"""Course prerequisite data structure.

This module contains the class that should store all of the
data about course prerequisites and track taken courses.
Note that by tracking "taken" courses, we are restricting the use
of this class to be one instance per student (otherwise,
"taken" doesn't make sense).

Course: a course and its prerequisites.
"""


class Course:
    """A tree representing a course and its prerequisites.

    This class not only tracks the underlying prerequisite relationships,
    but also can change over time by allowing courses to be "taken".

    Attributes:
    - name (str): the name of the course
    - prereqs (list of Course): a list of the course's prerequisites
    - taken (bool): represents whether the course has been taken or not
    """

    # Core Methods - implement all of these
    def __init__(self, name, prereqs=None):
        """ (Course, str, list of Courses) -> NoneType

        Create a new course with given name and prerequisites.
        By default, the course has no prerequisites (represent this
        with an empty list, NOT None).
        The newly created course is not taken.
        """
        # Create an attribute self.name and assign it to the parameter
        self.name = name
        if prereqs is None:
            # Create an list attribute self.prereqs if and only if there are
            # no prereqistes passed in
            self.prereqs = []
        else:
            # If there are prerequisites, initialise self.prereqs
            self.prereqs = prereqs
        # Originally set the course to untaken by creating an attribute
        # self.taken
        self.taken = False

    def __contains__(self, item):
        """(Course, str) -> boolean

        Return if a course name is in the course tree
        """
        if self.name == item:
            return True
        else:
            for course in self.prereqs:
                # If the item is found inside the prerequistes tree
                if item in course:
                    return True
            return False

    def is_takeable(self):
        """ (Course) -> bool

        Return True if the user can take this course.
        A course is takeable if and only if all of its prerequisites are taken.
        """
        # Go through all the prerequisites
        for course in self.prereqs:
            # if there exists a course inside the prerequiste tree that is
            # untaken return False
            if course.taken is False:
                return False
        # If no such course is found, return true.
        return True

    def take(self):
        """ (Course) -> NoneType

        If this course is takeable, change self.taken to True.
        Do nothing if self.taken is already True.
        Raise UntakeableError if this course is not takeable.
        """
        # if the course is takable, change the self.taken attribute to True
        if self.is_takeable():
            self.taken = True
        else:
            # Raise UntakeableError if the course is not takable
            raise UntakeableError

    def add_prereq(self, prereq):
        """ (Course, Course) -> NoneType

        Add a prereq as a new prerequisite for this course.

        Raise PrerequisiteError if either:
        - prereq has this course in its prerequisite tree, or
        - this course already has prereq in its prerequisite tree
        """
        if self == prereq:
            raise PrerequisiteError
        if prereq.is_prereq(self):
            # if the prerequiste is inside the prereqs list
            raise PrerequisiteError
        if self.is_prereq(prereq):
            # if the course is already in prerequiste tree
            raise PrerequisiteError

        # if no such error is raised, add prereq in the list self.prereqs
        self.prereqs.append(prereq)

    def is_prereq(self, my_course):
        """(Course, Course) -> boolean

        Return True if the course is inside the prerequisite tree of my_course
        """
        # if prerequsite tree of my_course is empty, then the my_course is
        # no a prerequiste of self
        if my_course.prereqs == []:
            return False
        else:
            # Recursive step: Go through all courses in my_course.prereqs
            for course in my_course.prereqs:
                if course.name == self.name:
                    # if course is found
                    return True
                if self.is_prereq(course):
                    # check if self is inside the prereq tree of my_course
                    return True
            # else nothing is found, return false
            return False

    def missing_prereqs(self):
        """ (Course) -> list of str

        Return a list of all of the names of the prerequisites of this course
        that are not taken.

        The returned list should be in alphabetical order, and should be
        empty if this course is not missing any prerequisites.
        """
        # prereqs is empty, return an empty list
        if self.prereqs == []:
            return []
        else:
            # create an empty list of miss_p
            miss_p = []
            for course in self.prereqs:
                # if course is not taken, then add that course to miss_p
                if not course.taken:
                    miss_p = miss_p + [course.name]
                # Recursive step: do the same by going through every other
                # course in self.prereqs
                miss_p = miss_p + course.missing_prereqs()

            # finally, sort and return miss_p
            miss_p.sort()
            return miss_p

    def get_course(self, name):
        """(Course, str) -> Course

        Return the first course with the name given.
        """
        # Base case: Check to see if the course itself matches the name
        if self.name == name:
            return self

        else:
            # Recursive step:
            for course in self.prereqs:
                # check all prereqs to see if match name
                if course.get_course(name):
                    return course.get_course(name)

    def set_courses_taken(self, course_list):
        """(Course, list of str) -> NoneType

        Take all the course in the course_list given
        """
        for course in course_list:
            self.get_course(course).take()

    def reset_course(self):
        """(Course) -> NoneType

        Reset the course, make every prereq in the course tree untaken.
        """
        # Base case: set the first course's taken attribute to False
        self.taken = False
        # Recursive step: call the same function and set all the prereqisites
        # to untaken
        for course in self.prereqs:
            course.reset_course()


class UntakeableError(Exception):
    pass


class PrerequisiteError(Exception):
    pass
