import unittest
import cbapi


def test_cbapi():

    cbapi.set_key("fcc6d1909dmsha9e61b6e0048f1cp1b804ejsn16302603dc9a")  # hide it later

    print(">>", "MadlyRad Labs, Inc.", end=' ... \n')
    org = cbapi.get_org(name="MadlyRad Labs, Inc.")

    print(">>", "Ritwik Bhattacharya", end=' ... \n')
    ppl = cbapi.get_org(name="MadlyRad Labs, Inc.")

    # always should have info for valid symbols
    assert(org.shape[0] > 0)
    assert(ppl.shape[0] > 0)

    print("OK")


if __name__ == "__main__":
    test_cbapi()
