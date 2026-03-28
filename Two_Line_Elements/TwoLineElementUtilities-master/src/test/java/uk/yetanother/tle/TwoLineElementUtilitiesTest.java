package uk.yetanother.tle;

import static org.junit.Assert.*;

import org.junit.Test;

/*
 * @author Ashley Baker
 */
public class TwoLineElementUtilitiesTest {

    private static String tleLine1 = "1 25544U 98067A   19026.44648441  .00002471  00000-0  46032-4 0  999";
    private static int tleLine1Checksum = 6;
    private static String tleLine2 = "2 25544  51.6426 346.1706 0004731 317.4654 142.0482 15.5318491515323";
    private static int tleLine2Checksum = 5;

    @Test
    public void validateChecksumGeneration() {
        assertEquals("Invalid Checksum Generated", tleLine1Checksum, TwoLineElementUtilities.generateLineChecksum(tleLine1));
        assertEquals("Invalid Checksum Generated", tleLine2Checksum, TwoLineElementUtilities.generateLineChecksum(tleLine2));
    }
}
