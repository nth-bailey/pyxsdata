from __future__ import annotations

from dataclasses import dataclass, field

from pyxsdata.models.datatype import XmlDate


@dataclass(kw_only=True)
class Country:
    class Meta:
        name = "country"

    name: str = field(
        metadata={
            "type": "Element",
        }
    )
    code: str = field(
        metadata={
            "type": "Element",
        }
    )
    timezone: None | str = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )


@dataclass(kw_only=True)
class Externals:
    class Meta:
        name = "externals"

    tvrage: int = field(
        metadata={
            "type": "Element",
        }
    )
    thetvdb: None | int = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    imdb: str = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Image:
    class Meta:
        name = "image"

    medium: str = field(
        metadata={
            "type": "Element",
        }
    )
    original: str = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Previousepisode:
    class Meta:
        name = "previousepisode"

    href: str = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Rating:
    class Meta:
        name = "rating"

    average: float = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Schedule:
    class Meta:
        name = "schedule"

    time: str = field(
        metadata={
            "type": "Element",
        }
    )
    days: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Self:
    class Meta:
        name = "self"

    href: str = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Links:
    class Meta:
        name = "_links"

    self_value: Self = field(
        metadata={
            "name": "self",
            "type": "Element",
        }
    )
    previousepisode: Previousepisode = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Network:
    class Meta:
        name = "network"

    id: None | int = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    name: str = field(
        metadata={
            "type": "Element",
        }
    )
    country: Country = field(
        metadata={
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class Series:
    class Meta:
        name = "series"

    id: int = field(
        metadata={
            "type": "Element",
        }
    )
    url: None | str = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    name: str = field(
        metadata={
            "type": "Element",
        }
    )
    type_value: str = field(
        metadata={
            "name": "type",
            "type": "Element",
        }
    )
    language: str = field(
        metadata={
            "type": "Element",
        }
    )
    genres: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    status: str = field(
        metadata={
            "type": "Element",
        }
    )
    runtime: int = field(
        metadata={
            "type": "Element",
        }
    )
    premiered: XmlDate = field(
        metadata={
            "type": "Element",
        }
    )
    official_site: str = field(
        metadata={
            "name": "officialSite",
            "type": "Element",
        }
    )
    schedule: Schedule = field(
        metadata={
            "type": "Element",
        }
    )
    rating: Rating = field(
        metadata={
            "type": "Element",
        }
    )
    weight: None | int = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    network: Network = field(
        metadata={
            "type": "Element",
        }
    )
    web_channel: None | object = field(
        default=None,
        metadata={
            "name": "webChannel",
            "type": "Element",
        },
    )
    externals: Externals = field(
        metadata={
            "type": "Element",
        }
    )
    image: None | Image = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    summary: str = field(
        metadata={
            "type": "Element",
        }
    )
    updated: int = field(
        metadata={
            "type": "Element",
        }
    )
    links: None | Links = field(
        default=None,
        metadata={
            "name": "_links",
            "type": "Element",
        },
    )
