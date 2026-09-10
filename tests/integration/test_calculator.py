import os
from unittest import TestCase, mock

from click.testing import CliRunner

from pyxsdata.cli import cli
from pyxsdata.formats.dataclass.client import Client, Config
from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
from pyxsdata.formats.dataclass.transports import DefaultTransport
from pyxsdata.utils.testing import load_class
from tests import fixtures_dir, root
from tests.fixtures.calculator import (
    CalculatorSoapAdd,
    CalculatorSoapAddOutput,
)

os.chdir(root)


class CalculatorServiceTests(TestCase):
    def test_wsdl_codegen(self) -> None:
        schema = fixtures_dir.joinpath("calculator/services.wsdl")
        package = "tests.fixtures.calculator"
        runner = CliRunner()
        result = runner.invoke(
            cli, ["generate", str(schema), "--package", package]
        )

        if result.exception:
            raise result.exception

        clazz = load_class(result.output, "CalculatorSoapMultiplyOutput")
        self.assertEqual("Envelope", clazz.Meta.name)

    @mock.patch.object(DefaultTransport, "post")
    def test_client(self, mock_most) -> None:
        url = "http://www.dneonline.com/calculator.asmx"
        request = fixtures_dir.joinpath("calculator/AddRQ.xml").read_text()
        response = fixtures_dir.joinpath("calculator/AddRS.xml").read_bytes()
        headers = {
            "content-type": "text/xml",
            "SOAPAction": "http://tempuri.org/Add",
        }
        mock_most.return_value = response

        config = Config.from_service(CalculatorSoapAdd)
        serializer = XmlSerializer(config=SerializerConfig(indent="  "))
        client = Client(config=config, serializer=serializer)
        result = client.send({"Body": {"Add": {"intA": 1, "intB": 3}}})

        self.assertIsInstance(result, CalculatorSoapAddOutput)

        mock_most.assert_called_once_with(url, data=request, headers=headers)
