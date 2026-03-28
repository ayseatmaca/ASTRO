package uk.yetanother.tle.model;

/**
 * The Interface TwoLineElementFile - Holds all the parameters parsed from TLE data.
 * 
 * @author Ashley Baker
 */
public interface TwoLineElementFile {

    /**
     * Gets the satellite name.
     *
     * @return the satellite name
     */
    public String getSatelliteName();

    /**
     * Gets the header.
     *
     * @return the header
     */
    public String getHeader();

    /**
     * Gets the satellite number.
     *
     * @return the satellite number
     */
    public int getSatelliteNumber();

    /**
     * Gets the satellite classification.
     *
     * @return the satellite classification
     */
    public String getSatelliteClassification();

    /**
     * Gets the international designator launch year.
     *
     * @return the international designator launch year
     */
    public String getInternationalDesignatorLaunchYear();

    /**
     * Gets the international designator launch number.
     *
     * @return the international designator launch number
     */
    public String getInternationalDesignatorLaunchNumber();

    /**
     * Gets the international designator launch item.
     *
     * @return the international designator launch item
     */
    public String getInternationalDesignatorLaunchItem();

    /**
     * Gets the epoch year.
     *
     * @return the epoch year
     */
    public String getEpochYear();

    /**
     * Gets the epoch day.
     *
     * @return the epoch day
     */
    public float getEpochDay();

    /**
     * Gets the first time derivative.
     *
     * @return the first time derivative
     */
    public float getFirstTimeDerivative();

    /**
     * Gets the second time derivative.
     *
     * @return the second time derivative
     */
    public float getSecondTimeDerivative();

    /**
     * Gets the bstar drag term.
     *
     * @return the bstar drag term
     */
    public float getBstarDragTerm();

    /**
     * Gets the element set number.
     *
     * @return the element set number
     */
    public int getElementSetNumber();

    /**
     * Gets the line one checksum.
     *
     * @return the line one checksum
     */
    public int getLineOneChecksum();

    /**
     * Gets the line one.
     *
     * @return the line one
     */
    public String getLineOne();

    /**
     * Gets the inclination.
     *
     * @return the inclination
     */
    public float getInclination();

    /**
     * Gets the right ascension.
     *
     * @return the right ascension
     */
    public float getRightAscension();

    /**
     * Gets the eccentricity.
     *
     * @return the eccentricity
     */
    public float getEccentricity();

    /**
     * Gets the argument of perigee.
     *
     * @return the argument of perigee
     */
    public float getArgumentOfPerigee();

    /**
     * Gets the mean anomaly.
     *
     * @return the mean anomaly
     */
    public float getMeanAnomaly();

    /**
     * Gets the mean motion.
     *
     * @return the mean motion
     */
    public float getMeanMotion();

    /**
     * Gets the revolution number.
     *
     * @return the revolution number
     */
    public int getRevolutionNumber();

    /**
     * Gets the line two checksum.
     *
     * @return the line two checksum
     */
    public int getLineTwoChecksum();

    /**
     * Gets the line two.
     *
     * @return the line two
     */
    public String getLineTwo();
}
