package uk.yetanother.tle;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

/*
 * @author Ashley Baker
 */
public class TwoLineElementValidatorTest {

    private static String VALID_HEADER = "POLAR                   ";
    private static String tleLine1 = "1 25544U 98067A   19026.44648441  .00002471  00000-0  46032-4 0  999";
    private static int tleLine1Checksum = 6;
    private static String tleLine2 = "2 25544  51.6426 346.1706 0004731 317.4654 142.0482 15.5318491515323";
    private static int tleLine2Checksum = 5;

    @Test
    public void checkChecksumValidation() {
        assertEquals("TLE Line expected to be valid", true, TwoLineElementValidator.isLineChecksumValid(tleLine1 + tleLine1Checksum));
        assertEquals("TLE Line expected to be invalid", false, TwoLineElementValidator.isLineChecksumValid(tleLine1 + 0));
        assertEquals("TLE Line expected to be invalid", false, TwoLineElementValidator.isLineChecksumValid(null));
        assertEquals("TLE Line expected to be invalid", false, TwoLineElementValidator.isLineChecksumValid(""));
    }

    @Test
    public void checkInvalidDataValidation() {
        assertEquals("TLE data expected to be valid", true, TwoLineElementValidator.isDataValid(VALID_HEADER, tleLine1 + tleLine1Checksum, tleLine2 + tleLine2Checksum));
        assertEquals("TLE data expected to be invalid", false, TwoLineElementValidator.isDataValid(VALID_HEADER, tleLine1 + 0, tleLine2 + tleLine2Checksum));
        assertEquals("TLE data expected to be invalid", false, TwoLineElementValidator.isDataValid(VALID_HEADER, tleLine1 + tleLine1Checksum, tleLine2 + 0));
    }

    @Test
    public void checkInvalidDataLengths() {
        assertEquals("TLE data expected to be invalid", false, TwoLineElementValidator.isDataValid(VALID_HEADER, tleLine1, tleLine2 + tleLine2Checksum));
        assertEquals("TLE data expected to be invalid", false, TwoLineElementValidator.isDataValid(VALID_HEADER, tleLine1 + tleLine1Checksum, tleLine2));
    }

}
