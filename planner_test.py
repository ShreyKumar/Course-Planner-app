# Assignment 2 - Unit Tests for Course (Sample tests)
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
import unittest

from planner import TermPlanner, parse_course_data
from course import Course


class TestParser(unittest.TestCase):

    def test_binary_simple(self):
        filename = 'binary_simple.txt'

        actual = parse_course_data(filename)
        self.assertEqual('CSC207', actual.name)

        prereqs = actual.prereqs
        prereq_names = [p.name for p in prereqs]
        # User assertCountEqual when order doesn't matter
        self.assertCountEqual(['CSC165', 'CSC148'], prereq_names)

        for p in prereqs:
            self.assertEqual([], p.prereqs)
    
    def test_binary_another_course(self):
        filename_another_course = 'single.txt'
    
        actual_another_course = parse_course_data(filename)
        self.assertEqual('CSC236', actual_another_course.name)
        
        prereqs = actual_another_course.prereqs
        prereq_names = [p.name for p in prereqs]
        # User assertCountEqual when order doesn't matter
        self.assertCountEqual(['CSC165', 'CSC148'], prereq_names)
        
        for p in prereqs:
            self.assertEqual([], p.prereqs)        


class TestIsValid(unittest.TestCase):
    def setUp(self):

        # Single prereq
        self.single = TermPlanner('single.txt')
        self.linear = TermPlanner('linear.txt')

    #def test_single_two(self):
        #self.assertTrue(self.single.is_valid([['CSC108'], ['CSC148']]))
    
    #def test_typical_student(self):
        #self.assertTrue(self.single.is_valid([['CSC108', 'CSC165'], ['CSC148']]))
    
    #def test_more_courses(self):
        #self.assertTrue(self.single.is_valid([['CSC108'], ['CSC148', 'CSC165'], ['CSC207']]))
        
    #def test_opposite(self):
        #self.assertFalse(self.single.is_valid([['CSC148'], ['CSC108']]))
    
    #def test_same_time(self):
        #self.assertFalse(self.single.is_valid(['CSC108', 'CSC148']))
    
    def test_long_one(self):
        self.assertTrue(self.single.is_valid([['CSC001', 'CSC101', 'CSC102', 'CSC103'], ['CSC002', 'CSC105', 'CSC131', 'CSC201', 'CSC104'], ['CSC003', 'CSC202', 'CSC203'], ['CSC004', 'CSC300'], ['CSC005'], ['CSC110'], ['CSC210'], ['CSC301'], ['CSC400']]))

    def test_long_linear(self):
        self.assertTrue(self.linear.is_valid([['1'],['2'],['3'],['4'],['5'],['6'],['7'],['8'],['9'],['0']]))



class TestPlanner(unittest.TestCase):
    def setUp(self):
        # Single prereq
        self.single = TermPlanner('single.txt')

    def gen_test(self, tp, courses):
        s = tp.generate_schedule(courses)
        # Uncomment this line if you implement good_schedule.
        #self.assertTrue(good_schedule(tp, s, courses))

    def test_one_prereq(self):
        self.gen_test(self.single, ['CSC108', 'CSC148'])


    #def good_schedule(tp, schedule, courses):
    """ (TermPlanner, list of (list of str)) -> bool
    Return True if schedule is an acceptable output
    of tp.generate_courses(courses).
    """
    #if tp.is_valid(shedule):


if __name__ == '__main__':
    unittest.main(exit=False)
