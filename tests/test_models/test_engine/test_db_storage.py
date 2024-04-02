#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import logging
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import pep8
import unittest
DBStorage = db_storage.DBStorage
d_storage = DBStorage()  # storage from db_storage file directly.
i_storage = models.storage  # storage from init.
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}
created_objs = []


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDbStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def tearDown(self):
        """Clean up after each test method"""
        # Delete any objects created during the test
        for obj in created_objs:
            pass
        # i_storage.delete(obj)
        # print([ (i, i.name) for i in created_objs])
        # Commit changes
        i_storage.save()
        # Close the session
        # i_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        i_storage.reload()

        with self.subTest("all shoud return a dictionary"):
            self.assertIs(type(i_storage.all()), dict)

        state_objs_before = i_storage.all(State)

        state_1 = State(name="Rabat")
        created_objs.append(state_1)
        key_1 = "State.{}".format(state_1.id)

        state_2 = State(name="Sale")
        created_objs.append(state_2)
        key_2 = "State.{}".format(state_2.id)

        # adding 2 states two DB.
        i_storage.new(state_1)
        i_storage.new(state_2)
        # i_storage.save()

        # all object after adding 2 states
        state_objs_after = i_storage.all(State)

        state_c_1 = state_objs_after.get(key_1, "Not Found")
        state_c_2 = state_objs_after.get(key_2, "Not Found")

        with self.subTest("It should return 2 objects"):
            self.assertEqual(len(state_objs_after) - len(state_objs_before), 2)

        with self.subTest("they must be instance of State"):
            self.assertIsInstance(state_c_1, State)
            self.assertIsInstance(state_c_2, State)

        with self.subTest("they all shoud have same id"):
            self.assertEqual(state_c_1.id, state_1.id)
            self.assertEqual(state_c_2.id, state_2.id)

        with self.subTest("they all shoud have same name"):
            self.assertEqual(state_c_1.name, state_1.name)
            self.assertEqual(state_c_2.name, state_2.name)

        # Delete recently created 2 states.
        # i_storage.delete(state_1)
        # i_storage.delete(state_2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        i_storage.reload()

        state_C = State(name="CasaBlanca")
        # created_objs.append(state_C)
        state_C_id = state_C.id
        key = "State.{}".format(state_C_id)

        with self.subTest("without using method new"):
            state_C_sess = i_storage._DBStorage__session.query(State).filter(
                    State.id == state_C_id).first()
            self.assertEqual(state_C_sess, None)  # Won't be found.

        i_storage.new(state_C)

        with self.subTest("using method new"):
            state_C_sess = i_storage._DBStorage__session.query(State).filter(
                    State.id == state_C_id).first()
            self.assertNotEqual(state_C_sess, None)  # Will be found.

        i_storage.reload()

        objs = i_storage.all(State)

        with self.subTest("It should not be loaded without save function"):
            #  Won't be loaded, save is not used yet.
            self.assertFalse(key in objs.keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to MySQL db"""
        i_storage.reload()

        state_K = State(name="Sidi Kacem")
        created_objs.append(state_K)
        state_K_id = state_K.id
        key = "State.{}".format(state_K_id)

        with self.subTest("without using method new"):
            state_K_sess = i_storage._DBStorage__session.query(State).filter(
                    State.id == state_K_id).first()
            self.assertEqual(state_K_sess, None)  # won't be found.

        i_storage.new(state_K)
        i_storage.save()
        i_storage.close()
        i_storage.reload()

        with self.subTest("using method new"):
            state_K_sess = i_storage._DBStorage__session.query(State).filter(
                    State.id == state_K_id).first()
            self.assertNotEqual(state_K_sess, None)  # Will be found

        objs = i_storage.all(State)

        with self.subTest("It should not be loaded without save function"):
            self.assertTrue(key in objs.keys())  # Will be loaded

        # i_storage.delete(state_K)
        i_storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test that delete removes an object from the database"""

        # Reload the storage
        i_storage.reload()

        # Create a new object
        state_L = State(name="Larache")
        state_L_id = state_L.id
        key = "State.{}".format(state_L_id)

        # Add the object to the database
        i_storage.new(state_L)
        i_storage.save()

        # Check if the object exists in the session before deletion
        with self.subTest("Object should exist before deletion"):
            state_L_sess = i_storage._DBStorage__session.query(State).filter(
                    State.id == state_L_id).first()
            # Object should exist in the session
            self.assertIsNotNone(state_L_sess)

        # Delete the object from the session
        i_storage.delete(state_L)
        i_storage.save()

        # Check if the object exists in the session after deletion
        with self.subTest("Object should not exist after deletion"):
            state_L_sess = i_storage._DBStorage__session.query(State).filter(
                    State.id == state_L_id).first()
            # Object should not exist in the session after deletion
            self.assertIsNone(state_L_sess)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves the correct object from the database"""

        # Reload the storage
        i_storage.reload()

        # Create a new object
        state_M = State(name="Mohamedia")
        created_objs.append(state_M)
        state_M_id = state_M.id

        # Add the object to the database
        i_storage.new(state_M)
        i_storage.save()

        # Retrieve the object using get method
        retrieved_state_M = i_storage.get(State, state_M_id)

        # Check if the retrieved object is the same as the original object
        with self.subTest("Retrieved object should match original object"):
            self.assertEqual(state_M, retrieved_state_M)

        # Try to retrieve an object that doesn't exist
        retrieved_state_nonexistent = i_storage.get(State, 'nonexistent_id')

        # Check if the retrieved object is None when object doesn't exist
        with self.subTest("should be None when object doesn't exist"):
            self.assertIsNone(retrieved_state_nonexistent)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct number of
        objects from the database
        """

        # Reload the storage
        i_storage.reload()

        # Count the total number of objects in the database before creation
        total_objects_count_before = i_storage.count()

        # Create two new objects
        state_T1 = State(name="Tetouan1")
        state_T2 = State(name="Tetouan2")
        created_objs.append(state_T1)
        created_objs.append(state_T2)

        # Add the objects to the database
        i_storage.new(state_T1)
        i_storage.new(state_T2)
        i_storage.save()

        # Count the total number of objects in the database after creation
        total_objects_count_after = i_storage.count()

        # Check if the count difference is greater than or equal to zero
        with self.subTest("Count difference should be >= than zero"):
            self.assertGreaterEqual(
                    total_objects_count_after - total_objects_count_before, 0)

        # Count the number of State objects in the database
        state_objects_count = i_storage.count(State)
        state_objects_storage = i_storage.all(State)

        # Check if the count matches the expected number of State objects
        with self.subTest("State count should match the expected count"):
            self.assertEqual(state_objects_count, len(state_objects_storage))
