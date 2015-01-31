import unittest
import yaml

from beerapp.app import app, TAGS
from beerapp.members import Member
from beerapp import db


class MembersYAMLTest(unittest.TestCase):
    def setUp(self):
        members_str = open(app.config['MEMBERS_FILE']).read()
        self.yaml = yaml.load_all(members_str)
        self.all = map(Member, yaml.load_all(members_str))

    def test_fields_exists(self):
        for member in self.yaml:
            self.assertIn('name', member.keys())
            self.assertIn('email', member.keys())
            self.assertIn('blog', member.keys())
            self.assertIn('feed', member.keys())
            self.assertIn('twitter', member.keys())
            self.assertIn('date_joined', member.keys())
            self.assertIn('id', member.keys())

    def test_id_not_repeat(self):
        ids = [member.get('id') for member in self.yaml]
        self.assertEqual(len(set(ids)), len(ids))


class AppFlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        members_str = open(app.config['MEMBERS_FILE']).read()
        self.yaml = yaml.load_all(members_str)

    def test_group_tags(self):
        _TAGS = []
        for member in self.yaml:
            if member.get('tags'):
                for tag in member['tags'].split(","):
                    _TAGS.append(tag.strip())
        self.assertEqual(TAGS(), set(_TAGS))


class MembersTest(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        members_str = open(app.config['MEMBERS_FILE']).read()
        self.yaml = yaml.load_all(members_str)
        self.all = map(Member, yaml.load_all(members_str))

    def test_load_all_member(self):
        for obj in self.all:
            self.assertEqual(0, len(obj.post_id_list))
            obj.fetch_entries()
            self.assertTrue(len(obj.post_id_list) >= 1)


if __name__ == '__main__':
    unittest.main()
