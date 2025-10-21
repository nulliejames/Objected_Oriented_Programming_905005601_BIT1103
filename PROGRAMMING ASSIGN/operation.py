from typing import Dict, List, Optional, Tuple

# Data structures
genres: Tuple[str, ...] = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "History", "Fantasy")
books: Dict[str, Dict] = {}
members: List[Dict] = []

def add_book(isbn: str, title: str, author: str, genre: str, total_copies: int) -> bool:
    isbn = isbn.strip()
    if not isbn:
        raise ValueError("ISBN cannot be empty.")
    if isbn in books:
        print(f"add_book: ISBN '{isbn}' already exists.")
        return False
    if genre not in genres:
        print(f"add_book: Genre '{genre}' is invalid. Valid genres: {genres}")
        return False
    if total_copies < 1:
        print("add_book: total_copies must be at least 1.")
        return False

    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        "available_copies": total_copies
    }
    print(f"add_book: Book '{title}' added with ISBN {isbn}.")
    return True


def update_book(isbn: str, title: Optional[str] = None, author: Optional[str] = None,
                genre: Optional[str] = None, total_copies: Optional[int] = None) -> bool:
    if isbn not in books:
        print(f"update_book: ISBN '{isbn}' not found.")
        return False
    book = books[isbn]

    if genre is not None and genre not in genres:
        print(f"update_book: Genre '{genre}' invalid.")
        return False

    if total_copies is not None:
        borrowed = book["total_copies"] - book["available_copies"]
        if total_copies < borrowed:
            print("update_book: Cannot set total_copies less than number of borrowed copies.")
            return False

        diff = total_copies - book["total_copies"]
        book["available_copies"] += diff
        book["total_copies"] = total_copies

    if title is not None:
        book["title"] = title
    if author is not None:
        book["author"] = author
    if genre is not None:
        book["genre"] = genre

    print(f"update_book: Book '{isbn}' updated.")
    return True


def delete_book(isbn: str) -> bool:
    if isbn not in books:
        print(f"delete_book: ISBN '{isbn}' not found.")
        return False
    book = books[isbn]
    if book["available_copies"] != book["total_copies"]:
        print("delete_book: Cannot delete book while some copies are borrowed.")
        return False
    del books[isbn]
    print(f"delete_book: Book '{isbn}' deleted.")
    return True


def search_books(query: str) -> List[Dict]:
    q = query.strip().lower()
    results = []
    for isbn, b in books.items():
        if q in b["title"].lower() or q in b["author"].lower():
            entry = b.copy()
            entry["isbn"] = isbn
            results.append(entry)
    return results


# ---------- Members ----------
def add_member(member_id: str, name: str, email: str) -> bool:
    member_id = member_id.strip()
    if not member_id:
        raise ValueError("member_id cannot be empty.")
    if any(m["member_id"] == member_id for m in members):
        print(f"add_member: Member ID '{member_id}' already exists.")
        return False
    members.append({
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []  # list of ISBNs
    })
    print(f"add_member: Member '{name}' added with ID {member_id}.")
    return True


def find_member(member_id: str) -> Optional[Dict]:
    for m in members:
        if m["member_id"] == member_id:
            return m
    return None


def update_member(member_id: str, name: Optional[str] = None, email: Optional[str] = None) -> bool:
    m = find_member(member_id)
    if not m:
        print(f"update_member: Member ID '{member_id}' not found.")
        return False
    if name is not None:
        m["name"] = name
    if email is not None:
        m["email"] = email
    print(f"update_member: Member '{member_id}' updated.")
    return True


def delete_member(member_id: str) -> bool:
    m = find_member(member_id)
    if not m:
        print(f"delete_member: Member ID '{member_id}' not found.")
        return False
    if m["borrowed_books"]:
        print("delete_member: Cannot delete member with borrowed books.")
        return False
    members.remove(m)
    print(f"delete_member: Member '{member_id}' deleted.")
    return True


# ---------- Borrow / Return ----------
MAX_BORROW = 3
def borrow_book(member_id: str, isbn: str) -> bool:
    m = find_member(member_id)
    if not m:
        print(f"borrow_book: Member '{member_id}' not found.")
        return False
    if isbn not in books:
        print(f"borrow_book: Book ISBN '{isbn}' not found.")
        return False
    book = books[isbn]
    if book["available_copies"] <= 0:
        print(f"borrow_book: No copies available for ISBN '{isbn}'.")
        return False
    if len(m["borrowed_books"]) >= MAX_BORROW:
        print(f"borrow_book: Member '{member_id}' already borrowed max ({MAX_BORROW}).")
        return False
    # proceed
    m["borrowed_books"].append(isbn)
    book["available_copies"] -= 1
    print(f"borrow_book: Member '{member_id}' borrowed '{book['title']}' (ISBN {isbn}).")
    return True


def return_book(member_id: str, isbn: str) -> bool:
    m = find_member(member_id)
    if not m:
        print(f"return_book: Member '{member_id}' not found.")
        return False
    if isbn not in books:
        print(f"return_book: Book ISBN '{isbn}' not recognized.")
        return False
    if isbn not in m["borrowed_books"]:
        print(f"return_book: Member '{member_id}' did not borrow ISBN '{isbn}'.")
        return False
    m["borrowed_books"].remove(isbn)
    books[isbn]["available_copies"] += 1
    print(f"return_book: Member '{member_id}' returned ISBN '{isbn}'.")
    return True


# ---------- Utility / Display ----------
def member_info(member_id: str) -> Optional[Dict]:
    m = find_member(member_id)
    if not m:
        return None
    return {
        "member_id": m["member_id"],
        "name": m["name"],
        "email": m["email"],
        "borrowed_books": list(m["borrowed_books"])
    }

def book_info(isbn: str) -> Optional[Dict]:
    if isbn not in books:
        return None
    b = books[isbn].copy()
    b["isbn"] = isbn
    return b