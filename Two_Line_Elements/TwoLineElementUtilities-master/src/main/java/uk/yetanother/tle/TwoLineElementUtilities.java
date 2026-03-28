package uk.yetanother.tle;

/**
 * TwoLineElementUtilities - Common methods to support TLE parser and validator functions..
 * 
 * @author Ashley Baker
 */
public final class TwoLineElementUtilities {

    /**
     * Private and unused constructor.
     */
    private TwoLineElementUtilities() {
    }

    /**
     * Generates the checksum for a given TLE data line.
     *
     * @param line the TLE data line to generate a checksum for.
     * @return the int - the checksum calculated.
     */
    public static int generateLineChecksum(String line) {
        String checksumLine = line;
        checksumLine = checksumLine.replaceAll("[A-Za-z+\\. ]", "0");
        checksumLine = checksumLine.replaceAll("[-]", "1");

        int checksum = 0;
        for (char digit : checksumLine.toCharArray()) {
            checksum = checksum + Character.getNumericValue(digit);
        }
        return checksum % 10;
    }
}
