"""Opt-in loopback PostgreSQL staging; only our random disposable schema."""

import os
import secrets
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from test_mathematics_batch2 import finish_new
from test_mathematics_batch3 import finish_arithmetic
from test_mathematics_batch4 import finish_parts
from test_mathematics_batch5 import finish_to_zero
from test_mathematics_batch6 import finish_properties
from test_mathematics_batch7 import finish_unknowns
from test_mathematics_batch8 import finish_first_book
from test_mathematics_grade2_part1 import finish_new as finish_grade2
from test_mathematics_grade2_part1_batch2 import finish_new as finish_grade2_second
from test_mathematics_grade2_part1_batch3 import finish_new as finish_grade2_third
from test_mathematics_grade2_part1_batch4 import finish_new as finish_grade2_fourth
from test_mathematics_grade2_part1_batch5 import finish_new as finish_grade2_fifth
from test_mathematics_grade2_part1_batch6 import finish_new as finish_grade2_sixth
from test_mathematics_grade2_part1_batch7 import finish_new as finish_grade2_seventh
from test_mathematics_grade2_part1_batch8 import finish_new as finish_grade2_eighth
from test_mathematics_grade2_part2 import finish_new as finish_grade2_part2
from test_mathematics_grade2_part2_batch2 import (
    finish_new as finish_grade2_part2_second,
)
from test_mathematics_grade2_part2_batch3 import finish_new as finish_grade2_part2_third
from test_mathematics_part2 import finish_second
from test_mathematics_part2_batch2 import finish_new as finish_second_new
from test_mathematics_part2_batch3 import finish_new as finish_second_third
from test_mathematics_part2_batch4 import finish_new as finish_second_fourth
from test_mathematics_part2_batch5 import finish_new as finish_second_fifth
from test_mathematics_part2_batch6 import finish_new as finish_second_sixth
from test_mathematics_part3 import finish_third
from test_mathematics_part3_batch2 import finish_new as finish_third_second
from test_mathematics_part3_batch3 import finish_new as finish_third_third
from test_mathematics_part3_batch4 import finish_new as finish_third_fourth
from test_mathematics_part3_batch5 import finish_new as finish_third_fifth
from test_mathematics_part3_batch6 import finish_new as finish_third_sixth
from test_mathematics_part3_batch7 import finish_new as finish_third_seventh
from test_mathematics_part4 import finish_fourth
from test_mathematics_part4_batch2 import finish_new as finish_fourth_second
from test_mathematics_part4_batch3 import finish_new as finish_fourth_third
from test_mathematics_part4_batch4 import finish_new as finish_fourth_fourth
from test_mathematics_part4_batch5 import finish_new as finish_fourth_fifth
from test_mathematics_part4_batch6 import finish_new as finish_fourth_sixth
from test_mathematics_preview import P, finish, make_preview
from test_mathematics_preview import (
    test_parallel_first_completions_award_only_once as check_parallel,
)

from services.database_url import normalize_database_url
from services.mathematics_curriculum import import_course, staging_url
from services.models import User


