package uk.yetanother.tle;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * TwoLineElementValidator - Used to validate TLE data that has been given to the parser.
 * 
 * @author Ashley Baker
 */
public final class TwoLineElementValidator {

    /** The logger. */
    private static Logger LOGGER = Logger.getLogger(TwoLineElementValidator.class.getName());

    /**
     * Private and unused constructor.
     */
    private TwoLineElementValidator() {
    }

    /**
     * Checks if the TLE data is valid or not.
     *
     * @param header A String of the TLE Header Line
     * @param lineOne A String of the first line of TLE data 
     * @param lineTwo A String of the second line of TLE data 
     * @return true, if data is valid
     */
    public static boolean isDataValid(String header, String lineOne, String lineTwo) {
        String errorMessages = validateLineLength(header, lineOne, lineTwo);
        errorMessages += isLineChecksumValid(lineOne) ? "" : "\nChecksum of line one is invalid.";
        errorMessages += isLineChecksumValid(lineTwo) ? "" : "\nChecksum of line two is invalid.";

        if (!errorMessages.isEmpty()) {
            LOGGER.log(Level.SEVERE, "TLE Data is invalid and cannot be parsed. " + errorMessages);
            return false;
        }
        return true;
    }

    /**
     * Checks if is line checksum valid or not.
     *
     * @param line the TLE data line to check the checksum on
     * @return true, if is line checksum is valid
     */
    public static boolean isLineChecksumValid(String line) {
        // If the line is null or is empty the checksum is invalid.
        if (line == null || line.isEmpty()) {
            return false;
        }

        int expectedChecksum = Character.getNumericValue(line.charAt(line.length() - 1));
        return expectedChecksum == TwoLineElementUtilities.generateLineChecksum(line.substring(0, line.length() - 1));
    }

    /**
     * Validate lengths of TLE lines.
     *
     * @param header A String of the TLE Header Line
     * @param lineOne A String of the first line of TLE data 
     * @param lineTwo A String of the second line of TLE data 
     * @return the string Returns a list of error messages to be logged, if no messages then no issues.
     */
    private static String validateLineLength(String header, String lineOne, String lineTwo) {
        String errorMessages = "";
        if (header.length() != TwoLineElementConstants.HEADER_LENGTH) {
            errorMessages += "\nThe header of the TLE Data is not the correct length, expected " + TwoLineElementConstants.HEADER_LENGTH + ".";
        }
        if (lineOne.length() != TwoLineElementConstants.LINE_LENGTH) {
            errorMessages += "\nThe first line of the TLE Data is not the correct length, expected " + TwoLineElementConstants.LINE_LENGTH + ".";
        }
        if (lineTwo.length() != TwoLineElementConstants.LINE_LENGTH) {
            errorMessages += "\nThe second line of the TLE Data is not the correct length, expected " + TwoLineElementConstants.LINE_LENGTH + ".";
        }
        return errorMessages;
    }

}
