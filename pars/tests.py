import json
import os

from django.conf import settings
from django.test import TestCase
from django.test import Client

from pars.models import Log
from pars.serializers import TransformSerializer, LogCreateSerializer
from pars.utils import DictObj

TEST_RESOURCE_PATH = os.path.join(settings.BASE_DIR, "test_resources")


class ParserTestCase(TestCase):
    def setUp(self):
        with open(os.path.join(TEST_RESOURCE_PATH, "input.json"), "r") as input_file:
            self.input = json.loads(input_file.read())

    def test_validator_serializer(self):
        self.assertTrue(
            LogCreateSerializer(data=self.input).is_valid(),
            "Input was not validated",
        )

    def test_validator_missing_id(self):
        self.input.pop("id")
        self.assertFalse(
            LogCreateSerializer(data=self.input).is_valid(),
            "id is required",
        )

    def test_validator_missing_created(self):
        self.input.pop("created")
        self.assertFalse(
            LogCreateSerializer(data=self.input).is_valid(),
            "created is required",
        )

    def test_validator_missing_updated(self):
        self.input.pop("updated")
        self.assertTrue(
            LogCreateSerializer(data=self.input).is_valid(),
            "updated should not be required",
        )

    def test_transform_serializer(self):
        serializer = LogCreateSerializer(data=self.input)
        serializer.is_valid(raise_exception=True)
        transformed_data = TransformSerializer(
            instance=DictObj(serializer.validated_data)
        ).data
        self.check_key_existence(transformed_data)
        self.assertEqual(
            transformed_data["counters_total"], 3, "sum was not calculated correctly"
        )
        with open(os.path.join(TEST_RESOURCE_PATH, "output.json"), "r") as output_file:
            expected_out_put = json.loads(output_file.read())

            self.assertDictEqual(
                transformed_data,
                expected_out_put,
                "output was not calculated correctly",
            )

    def check_key_existence(self, transformed_data):
        for key in ["path", "body", "author_id", "created_time", "counters_total"]:
            self.assertIn(
                key,
                transformed_data,
                f"{key} was not transformed",
            )

    def test_api(self):
        client = Client()
        response = client.post(
            "http://testserver/create/",
            data=self.input,
            content_type="application/json",
        )
        print("ASDASDASDASD", response.__dict__)
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(Log.objects.count(), 1, "there should be one object created")
        self.check_key_existence(response.json())
