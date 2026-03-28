package uk.yetanother.tle.exception;

/**
 * InvalidInputFileException - Used if TLE BufferedReader errors while parsing data.
 *
 * @author Ashley Baker
 */
public class InvalidInputFileException extends Exception {
    
    /** The Constant serialVersionUID. */
    private static final long serialVersionUID = -5073253000699895705L;

    /**
     * Instantiates a new InvalidInputFileException with a message and throwable.
     *
     * @param message the error message
     * @param e a throwable that was the root cause
     */
    public InvalidInputFileException(String message, Throwable e) {
        super(message, e);
    }

    /**
     * Instantiates a new InvalidInputFileException with a message.
     *
     * @param message the error message
     */
    public InvalidInputFileException(String message) {
        super(message);
    }
}
