package uk.yetanother.tle.model;

/**
 * TwoLineElementFileImpl - Holds all the parameters parsed from TLE data.
 * 
 * @author Ashley Baker
 */
public class TwoLineElementFileImpl implements TwoLineElementFile {

    /** The header. */
    private String header;
    
    /** The line one. */
    private String lineOne;
    
    /** The line two. */
    private String lineTwo;

    /** The satellite name. */
    private String satelliteName;
    
    /** The satellite number. */
    private int satelliteNumber;
    
    /** The Satellite classification. */
    private String SatelliteClassification;
    
    /** The international designator launch year. */
    private String internationalDesignatorLaunchYear;
    
    /** The international designator launch number. */
    private String internationalDesignatorLaunchNumber;
    
    /** The international designator launch item. */
    private String internationalDesignatorLaunchItem;
    
    /** The epoch year. */
    private String epochYear;
    
    /** The epoch day. */
    private float epochDay;
    
    /** The first time derivative. */
    private float firstTimeDerivative;
    
    /** The second time derivative. */
    private float secondTimeDerivative;
    
    /** The bstar drag term. */
    private float bstarDragTerm;
    
    /** The element set number. */
    private int elementSetNumber;
    
    /** The line one checksum. */
    private int lineOneChecksum;
    
    /** The inclination. */
    private float inclination;
    
    /** The right ascension. */
    private float rightAscension;
    
    /** The eccentricity. */
    private float eccentricity;
    
    /** The argument of perigee. */
    private float argumentOfPerigee;
    
    /** The mean anomaly. */
    private float meanAnomaly;
    
    /** The mean motion. */
    private float meanMotion;
    
    /** The revolution number. */
    private int revolutionNumber;
    
    /** The line two checksum. */
    private int lineTwoChecksum;

