package uk.yetanother.tle;

/**
 * TwoLineElementConstants - Holds the location of TLE parameters within the
 * encoded TLE lines of data. This is used to substring in the Parser and
 * Validator. Also includes other required static parameters.
 * 
 * @author Ashley Baker
 */
public final class TwoLineElementConstants {

    /**
     * Private and unused constructor.
     */
    private TwoLineElementConstants() {
    }

    /** The start offset for the classification parameter. */
    public static int CLASSIFICATION_START = 7;

    /** The end offset for the classification parameter. */
    public static int CLASSIFICATION_END = 8;

    /** The start offset for the launch year parameter. */
    public static int LAUNCH_YEAR_START = 9;

    /** The end offset for the launch year parameter. */
    public static int LAUNCH_YEAR_END = 11;

    /** The start offset for the launch number parameter. */
    public static int LAUNCH_NUMBER_START = 11;

    /** The end offset for the launch number parameter. */
    public static int LAUNCH_NUMBER_END = 14;

    /** The start offset for the launch item parameter. */
    public static int LAUNCH_ITEM_START = 14;

    /** The end offset for the launch item parameter. */
    public static int LAUNCH_ITEM_END = 15;

    /** The start offset for the epoch year parameter. */
    public static int EPOCH_YEAR_START = 18;

    /** The end offset for the epoch year parameter. */
    public static int EPOCH_YEAR_END = 20;

    /** The start offset for the epoch day parameter. */
    public static int EPOCH_DAY_START = 20;

    /** The end offset for the epoch day parameter. */
    public static int EPOCH_DAY_END = 32;

    /** The start offset for the first time derivative parameter. */
    public static int FIRST_TIME_DERIVATIVE_START = 33;

    /** The end offset for the first time derivative parameter. */
    public static int FIRST_TIME_DERIVATIVE_END = 42;

    /** The start offset for the second time derivative parameter. */
    public static int SECOND_TIME_DERIVATIVE_START = 44;

    /** The end offset for the second time derivative  parameter. */
    public static int SECOND_TIME_DERIVATIVE_END = 52;

    /** The start offset for the bstar drag term parameter. */
    public static int BSTAR_DRAG_TERM_START = 54;

    /** The end offset for the bstar drag term parameter. */
    public static int BSTAR_DRAG_TERM_END = 62;

    /** The start offset for the element set number parameter. */
    public static int ELEMENT_SET_NUMBER_START = 65;

    /** The end offset for the element set number parameter. */
    public static int ELEMENT_SET_NUMBER_END = 68;

    /** The start offset for the inclination parameter. */
    public static int INCLINATION_START = 8;

    /** The end offset for the inclination parameter. */
    public static int INCLINATION_END = 16;

    /** The start offset for the right ascension parameter. */
    public static int RIGHT_ASCENSION_START = 17;

    /** The end offset for the right ascension parameter. */
    public static int RIGHT_ASCENSION_END = 25;

    /** The start offset for the eccentricity parameter. */
    public static int ECCENTRICITY_START = 26;

    /** The end offset for the eccentricity parameter. */
    public static int ECCENTRICITY_END = 33;

    /** The start offset for the argument of perigee parameter. */
    public static int ARGUMENT_OF_PERIGEE_START = 34;

    /** The end offset for the argument of perigee parameter. */
    public static int ARGUMENT_OF_PERIGEE_END = 42;

    /** The start offset for the mean anomaly parameter. */
    public static int MEAN_ANOMALY_START = 43;

    /** The end offset for the mean anomaly parameter. */
    public static int MEAN_ANOMALY_END = 51;

    /** The start offset for the mean motion parameter. */
    public static int MEAN_MOTION_START = 52;

    /** The end offset for the mean motion parameter. */
    public static int MEAN_MOTION_END = 62;

    /** TThe start offset for the revolution number parameter. */
    public static int REVOLUTION_NUMBER_START = 63;

    /** The end offset for the revolution number parameter. */
    public static int REVOLUTION_NUMBER_END = 68;

    /** TThe start offset for the satellite number parameter. */
    public static int SATELLITE_NUMBER_START = 2;

    /** The end offset for the satellite number parameter. */
    public static int SATELLITE_NUMBER_END = 7;

    /** TThe start offset for the checksum parameter. */
    public static int CHECKSUM_START = 68;

    /** TThe end offset for the checksum parameter. */
    public static int CHECKSUM_END = 69;

    /** The length of a TLE header. */
    public static int HEADER_LENGTH = 24;

    /** The length of a TLE data line. */
    public static int LINE_LENGTH = 69;
}
