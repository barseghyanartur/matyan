import unittest

from ..auto_correct import (
    add_final_dot,
    capitalize,
    capitalize_first_letter,
    unslugify,
)


class TestAutoCorrect(unittest.TestCase):

    def test_unslugify(self):
        """Test `unslugify`."""
        texts = [
            (
                '',
                ''
            ),
            (
                'improve-document-sharing',
                'Improve document sharing'
            ),
        ]
        for before, after in texts:
            self.assertEqual(unslugify(before), after)

    def test_add_final_dot(self):
        """Test `add_final_dot`."""
        texts = [
            (
                '',
                ''
            ),
            (
                "alice’s Right Foot, Esq. hearthrug, near The Fender",
                "alice’s Right Foot, Esq. hearthrug, near The Fender."
            ),
        ]
        for before, after in texts:
            self.assertEqual(add_final_dot(before), after)

    def test_capitalize_first_letter(self):
        """Test `capitalize_first_letter`."""
        texts = [
            (
                '',
                ''
            ),
            (
                "alice’s right Foot, Esq.",
                "Alice’s right Foot, Esq."
            ),
        ]
        for before, after in texts:
            self.assertEqual(capitalize_first_letter(before), after)

    def test_capitalize(self):
        """Test `capitalize`."""
        texts = [
            (
                '',
                ''
            ),
            (
                "alice’s Right Foot, Esq. hearthrug, near The Fender, "
                "(with Alice’s love). Oh dear, what nonsense I’m talking!’",
                "Alice’s Right Foot, Esq. Hearthrug, near The Fender, "
                "(with Alice’s love). Oh dear, what nonsense I’m talking!’"
            ),
        ]
        for before, after in texts:
            self.assertEqual(capitalize(before), after)
