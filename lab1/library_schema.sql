CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE user_role AS ENUM ('reader', 'librarian');
CREATE TYPE user_status AS ENUM ('active', 'blocked');
CREATE TYPE copy_status AS ENUM ('available', 'reserved', 'loaned', 'lost', 'damaged');
CREATE TYPE reservation_status AS ENUM ('active', 'fulfilled', 'cancelled', 'expired');
CREATE TYPE fine_status AS ENUM ('unpaid', 'paid', 'waived');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(160) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role user_role NOT NULL DEFAULT 'reader',
    status user_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE authors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(160) NOT NULL UNIQUE
);

CREATE TABLE genres (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    isbn VARCHAR(17) NOT NULL UNIQUE,
    title VARCHAR(300) NOT NULL,
    publication_year SMALLINT CHECK (publication_year BETWEEN 1450 AND 2100),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE book_authors (
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES authors(id) ON DELETE RESTRICT,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE book_genres (
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    genre_id UUID NOT NULL REFERENCES genres(id) ON DELETE RESTRICT,
    PRIMARY KEY (book_id, genre_id)
);

CREATE TABLE book_copies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
    inventory_code VARCHAR(32) NOT NULL UNIQUE,
    status copy_status NOT NULL DEFAULT 'available',
    acquired_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reader_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    copy_id UUID NOT NULL REFERENCES book_copies(id) ON DELETE RESTRICT,
    status reservation_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    CHECK (expires_at > created_at)
);

CREATE TABLE loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reader_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    copy_id UUID NOT NULL REFERENCES book_copies(id) ON DELETE RESTRICT,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    due_at TIMESTAMPTZ NOT NULL,
    returned_at TIMESTAMPTZ,
    CHECK (due_at > issued_at),
    CHECK (returned_at IS NULL OR returned_at >= issued_at)
);

CREATE TABLE fines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reader_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    loan_id UUID NOT NULL UNIQUE REFERENCES loans(id) ON DELETE RESTRICT,
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    status fine_status NOT NULL DEFAULT 'unpaid',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    paid_at TIMESTAMPTZ,
    CHECK ((status = 'paid') = (paid_at IS NOT NULL))
);

CREATE UNIQUE INDEX uq_active_reservation_per_copy
    ON reservations(copy_id) WHERE status = 'active';
CREATE UNIQUE INDEX uq_active_loan_per_copy
    ON loans(copy_id) WHERE returned_at IS NULL;
CREATE INDEX ix_books_title ON books USING btree (lower(title));
CREATE INDEX ix_books_isbn ON books(isbn);
CREATE INDEX ix_copies_book_status ON book_copies(book_id, status);
CREATE INDEX ix_loans_due_at ON loans(due_at) WHERE returned_at IS NULL;
CREATE INDEX ix_reservations_expiry ON reservations(expires_at) WHERE status = 'active';
