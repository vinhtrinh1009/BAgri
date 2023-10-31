import unittest
import sys
sys.path.insert(
    0, "/media/thuando/e4b8fae4-08a2-4405-ad1b-c1ba018f26354/code/bagri/back_end")
from handler.season.handler import add, get_current_season_step, get_steps_from_stages
# import utils.update_stages


class TestSeasonMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_get_current_step(self):
        done_stages = [
            {
                "steps": [
                    {
                        "step_id": "620cab64d337e9856fbcbc44",
                        "idx": 0,
                        "name": "Ươm hạt",
                        "actual_day": 9
                    },
                    {
                        "step_id": "620cab64d337e9856fbcbc45",
                        "idx": 1,
                        "name": "Trồng cây",
                        "actual_day": 9
                    }
                ]
            },
            {
                "steps": [
                    {
                        "step_id": "620cab64d337e9856fbcbc47",
                        "idx": 0,
                        "name": "Ươm hạt 2",
                        "stage_id": "620cab64d337e9856fbcbc46",
                        "actual_day": 9
                    }
                ]
            }
        ]
        step = get_current_season_step(done_stages)
        self.assertEqual(step["step_id"], "620cab64d337e9856fbcbc47")

        not_done_stages = [
            {
                "steps": [
                    {
                        "step_id": "620cab64d337e9856fbcbc44",
                        "idx": 0,
                        "name": "Ươm hạt",
                        "actual_day": 9
                    },
                    {
                        "step_id": "620cab64d337e9856fbcbc45",
                        "idx": 1,
                        "name": "Trồng cây",
                    }
                ]
            },
            {
                "steps": [
                    {
                        "step_id": "620cab64d337e9856fbcbc47",
                        "idx": 0,
                        "name": "Ươm hạt",
                    }
                ]
            }
        ]
        step = get_current_season_step(not_done_stages)
        self.assertEqual(step["step_id"], "620cab64d337e9856fbcbc45")

    def test_get_steps_from_stages(self):
        stages = [
            {
                "steps": [
                    {
                        "step_id": "620cab64d337e9856fbcbc44",
                        "idx": 0,
                        "name": "Ươm hạt",
                        "actual_day": 9
                    },
                    {
                        "step_id": "620cab64d337e9856fbcbc45",
                        "idx": 1,
                        "name": "Trồng cây",
                    }
                ]
            },
            {
                "steps": [
                    {
                        "step_id": "620cab64d337e9856fbcbc47",
                        "idx": 0,
                        "name": "Ươm hạt",
                    }
                ]
            }
        ]
        steps = get_steps_from_stages(stages)
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[1]["step_id"], "620cab64d337e9856fbcbc45")


if __name__ == '__main__':
    unittest.main()
