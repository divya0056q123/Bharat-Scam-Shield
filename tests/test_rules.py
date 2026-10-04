import unittest
from backend.rules import analyze

class T(unittest.TestCase):
    def test_pdf_example(self):
        r = analyze("Invest ₹10,000 today and get ₹50,000 guaranteed in 7 days. Limited seats. Contact immediately.")
        self.assertEqual(r["level"], "high")
    def test_hindi(self):
        r = analyze("पक्का मुनाफ़ा! पैसे दोगुना, तुरंत ग्रुप में जुड़ें, सेबी पंजीकृत")
        self.assertIn(r["level"], ("medium", "high"))
    def test_benign(self):
        self.assertEqual(analyze("Your SIP of Rs 5000 for this month was processed.")["level"], "low")
    def test_fake_sebi_link(self):
        r = analyze("Verify now: http://sebi-check.xyz/login")
        self.assertTrue(any(s["id"] == "url" for s in r["signals"]))
    def test_risk_stats(self):
        r = analyze("Invest ₹10,000 today and get ₹50,000 guaranteed in 7 days. Join our VIP group: https://bit.ly/xyz")
        self.assertGreater(r["score"], 0)
        self.assertGreaterEqual(r["stats"]["signal_count"], 1)
        self.assertGreaterEqual(r["stats"]["link_count"], 1)
    def test_categories(self):
        r = analyze("Limited seats. Contact immediately. Get guaranteed profit in 7 days.")
        self.assertIn("urgency", r["categories"])
        self.assertIn("guaranteed", r["categories"])
if __name__ == "__main__":
    unittest.main()