    /**
     * Instantiates a new TwoLineElementFileImpl  - Holds all the parameters parsed from TLE data.
     *
     * @param header - A String of the TLE Header Line
     * @param lineOne - A String of the first line of TLE data 
     * @param lineTwo - A String of the second line of TLE data
     */
    public TwoLineElementFileImpl(String header, String lineOne, String lineTwo) {
        this.header = header;
        this.lineOne = lineOne;
        this.lineTwo = lineTwo;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getArgumentOfPerigee()
     */
    public float getArgumentOfPerigee() {
        return argumentOfPerigee;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getBstarDragTerm()
     */
    public float getBstarDragTerm() {
        return bstarDragTerm;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getEccentricity()
     */
    public float getEccentricity() {
        return eccentricity;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getElementSetNumber()
     */
    public int getElementSetNumber() {
        return elementSetNumber;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getEpochDay()
     */
    public float getEpochDay() {
        return epochDay;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getEpochYear()
     */
    public String getEpochYear() {
        return epochYear;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getFirstTimeDerivative()
     */
    public float getFirstTimeDerivative() {
        return firstTimeDerivative;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getHeader()
     */
    public String getHeader() {
        return header;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getInclination()
     */
    public float getInclination() {
        return inclination;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getInternationalDesignatorLaunchItem()
     */
    public String getInternationalDesignatorLaunchItem() {
        return internationalDesignatorLaunchItem;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getInternationalDesignatorLaunchNumber()
     */
    public String getInternationalDesignatorLaunchNumber() {
        return internationalDesignatorLaunchNumber;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getInternationalDesignatorLaunchYear()
     */
    public String getInternationalDesignatorLaunchYear() {
        return internationalDesignatorLaunchYear;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getLineOne()
     */
    public String getLineOne() {
        return lineOne;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getLineOneChecksum()
     */
    public int getLineOneChecksum() {
        return lineOneChecksum;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getLineTwo()
     */
    public String getLineTwo() {
        return lineTwo;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getLineTwoChecksum()
     */
    public int getLineTwoChecksum() {
        return lineTwoChecksum;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getMeanAnomaly()
     */
    public float getMeanAnomaly() {
        return meanAnomaly;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getMeanMotion()
     */
    public float getMeanMotion() {
        return meanMotion;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getRevolutionNumber()
     */
    public int getRevolutionNumber() {
        return revolutionNumber;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getRightAscension()
     */
    public float getRightAscension() {
        return rightAscension;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getSatelliteClassification()
     */
    public String getSatelliteClassification() {
        return SatelliteClassification;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getSatelliteName()
     */
    public String getSatelliteName() {
        return satelliteName;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getSatelliteNumber()
     */
    public int getSatelliteNumber() {
        return satelliteNumber;
    }

    /* (non-Javadoc)
     * @see uk.yetanother.tle.model.TwoLineElementFile#getSecondTimeDerivative()
     */
    public float getSecondTimeDerivative() {
        return secondTimeDerivative;
    }

    /**
     * Sets the argument of perigee.
     *
     * @param argumentOfPerige the new argument of perigee
     */
    public void setArgumentOfPerigee(float argumentOfPerige) {
        this.argumentOfPerigee = argumentOfPerige;
    }

    /**
     * Sets the bstar drag term.
     *
     * @param bstarDragTerm the new bstar drag term
     */
    public void setBstarDragTerm(float bstarDragTerm) {
        this.bstarDragTerm = bstarDragTerm;
    }

    /**
     * Sets the eccentricity.
     *
     * @param eccentricity the new eccentricity
     */
    public void setEccentricity(float eccentricity) {
        this.eccentricity = eccentricity;
    }

    /**
     * Sets the element set number.
     *
     * @param elementSetNumber the new element set number
     */
    public void setElementSetNumber(int elementSetNumber) {
        this.elementSetNumber = elementSetNumber;
    }

    /**
     * Sets the epoch day.
     *
     * @param epochDay the new epoch day
     */
    public void setEpochDay(float epochDay) {
        this.epochDay = epochDay;
    }

    /**
     * Sets the epoch year.
     *
     * @param epochYear the new epoch year
     */
    public void setEpochYear(String epochYear) {
        this.epochYear = epochYear;
    }

    /**
     * Sets the first time derivative.
     *
     * @param firstTimeDerivative the new first time derivative
     */
    public void setFirstTimeDerivative(float firstTimeDerivative) {
        this.firstTimeDerivative = firstTimeDerivative;
    }

    /**
     * Sets the inclination.
     *
     * @param inclination the new inclination
     */
    public void setInclination(float inclination) {
        this.inclination = inclination;
    }

    /**
     * Sets the international designator launch item.
     *
     * @param internationalDesignatorLaunchItem the new international designator launch item
     */
    public void setInternationalDesignatorLaunchItem(String internationalDesignatorLaunchItem) {
        this.internationalDesignatorLaunchItem = internationalDesignatorLaunchItem;
    }

    /**
     * Sets the international designator launch number.
     *
     * @param internationalDesignatorLaunchNumber the new international designator launch number
     */
    public void setInternationalDesignatorLaunchNumber(String internationalDesignatorLaunchNumber) {
        this.internationalDesignatorLaunchNumber = internationalDesignatorLaunchNumber;
    }

    /**
     * Sets the international designator launch year.
     *
     * @param internationalDesignatorLaunchYear the new international designator launch year
     */
    public void setInternationalDesignatorLaunchYear(String internationalDesignatorLaunchYear) {
        this.internationalDesignatorLaunchYear = internationalDesignatorLaunchYear;
    }

    /**
     * Sets the line one checksum.
     *
     * @param lineOneChecksum the new line one checksum
     */
    public void setLineOneChecksum(int lineOneChecksum) {
        this.lineOneChecksum = lineOneChecksum;
    }

    /**
     * Sets the line two checksum.
     *
     * @param lineTwoChecksum the new line two checksum
     */
    public void setLineTwoChecksum(int lineTwoChecksum) {
        this.lineTwoChecksum = lineTwoChecksum;
    }

    /**
     * Sets the mean anomaly.
     *
     * @param meanAnomaly the new mean anomaly
     */
    public void setMeanAnomaly(float meanAnomaly) {
        this.meanAnomaly = meanAnomaly;
    }

    /**
     * Sets the mean motion.
     *
     * @param meanMotion the new mean motion
     */
    public void setMeanMotion(float meanMotion) {
        this.meanMotion = meanMotion;
    }

    /**
     * Sets the revolution number.
     *
     * @param revolutionNumber the new revolution number
     */
    public void setRevolutionNumber(int revolutionNumber) {
        this.revolutionNumber = revolutionNumber;
    }

    /**
     * Sets the right ascension.
     *
     * @param rightAscension the new right ascension
     */
    public void setRightAscension(float rightAscension) {
        this.rightAscension = rightAscension;
    }

    /**
     * Sets the satellite classification.
     *
     * @param satelliteClassification the new satellite classification
     */
    public void setSatelliteClassification(String satelliteClassification) {
        SatelliteClassification = satelliteClassification;
    }

    /**
     * Sets the satellite name.
     *
     * @param satelliteName the new satellite name
     */
    public void setSatelliteName(String satelliteName) {
        this.satelliteName = satelliteName;
    }

    /**
     * Sets the satellite number.
     *
     * @param satelliteNumber the new satellite number
     */
    public void setSatelliteNumber(int satelliteNumber) {
        this.satelliteNumber = satelliteNumber;
    }

    /**
     * Sets the second time derivative.
     *
     * @param secondTimeDerivative the new second time derivative
     */
    public void setSecondTimeDerivative(float secondTimeDerivative) {
        this.secondTimeDerivative = secondTimeDerivative;
    }

    /* (non-Javadoc)
     * @see java.lang.Object#toString()
     */
    @Override
    public String toString() {
        return header + "\n" + lineOne + "\n" + lineTwo;
    }
}
