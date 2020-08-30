import unittest
import cbapi


def test_cbapi():

    cbapi.set_key(<YOUR_RAPIDAPI_KEY>)

    print(">>", "MadlyRad Labs, Inc.", end=' ... \n')
    org = cbapi.get_org(name="MadlyRad Labs, Inc.")

    print(">>", "Ritwik Bhattacharya", end=' ... \n')
    ppl = cbapi.get_ppl(name="MadlyRad Labs, Inc.")

    # always should have info for valid symbols
    assert(org.shape[0] > 0)
    assert(ppl.shape[0] > 0)

    print("OK")


if __name__ == "__main__":
    test_cbapi()
