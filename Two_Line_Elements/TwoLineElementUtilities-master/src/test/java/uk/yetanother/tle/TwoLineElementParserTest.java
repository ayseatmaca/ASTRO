package uk.yetanother.tle;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

import uk.yetanother.tle.exception.InvalidInputFileException;
import uk.yetanother.tle.model.TwoLineElementFile;

/*
 * @author Ashley Baker
 */
@RunWith(MockitoJUnitRunner.class)
public class TwoLineElementParserTest {
    
	private static String VALID_ISS_FILENAME = "/VALID_ISS.tle";
	
	private static String VALID_HEADER = "POLAR                   ";
	private static String VALID_LINE_ONE = "1 23802U 96013A   19039.48429579  .00000202  00000-0  00000+0 0  9997";
	private static String VALID_LINE_TWO = "2 23802  78.6744 257.3784 6839111 299.9661   9.8350  1.29844754109964";
	
	@Test
	public void parseValidDataFromFile() throws InvalidInputFileException {
		BufferedReader tleFile = new BufferedReader(new InputStreamReader(this.getClass().getResourceAsStream(VALID_ISS_FILENAME)));
		TwoLineElementFile tleData = TwoLineElementParser.parseData(tleFile);
		
		//Check Header
		assertEquals("Unexpected Satellite Name.", "ISS (ZARYA)", tleData.getSatelliteName());
		assertEquals("Unexpected Header.", "ISS (ZARYA)             ", tleData.getHeader());
		
		//Check Line One
		assertEquals("Unexpected Satellite Number.", 25544, tleData.getSatelliteNumber());
		assertEquals("Unexpected Satellite Classification.", "U", tleData.getSatelliteClassification());
		assertEquals("Unexpected Launch Year.", "98", tleData.getInternationalDesignatorLaunchYear());
		assertEquals("Unexpected Launch Number.", "067", tleData.getInternationalDesignatorLaunchNumber());
		assertEquals("Unexpected Launch Item.", "A", tleData.getInternationalDesignatorLaunchItem());
		assertEquals("Unexpected Epoch Year.", "19", tleData.getEpochYear());
		assertEquals("Unexpected Epoch Day.", Float.valueOf("26.44648441"), tleData.getEpochDay(), 0.00000001);
		assertEquals("Unexpected First Time Derivative.", Float.valueOf("0.00002471"), tleData.getFirstTimeDerivative(), 0.00000001);
		assertEquals("Unexpected Second Time Derivative.", Float.valueOf("0.00000E-0"), tleData.getSecondTimeDerivative(), 0.00000001);
		assertEquals("Unexpected BSTAR Drag Term.", Float.valueOf("0.46032E-4"), tleData.getBstarDragTerm(), 0.0000001);
		assertEquals("Unexpected Element Set Number.", 999, tleData.getElementSetNumber());
		assertEquals("Unexpected Line One Checksum.", 6, tleData.getLineOneChecksum());
		assertEquals("Unexpected Line One.", "1 25544U 98067A   19026.44648441  .00002471  00000-0  46032-4 0  9996", tleData.getLineOne());
		
		//Check Line Two
		assertEquals("Unexpected Inclination.", Float.valueOf("51.6426"), tleData.getInclination(), 0.0001);
		assertEquals("Unexpected Right Ascension.", Float.valueOf("346.1706"), tleData.getRightAscension(), 0.0001);
		assertEquals("Unexpected Eccentricity.", Float.valueOf("0.0004731"), tleData.getEccentricity(), 0.0000001);
		assertEquals("Unexpected Argument of Perigee.", Float.valueOf("317.4654"), tleData.getArgumentOfPerigee(), 0.0001);
		assertEquals("Unexpected Mean Anomaly.", Float.valueOf("142.0482"), tleData.getMeanAnomaly(), 0.0001);
		assertEquals("Unexpected Mean Motion.", Float.valueOf("15.53184915"), tleData.getMeanMotion(), 0.00000001);
		assertEquals("Unexpected Revolution Number.", 15323, tleData.getRevolutionNumber());
		assertEquals("Unexpected Line Two Checksum.", 5, tleData.getLineTwoChecksum());
		assertEquals("Unexpected Line Two.", "2 25544  51.6426 346.1706 0004731 317.4654 142.0482 15.53184915153235", tleData.getLineTwo());
		
		//Check toString()
		String expectedHeader = tleData.getHeader() + "\n" + tleData.getLineOne() + "\n" + tleData.getLineTwo();
		assertEquals("Unexpected toString().", expectedHeader,  tleData.toString());
	}
	
	@Test(expected = InvalidInputFileException.class)
	public void parseNullFile() throws InvalidInputFileException {
		TwoLineElementParser.parseData(null);
	}
	
	@Test(expected = InvalidInputFileException.class)
	public void parseEmptyFile() throws InvalidInputFileException, IOException {
		BufferedReader mockedReader = mock(BufferedReader.class);
		when(mockedReader.readLine()).thenThrow(new IOException());
		TwoLineElementParser.parseData(mockedReader);
	}
	
	@Test()
	public void testHeaderLengths() throws InvalidInputFileException {
		String shortHeader = "Short                  ";
		String longHeader = "Long                     ";
		
		assertEquals("Expected to be invalid.", null, TwoLineElementParser.parseData(shortHeader, VALID_LINE_ONE, VALID_LINE_TWO));
		assertEquals("Expected to be invalid.", null, TwoLineElementParser.parseData(longHeader, VALID_LINE_ONE, VALID_LINE_TWO));
		assertNotEquals("Expected to be valid", null, TwoLineElementParser.parseData(VALID_HEADER, VALID_LINE_ONE, VALID_LINE_TWO));
	}
}
