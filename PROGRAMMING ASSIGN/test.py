import unittest
from operation import *

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        # Clear global data structures before each test
        books.clear()
        members.clear()

    def test_add_book(self):
        self.assertTrue(add_book("978-0001", "Test Book", "Test Author", "Fiction", 1))
        self.assertIn("978-0001", books)
        self.assertFalse(add_book("978-0001", "Duplicate", "Author", "Fiction", 1))  # Duplicate ISBN
        self.assertFalse(add_book("978-0002", "Invalid Genre", "Author", "Invalid", 1))  # Invalid genre
        self.assertFalse(add_book("978-0003", "Zero Copies", "Author", "Fiction", 0))  # Invalid copies

    def test_update_book(self):
        add_book("978-0001", "Original Title", "Original Author", "Fiction", 2)
        self.assertTrue(update_book("978-0001", title="New Title"))
        self.assertEqual(books["978-0001"]["title"], "New Title")
        self.assertFalse(update_book("978-9999", title="Nonexistent"))  # Not found
        self.assertFalse(update_book("978-0001", genre="Invalid"))  # Invalid genre
        # Test total_copies reduction failure if borrowed
        borrow_book("M001", "978-0001")  # Assume member added first
        add_member("M001", "Test Member", "test@email.com")
        borrow_book("M001", "978-0001")
        self.assertFalse(update_book("978-0001", total_copies=0))  # Can't reduce below borrowed

    def test_delete_book(self):
        add_book("978-0001", "Deletable", "Author", "Fiction", 1)
        self.assertTrue(delete_book("978-0001"))
        self.assertNotIn("978-0001", books)
        self.assertFalse(delete_book("978-9999"))  # Not found
        # Can't delete if borrowed
        add_book("978-0002", "Borrowed", "Author", "Fiction", 1)
        add_member("M001", "Test Member", "test@email.com")
        borrow_book("M001", "978-0002")
        self.assertFalse(delete_book("978-0002"))

    def test_search_books(self):
        add_book("978-0001", "Python Book", "Bob Coder", "Non-Fiction", 1)
        add_book("978-0002", "Other Book", "Other Author", "Fiction", 1)
        results = search_books("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Python Book")
        results = search_books("nonexistent")
        self.assertEqual(len(results), 0)

    def test_add_member(self):
        self.assertTrue(add_member("M001", "Test Name", "test@email.com"))
        self.assertEqual(len(members), 1)
        self.assertFalse(add_member("M001", "Duplicate", "email.com"))  # Duplicate ID

    def test_update_member(self):
        add_member("M001", "Original Name", "original@email.com")
        self.assertTrue(update_member("M001", name="New Name"))
        self.assertEqual(members[0]["name"], "New Name")
        self.assertFalse(update_member("M999", name="Nonexistent"))

    def test_delete_member(self):
        add_member("M001", "Deletable", "email.com")
        self.assertTrue(delete_member("M001"))
        self.assertEqual(len(members), 0)
        self.assertFalse(delete_member("M999"))  # Not found
        # Can't delete if borrowed books
        add_member("M002", "Borrower", "email.com")
        add_book("978-0001", "Book", "Author", "Fiction", 1)
        borrow_book("M002", "978-0001")
        self.assertFalse(delete_member("M002"))

    def test_borrow_book(self):
        add_member("M001", "Borrower", "email.com")
        add_book("978-0001", "Available", "Author", "Fiction", 1)
        self.assertTrue(borrow_book("M001", "978-0001"))
        self.assertIn("978-0001", members[0]["borrowed_books"])
        self.assertEqual(books["978-0001"]["available_copies"], 0)
        self.assertFalse(borrow_book("M001", "978-0001"))  # No copies
        # Max borrow limit
        add_book("978-0002", "Book2", "Author", "Fiction", 1)
        add_book("978-0003", "Book3", "Author", "Fiction", 1)
        add_book("978-0004", "Book4", "Author", "Fiction", 1)
        borrow_book("M001", "978-0002")
        borrow_book("M001", "978-0003")
        self.assertFalse(borrow_book("M001", "978-0004"))  # Exceeds max

    def test_return_book(self):
        add_member("M001", "Borrower", "email.com")
        add_book("978-0001", "Borrowed", "Author", "Fiction", 1)
        borrow_book("M001", "978-0001")
        self.assertTrue(return_book("M001", "978-0001"))
        self.assertNotIn("978-0001", members[0]["borrowed_books"])
        self.assertEqual(books["978-0001"]["available_copies"], 1)
        self.assertFalse(return_book("M001", "978-0001"))  # Not borrowed
        self.assertFalse(return_book("M999", "978-0001"))  # Member not found

if __name__ == "__main__":
    unittest.main()