def test_math_postgres_immutable_import_first_book_and_parallel_reward(monkeypatch):
    filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
    if not filename:
        pytest.skip("opt-in local PostgreSQL URL file not supplied")
    monkeypatch.setenv("ENVIRONMENT", "test")
    url = normalize_database_url(Path(filename).read_text().strip())
    staging_url(make_url(url))
    admin = create_engine(url)
    schema = "math_preview_" + secrets.token_hex(8)
    with admin.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    try:
        client, factory = make_preview(engine, monkeypatch)
        with client:
            check_parallel((client, factory))
            for number in range(2, 6):
                assert finish(client, number)[-1]["xp_awarded"] == 10
            assert finish(client, 5)[-1]["xp_awarded"] == 0
            for number in range(6, 11):
                assert finish_new(client, number)[-1]["xp_awarded"] == 10
            assert finish_new(client, 10)[-1]["xp_awarded"] == 0
            for number in range(11, 16):
                assert finish_arithmetic(client, number)[-1]["xp_awarded"] == 10
            assert finish_arithmetic(client, 15)[-1]["xp_awarded"] == 0
            for number in range(16, 21):
                assert finish_parts(client, number)[-1]["xp_awarded"] == 10
            assert finish_parts(client, 20)[-1]["xp_awarded"] == 0
            for number in range(21, 26):
                assert finish_to_zero(client, number)[-1]["xp_awarded"] == 10
            assert finish_to_zero(client, 25)[-1]["xp_awarded"] == 0
            for number in range(26, 31):
                assert finish_properties(client, number)[-1]["xp_awarded"] == 10
            assert finish_properties(client, 30)[-1]["xp_awarded"] == 0
            for number in range(31, 36):
                assert finish_unknowns(client, number)[-1]["xp_awarded"] == 10
            assert finish_unknowns(client, 35)[-1]["xp_awarded"] == 0
            for number in range(36, 42):
                assert finish_first_book(client, number)[-1]["xp_awarded"] == 10
            assert finish_first_book(client, 41)[-1]["xp_awarded"] == 0
            assert all(
                l["state"] == "completed"
                for l in client.get(P + "/catalog").json()["lessons"]
            )
            for number in range(42, 47):
                assert finish_second(client, number)[-1]["xp_awarded"] == 10
            assert finish_second(client, 46)[-1]["xp_awarded"] == 0
            for number in range(47, 52):
                assert finish_second_new(client, number)[-1]["xp_awarded"] == 10
            assert finish_second_new(client, 51)[-1]["xp_awarded"] == 0
            for number in range(52, 57):
                assert finish_second_third(client, number)[-1]["xp_awarded"] == 10
            assert finish_second_third(client, 56)[-1]["xp_awarded"] == 0
            for number in range(57, 62):
                assert finish_second_fourth(client, number)[-1]["xp_awarded"] == 10
            assert finish_second_fourth(client, 61)[-1]["xp_awarded"] == 0
            for number in range(62, 69):
                assert finish_second_fifth(client, number)[-1]["xp_awarded"] == 10
            assert finish_second_fifth(client, 68)[-1]["xp_awarded"] == 0
            for number in range(69, 74):
                assert finish_second_sixth(client, number)[-1]["xp_awarded"] == 10
            assert finish_second_sixth(client, 73)[-1]["xp_awarded"] == 0
            assert all(
                l["state"] == "completed"
                for l in client.get(P + "/catalog", params={"part": 2}).json()[
                    "lessons"
                ]
            )
            assert not client.get(P + "/catalog", params={"part": 3}).json()[
                "previous_book_navigation_ready"
            ]
            monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
            for number in range(1, 6):
                assert finish_third(client, number)[-1]["xp_awarded"] == 10
            assert finish_third(client, 5)[-1]["xp_awarded"] == 0
            for number in range(6, 11):
                assert finish_third_second(client, number)[-1]["xp_awarded"] == 10
            assert finish_third_second(client, 10)[-1]["xp_awarded"] == 0
            for number in [11, 14, 15, 16, 17]:
                assert finish_third_third(client, number)[-1]["xp_awarded"] == 10
            assert finish_third_third(client, 17)[-1]["xp_awarded"] == 0
            for number in range(18, 23):
                assert finish_third_fourth(client, number)[-1]["xp_awarded"] == 10
            assert finish_third_fourth(client, 22)[-1]["xp_awarded"] == 0
            for number in [23, 24, 25, 26, 30]:
                assert finish_third_fifth(client, number)[-1]["xp_awarded"] == 10
            assert finish_third_fifth(client, 30)[-1]["xp_awarded"] == 0
            for number in range(31, 36):
                assert finish_third_sixth(client, number)[-1]["xp_awarded"] == 10
            assert finish_third_sixth(client, 35)[-1]["xp_awarded"] == 0
            for number in range(36, 43):
                assert finish_third_seventh(client, number)[-1]["xp_awarded"] == 10
            assert finish_third_seventh(client, 42)[-1]["xp_awarded"] == 0
            third = client.get(P + "/catalog", params={"part": 3}).json()
            assert not third["previous_book_complete"]
            assert third["source_gap_bridge"]["missing_source_numbers"] == [74]
            assert all(l["state"] == "completed" for l in third["lessons"])
            monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "false")
            assert not client.get(P + "/catalog", params={"part": 4}).json()[
                "previous_book_navigation_ready"
            ]
            monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
            for number in range(112, 117):
                assert finish_fourth(client, number)[-1]["xp_awarded"] == 10
            assert finish_fourth(client, 116)[-1]["xp_awarded"] == 0
            fourth = client.get(P + "/catalog", params={"part": 4}).json()
            assert not fourth["previous_book_complete"]
            assert fourth["source_gap_bridge"]["schedule_only_rows_not_completed"] == 5
            for number in range(117, 122):
                assert finish_fourth_second(client, number)[-1]["xp_awarded"] == 10
            assert finish_fourth_second(client, 121)[-1]["xp_awarded"] == 0
            for number in range(122, 127):
                assert finish_fourth_third(client, number)[-1]["xp_awarded"] == 10
            assert finish_fourth_third(client, 126)[-1]["xp_awarded"] == 0
            for number in range(127, 133):
                assert finish_fourth_fourth(client, number)[-1]["xp_awarded"] == 10
            assert finish_fourth_fourth(client, 132)[-1]["xp_awarded"] == 0
            for number in range(133, 139):
                assert finish_fourth_fifth(client, number)[-1]["xp_awarded"] == 10
            assert finish_fourth_fifth(client, 138)[-1]["xp_awarded"] == 0
            for number in range(139, 145):
                assert finish_fourth_sixth(client, number)[-1]["xp_awarded"] == 10
            assert finish_fourth_sixth(client, 144)[-1]["xp_awarded"] == 0
            fourth = client.get(P + "/catalog", params={"part": 4}).json()
            assert all(l["state"] == "completed" for l in fourth["lessons"])
            for number in range(1, 6):
                assert finish_grade2(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2(client, 5)[-1]["xp_awarded"] == 0
            for number in range(6, 11):
                assert finish_grade2_second(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_second(client, 10)[-1]["xp_awarded"] == 0
            for number in range(11, 16):
                assert finish_grade2_third(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_third(client, 15)[-1]["xp_awarded"] == 0
            for number in range(16, 22):
                assert finish_grade2_fourth(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_fourth(client, 21)[-1]["xp_awarded"] == 0
            for number in range(22, 26):
                assert finish_grade2_fifth(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_fifth(client, 25)[-1]["xp_awarded"] == 0
            strict_grade2 = client.get(P + "/catalog", params={"grade": 2}).json()
            assert strict_grade2["lessons"][-1]["state"] == "locked"
            monkeypatch.setenv("MATHEMATICS_QA_GRADE2_PART1_SOURCE_GAP", "true")
            for number in range(27, 32):
                assert finish_grade2_sixth(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_sixth(client, 31)[-1]["xp_awarded"] == 0
            for number in range(32, 37):
                assert finish_grade2_seventh(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_seventh(client, 36)[-1]["xp_awarded"] == 0
            for number in range(37, 45):
                assert finish_grade2_eighth(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_eighth(client, 44)[-1]["xp_awarded"] == 0
            monkeypatch.setenv("MATHEMATICS_QA_GRADE2_PART2_PREVIEW", "true")
            for number in range(1, 6):
                assert finish_grade2_part2(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_part2(client, 5)[-1]["xp_awarded"] == 0
            for number in range(6, 11):
                assert (
                    finish_grade2_part2_second(client, number)[-1]["xp_awarded"] == 10
                )
            assert finish_grade2_part2_second(client, 10)[-1]["xp_awarded"] == 0
            for number in range(11, 16):
                assert finish_grade2_part2_third(client, number)[-1]["xp_awarded"] == 10
            assert finish_grade2_part2_third(client, 15)[-1]["xp_awarded"] == 0
            grade2 = client.get(P + "/catalog", params={"grade": 2}).json()
            assert all(l["state"] == "completed" for l in grade2["lessons"])
            assert grade2["book"]["source_gaps"][0]["missing_printed_pages"] == [54, 55]
        with factory.begin() as db:
            assert db.get(User, 1).xp_total == 2147 and db.get(User, 2).xp_total == 0
            assert import_course(db) == {"created": 0, "skipped": 201}
    finally:
        engine.dispose()
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()
