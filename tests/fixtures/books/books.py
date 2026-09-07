from __future__ import annotations

from dataclasses import dataclass, field

from pyxsdata.models.datatype import XmlDate

__NAMESPACE__ = "urn:books"


@dataclass(kw_only=True)
class BookForm:
    """
    Book Definition.

    Attributes:
        author: Writer's name
        title: Book Title
        genre: Book Genre
        price: Amount in USD
        pub_date: Publication date
        review: Sticky Review
        id: International Standard Book Number
        lang: Language ISO Code
    """

    author: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    title: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    genre: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    price: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pub_date: XmlDate = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    review: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: str = field(
        init=False,
        default="en",
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BooksForm:
    book: list[BookForm] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class Books(BooksForm):
    """
    Το βιβλίο.
    """

    class Meta:
        name = "books"
        namespace = "urn:books"
