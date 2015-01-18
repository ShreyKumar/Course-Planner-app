# Assignment 2 - Unit Tests for Course
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
"""Unit tests for course.py

Submit this file, containing *thorough* unit tests
for your code in course.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from course import (Course, UntakeableError,
                    PrerequisiteError)


class TestCourseConstructor(unittest.TestCase):
    """
    Set of test cases to test whether the constructor for Course works
    """
    def setUp(self):
        """
        Create two courses and make course1 a prereq of course2
        """
        self.course1 = Course("AAA111")
        self.course2 = Course("BBB222", [self.course1])

    def tearDown(self):
        """
        Reset everything
        """
        self.course1 = None
        self.course2 = None

    def test_create_course_name(self):
        """
        Check if course name is satisfied when course1 is created
        """
        self.assertEqual(self.course1.name, "AAA111")

    def test_create_course_no_prereqs(self):
        """
        Check if there are intitially no prereqs of course1
        """
        self.assertEqual(self.course1.prereqs, [])

    def test_create_course_not_taken(self):
        """
        Check if course taken is initially False
        """
        self.assertFalse(self.course1.taken)

    def test_create_course_with_prereq(self):
        """
        Check if course1 is correctly assigned as prereq of course2
        """
        self.assertEqual(self.course2.prereqs, [self.course1])


class TestCourseIsTakeable(unittest.TestCase):

    def setUp(self):
        """
        Create 2 courses, create a third course with one prereq and a fourth
        course with two prereqs
        """
        self.course1 = Course("AAA111")
        self.course2 = Course("BBB222")
        self.course_one_prereq = Course("One", [self.course1])
        self.course_two_prereq = Course("Two", [self.course1, self.course2])

    def tearDown(self):
        """
        Reset all course variables
        """
        self.course1 = None
        self.course2 = None
        self.course3 = None
        self.course_one_prereq = None
        self.course_two_prereq = None

    def test_is_takeable_leaf(self):
        """
        Check if course is takable, expect true since course1 is prereq of
        course2
        """
        self.assertTrue(self.course1.is_takeable())

    def test_is_takeable_leaf_taken(self):
        """
        Check if course is takable, even if the course is already taken
        """
        self.course1.taken = True
        self.assertTrue(self.course1.is_takeable())

    def test_is_takeable_one_prereq_no(self):
        """
        Check if course_one_prereq is takable if course.taken is set to False
        """
        self.assertFalse(self.course_one_prereq.is_takeable())

    def test_is_takeable_one_prereq_yes(self):
        """
        Set 1 course to taken, then check if only 1 course is takeable
        """
        self.course1.taken = True
        self.assertTrue(self.course_one_prereq.is_takeable())

    def test_is_takeable_two_prereq_one_no(self):
        """
        Check if two prereqs are taken.
        """
        self.course1.taken = True
        self.assertFalse(self.course_two_prereq.is_takeable())

    def test_is_takeable_two_prereq_yes(self):
        """
        Checks if course with two prereq is taken if both both prereqs are
        taken
        """
        self.course1.taken = True
        self.course2.taken = True
        self.assertTrue(self.course_two_prereq.is_takeable())


class TestCourseTake(unittest.TestCase):

    def setUp(self):
        """
        Set up courses to test take()
        """
        self.course1 = Course("AAA111")
        self.course2 = Course("BBB222")
        self.course_one_prereq = Course("One", [self.course1])
        self.course_two_prereq = Course("Two", [self.course1, self.course2])

    def tearDown(self):
        """
        Reset all attributes
        """
        self.course1 = None
        self.course2 = None
        self.course3 = None
        self.course_one_prereq = None
        self.course_two_prereq = None

    def test_take_leaf(self):
        """
        Take 1 course and check if course is taken
        """
        self.course1.take()
        self.assertTrue(self.course1.taken)

    def test_take_leaf_again(self):
        """
        Take 1 course twice and check if course is still taken
        """
        self.course1.take()
        self.assertTrue(self.course1.taken)
        self.course1.take()
        self.assertTrue(self.course1.taken)

    def test_take_one_prereq_error(self):
        """
        Check if UntakeableError is raised if course is taken if prereq is
        not
        """
        self.assertRaises(UntakeableError, self.course_one_prereq.take)
        self.assertFalse(self.course_one_prereq.taken)

    def test_take_one_prereq(self):
        """
        Set course's prereq to taken, then take the course and check if
        course has been taken
        """
        self.course1.taken = True
        self.course_one_prereq.take()
        self.assertTrue(self.course_one_prereq.taken)

    def test_take_two_prereq_error(self):
        """
        Check if prereq error is raised if try to take only one of the
        course's prereq, then try to take the course.
        """
        self.course1.taken = True
        self.assertRaises(UntakeableError, self.course_two_prereq.take)
        self.assertFalse(self.course_two_prereq.taken)

    def test_take_two_prereq(self):
        """
        Check if course is taken if both its prereqs are taken
        """
        self.course1.taken = True
        self.course2.taken = True
        self.course_two_prereq.take()
        self.assertTrue(self.course_two_prereq.taken)


class TestCourseAddPrereq(unittest.TestCase):

    def setUp(self):
        """
        Set up all courses to test addprereq()
        """
        self.course1 = Course("AAA111")
        self.course2 = Course("BBB222")
        self.course3 = Course("CCC333")
        self.course_no_prereq = Course("None")
        self.course_one_prereq = Course("One", [self.course1])
        self.course_two_prereq = Course("Two", [self.course1, self.course2])

    def tearDown(self):
        """
        Reset all courses initialised at setUp
        """
        self.course1 = None
        self.course2 = None
        self.course3 = None
        self.course_no_prereq = None
        self.course_one_prereq = None
        self.course_two_prereq = None

    def test_add_prereq_none(self):
        """
        Adds a course prereq to a course objects's prereq attribute
        and checks if the course has been added to prereq
        """
        self.course_no_prereq.add_prereq(self.course1)
        self.assertEqual(self.course_no_prereq.prereqs, [self.course1])

    def test_add_prereq_itself(self):
        """
        Checks if PrerequisteError is raised if attempted to add prereq to
        tree with already prereq
        """
        with self.assertRaises(PrerequisiteError):
            self.course1.add_prereq(self.course1)

    def test_add_prereq_have_one_repeat_error(self):
        """
        Checks if PrerequisteError is raised if attempted to add prereq to
        same course
        """
        with self.assertRaises(PrerequisiteError):
            self.course_one_prereq.add_prereq(self.course1)

    def test_add_prereq_have_one(self):
        """
        Add second prereq to course with only 1 prereq, then checks if course
        contains both prereqs
        """
        self.course_one_prereq.add_prereq(self.course2)
        prereqs = [self.course1, self.course2]
        self.assertEqual(self.course_one_prereq.prereqs, prereqs)

    def test_add_prereq_have_two_repeat_error(self):
        """
        Checks if PrerequisteError is raised if tried to add each course in
        course prereqs again
        """
        with self.assertRaises(PrerequisiteError):
            self.course_two_prereq.add_prereq(self.course1)
        with self.assertRaises(PrerequisiteError):
            self.course_two_prereq.add_prereq(self.course2)

    def test_add_prereq_course_with_prereq(self):
        """
        Checks if PrerequisteError is raised if course with 2 prereqs is
        added
        """
        self.course3.add_prereq(self.course_two_prereq)
        self.assertEqual(self.course3.prereqs, [self.course_two_prereq])
        self.assertTrue(self.course1.is_prereq(self.course3))
        self.assertTrue(self.course2.is_prereq(self.course3))

    def test_add_prereq_course_with_prereq_repeat_error(self):
        """
        Checks if PrerequisteError is raised if every course in course
        prereqs is added as prereq
        """
        self.course3.add_prereq(self.course_two_prereq)
        with self.assertRaises(PrerequisiteError):
            self.course3.add_prereq(self.course_two_prereq)
        with self.assertRaises(PrerequisiteError):
            self.course3.add_prereq(self.course1)
        with self.assertRaises(PrerequisiteError):
            self.course3.add_prereq(self.course2)

    def test_add_prereq_is_prereq_of_error(self):
        """
        Check if PrerequisteError is raised if attempted to add prereq, if
        it already has been included
        """
        with self.assertRaises(PrerequisiteError):
            self.course1.add_prereq(self.course_one_prereq)

    def test_add_prereq_is_prereq_of_error_furthur_down(self):
        """
        Add course_two_prereq as prereq to course3, hence all prereqs of
        course_two_prereq become prereqs of course3
        Check if PrerequisiteError is raised if the prereq of course3 is
        attempting to add course itself as prereq
        """
        self.course3.add_prereq(self.course_two_prereq)
        with self.assertRaises(PrerequisiteError):
            self.course1.add_prereq(self.course3)
        with self.assertRaises(PrerequisiteError):
            self.course2.add_prereq(self.course3)


class TestCourseMissingPrereq(unittest.TestCase):

    def setUp(self):
        """
        Set up all course objects to check
        """
        self.course1 = Course("AAA111")
        self.course2 = Course("BBB222")
        self.course_no_prereq = Course("None")
        self.course_one_prereq = Course("One", [self.course1])
        self.course_two_prereq = Course("Two", [self.course1, self.course2])
        self.course3 = Course("CCC333", [self.course_two_prereq])

    def tearDown(self):
        """
        Reset all courses
        """
        self.course1 = None
        self.course2 = None
        self.course3 = None
        self.course_no_prereq = None
        self.course_one_prereq = None
        self.course_two_prereq = None

    def test_missing_prereq_none(self):
        """
        Check if missing prereqs of course with no prereqs is none
        """
        p_l = []
        self.assertEqual(self.course_no_prereq.missing_prereqs(), p_l)

    def test_missing_prereq_one(self):
        """
        Check if returns all prereqs of course which have not been taken
        """
        p_l = ["AAA111"]
        self.assertEqual(self.course_one_prereq.missing_prereqs(), p_l)

    def test_missing_prereq_one_no(self):
        """
        Take the prereq in course object, check if [] is returned if
        missing_prereq() is called.
        """
        self.course1.taken = True
        p_l = []
        self.assertEqual(self.course_one_prereq.missing_prereqs(), p_l)

    def test_missing_prereq_one_of_two(self):
        """
        Take only one of the prereqs in course object, check if the other
        prereq (not taken) is returned when missing_prereqs() is called
        """
        self.course1.taken = True
        p_l = ["BBB222"]
        self.assertEqual(self.course_two_prereq.missing_prereqs(), p_l)

    def test_missing_prereq_two(self):
        """
        Set no prereqs to taken, check if names of both prereqs are returned
        when missing_prereqs() is called
        """
        p_l = ["AAA111", "BBB222"]
        self.assertEqual(self.course_two_prereq.missing_prereqs(), p_l)

    def test_missing_prereq_two_no(self):
        """
        Set both prereqs to taken, check if [] is returned when
        missing_prereqs() is called
        """
        self.course1.taken = True
        self.course2.taken = True
        p_l = []
        self.assertEqual(self.course_two_prereq.missing_prereqs(), p_l)

    def test_missing_prereq_all(self):
        """
        Set all prereqs to untaken, check if list of all prereqs is returned
        when missing_prereqs() is called
        """
        p_l = ["AAA111", "BBB222", "Two"]
        self.assertEqual(self.course3.missing_prereqs(), p_l)

    def test_missing_prereq_furthur_down(self):
        """
        Set one prereq to taken and two to untaken, then check if the untaken
        prereqs are returned when missing_prereqs() is called
        """
        self.course2.taken = True
        p_l = ["AAA111", "Two"]
        self.assertEqual(self.course3.missing_prereqs(), p_l)

if __name__ == '__main__':
    unittest.main(exit=False)
