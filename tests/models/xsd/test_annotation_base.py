from unittest import TestCase

from pyxsdata.formats.dataclass.models.generics import AnyElement
from pyxsdata.models.xsd import Annotation, AnnotationBase, Documentation


class AnnotationBaseTest(TestCase):
    def test_property_display_help(self) -> None:
        base = AnnotationBase()
        self.assertIsNone(base.display_help)

        base.annotations.append(Annotation(documentations=[Documentation()]))
        self.assertIsNone(base.display_help)

        base.annotations.append(
            Annotation(
                documentations=[
                    Documentation(
                        content=[
                            "    I am a ",
                            AnyElement(
                                qname="{http://www.w3.org/1999/xhtml}p",
                                text="test",
                                tail="\n",
                                children=[
                                    AnyElement(
                                        qname="{http://www.w3.org/1999/xhtml}span",
                                        text="!",
                                    )
                                ],
                            ),
                        ]
                    )
                ]
            )
        )
        self.assertEqual("I am a <p>test<span>!</span>\n</p>", base.display_help)
