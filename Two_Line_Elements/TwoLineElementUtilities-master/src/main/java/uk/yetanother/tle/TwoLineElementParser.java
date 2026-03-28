package uk.yetanother.tle;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

import uk.yetanother.tle.exception.InvalidInputFileException;
import uk.yetanother.tle.model.TwoLineElementFile;
import uk.yetanother.tle.model.TwoLineElementFileImpl;

/**
 * TwoLineElementParser - This Parser takes a BufferReader of a TLE file or the
 * three TLE lines as Strings. In return a TwoLineElementFile class is returned
 * providing getters for the TLE parameters.
 * 
 * @author Ashley Baker
 *
 */
public final class TwoLineElementParser {

    /** The logger. */
    private static Logger LOGGER = Logger.getLogger(TwoLineElementParser.class.getName());

    /**
     * Private and unused constructor.
     */
    private TwoLineElementParser() {
    }

    /**
     * Parses a TLE File provided as a BufferedReader.
     *
     * @param inputFile TLE file as a BufferedReader 
     * @return TwoLineElementFile class providing getters for the TLE parameters
     * @throws InvalidInputFileException Thrown if there is an IOException while using the BufferedReader.
     */
    public static TwoLineElementFile parseData(BufferedReader inputFile) throws InvalidInputFileException {
        if (inputFile == null) {
            throw new InvalidInputFileException("The provided input file was null.");
        }

        try {
            String header = inputFile.readLine();
            String lineOne = inputFile.readLine();
            String lineTwo = inputFile.readLine();
            return parseData(header, lineOne, lineTwo);
        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, "Unable to read the required lines from the provided input file.", e);
            throw new InvalidInputFileException("Unable to read the required lines from the provided input file.", e);
        }
    }

    /**
     * Parses a TLE File provided as Strings. One for each line of TLE data.
     *
     * @param header A String of the TLE Header Line
     * @param lineOne A String of the first line of TLE data 
     * @param lineTwo A String of the second line of TLE data 
     * @return TwoLineElementFile class providing getters for the TLE parameters
     */
    public static TwoLineElementFile parseData(String header, String lineOne, String lineTwo) {
        return TwoLineElementValidator.isDataValid(header, lineOne, lineTwo) ? createAndPopulateTLE(header, lineOne, lineTwo) : null;
    }

    /**
     * Creates the and populates the TwoLineElementFile class to be returned.
     *
     * @param header A String of the TLE Header Line
     * @param lineOne A String of the first line of TLE data 
     * @param lineTwo A String of the second line of TLE data 
     * @return TwoLineElementFile class providing getters for the TLE parameters
     */
    private static TwoLineElementFile createAndPopulateTLE(String header, String lineOne, String lineTwo) {
        TwoLineElementFileImpl tleFile = new TwoLineElementFileImpl(header, lineOne, lineTwo);
        parseHeader(header, tleFile);
        parseLineOne(lineOne, tleFile);
        parseLineTwo(lineTwo, tleFile);
        return tleFile;
    }

    /**
     * Parses the header data into the TwoLineElementFile class to be returned.
     *
     * @param header A String of the TLE Header Line
     * @param file TwoLineElementFile to update with parameters from the header data
     */
    private static void parseHeader(String header, TwoLineElementFileImpl file) {
        file.setSatelliteName(header.trim());
    }

    /**
     * Parses line one TLE data into the TwoLineElementFile class to be returned.
     *
     * @param lineOne A String of line one TLE data
     * @param file TwoLineElementFile to update with parameters from the line one data
     */
    private static void parseLineOne(String lineOne, TwoLineElementFileImpl file) {
        file.setSatelliteNumber(Integer.valueOf(lineOne.substring(TwoLineElementConstants.SATELLITE_NUMBER_START, TwoLineElementConstants.SATELLITE_NUMBER_END).trim()));
        file.setSatelliteClassification(lineOne.substring(TwoLineElementConstants.CLASSIFICATION_START, TwoLineElementConstants.CLASSIFICATION_END));
        file.setInternationalDesignatorLaunchYear(lineOne.substring(TwoLineElementConstants.LAUNCH_YEAR_START, TwoLineElementConstants.LAUNCH_YEAR_END));
        file.setInternationalDesignatorLaunchNumber(lineOne.substring(TwoLineElementConstants.LAUNCH_NUMBER_START, TwoLineElementConstants.LAUNCH_NUMBER_END));
        file.setInternationalDesignatorLaunchItem(lineOne.substring(TwoLineElementConstants.LAUNCH_ITEM_START, TwoLineElementConstants.LAUNCH_ITEM_END));
        file.setEpochYear(lineOne.substring(TwoLineElementConstants.EPOCH_YEAR_START, TwoLineElementConstants.EPOCH_YEAR_END));
        file.setEpochDay(Float.valueOf(lineOne.substring(TwoLineElementConstants.EPOCH_DAY_START, TwoLineElementConstants.EPOCH_DAY_END)));
        file.setFirstTimeDerivative(Float.valueOf(lineOne.substring(TwoLineElementConstants.FIRST_TIME_DERIVATIVE_START, TwoLineElementConstants.FIRST_TIME_DERIVATIVE_END)));
        file.setSecondTimeDerivative(parseFloatWithExponent(lineOne.substring(TwoLineElementConstants.SECOND_TIME_DERIVATIVE_START, TwoLineElementConstants.SECOND_TIME_DERIVATIVE_END)));
        file.setBstarDragTerm(parseFloatWithExponent(lineOne.substring(TwoLineElementConstants.BSTAR_DRAG_TERM_START, TwoLineElementConstants.BSTAR_DRAG_TERM_END)));
        file.setElementSetNumber(Integer.valueOf(lineOne.substring(TwoLineElementConstants.ELEMENT_SET_NUMBER_START, TwoLineElementConstants.ELEMENT_SET_NUMBER_END).trim()));
        file.setLineOneChecksum(Integer.valueOf(lineOne.substring(TwoLineElementConstants.CHECKSUM_START, TwoLineElementConstants.CHECKSUM_END).trim()));
    }

    /**
     * Parses line two TLE data into the TwoLineElementFile class to be returned.
     *
     * @param lineTwo A String of line two TLE data
     * @param file TwoLineElementFile to update with parameters from the line two data
     */
    private static void parseLineTwo(String lineTwo, TwoLineElementFileImpl file) {
        file.setInclination(Float.valueOf(lineTwo.substring(TwoLineElementConstants.INCLINATION_START, TwoLineElementConstants.INCLINATION_END)));
        file.setRightAscension(Float.valueOf(lineTwo.substring(TwoLineElementConstants.RIGHT_ASCENSION_START, TwoLineElementConstants.RIGHT_ASCENSION_END)));
        file.setEccentricity(parseFloatWithExponent(lineTwo.substring(TwoLineElementConstants.ECCENTRICITY_START, TwoLineElementConstants.ECCENTRICITY_END)));
        file.setArgumentOfPerigee(Float.valueOf(lineTwo.substring(TwoLineElementConstants.ARGUMENT_OF_PERIGEE_START, TwoLineElementConstants.ARGUMENT_OF_PERIGEE_END)));
        file.setMeanAnomaly(Float.valueOf(lineTwo.substring(TwoLineElementConstants.MEAN_ANOMALY_START, TwoLineElementConstants.MEAN_ANOMALY_END)));
        file.setMeanMotion(Float.valueOf(lineTwo.substring(TwoLineElementConstants.MEAN_MOTION_START, TwoLineElementConstants.MEAN_MOTION_END)));
        file.setRevolutionNumber(Integer.valueOf(lineTwo.substring(TwoLineElementConstants.REVOLUTION_NUMBER_START, TwoLineElementConstants.REVOLUTION_NUMBER_END).trim()));
        file.setLineTwoChecksum(Integer.valueOf(lineTwo.substring(TwoLineElementConstants.CHECKSUM_START, TwoLineElementConstants.CHECKSUM_END)));
    }

    /**
     * Parses a String that represents a float with exponent.
     *
     * @param stringToParse the String that represents a float with exponent
     * @return the float
     */
    private static float parseFloatWithExponent(String stringToParse) {
        String valueToParse = "0." + stringToParse.trim();
        valueToParse = valueToParse.replace("-", "E-");
        valueToParse = valueToParse.replace("+", "E+");
        return Float.valueOf(valueToParse);
    }
}
