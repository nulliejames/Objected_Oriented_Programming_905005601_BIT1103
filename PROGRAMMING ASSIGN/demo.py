from operation import *

# Add some books
add_book("978-0001", "The Great Adventure", "Alice Writer", "Fiction", 3)
add_book("978-0002", "Python for Beginners", "Bob Coder", "Non-Fiction", 2)
add_book("978-0003", "Space Odyssey", "Carol SciFi", "Sci-Fi", 1)

# Add members
add_member("M001", "John Doe", "john@example.com")
add_member("M002", "Jane Smith", "jane@example.com")

# Search
print("\nSearch 'python':", search_books("python"))

# Borrowing
borrow_book("M001", "978-0002")  # John borrows Python book
borrow_book("M001", "978-0001")  # John borrows Fiction
borrow_book("M002", "978-0003")  # Jane borrows Sci-Fi

# Trying to borrow unavailable
borrow_book("M002", "978-0003")  # should show no copies available

# Return
return_book("M001", "978-0001")

# Update book (increase total copies)
update_book("978-0003", total_copies=2)

# Delete attempts
delete_book("978-0002")  # fail if copies borrowed
# Return that one
return_book("M001", "978-0002")
delete_book("978-0002")  # should now succeed

# Member deletion
delete_member("M002")  # fail if M002 still has borrowed books
return_book("M002", "978-0003")
delete_member("M002")  # should succeed

# Print final state
print("\nBooks:", books)
print("Members:", members)