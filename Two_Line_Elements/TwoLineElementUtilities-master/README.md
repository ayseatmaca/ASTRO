# Two Line Element Utilities
Provides an easy way to parse Two Line Element (TLE) files or strings. The data's length and checksums are verified when parsed and a TwoLineElementFile class is returned providing getters for all the data's parameters.  

## Getting Started

Two Line Element Utilities is provided as a pre-built maven library that requires no additional libraries to work. To parse TLE data simply provide either a BufferedReader of your TLE file or data as String's as shown below.

With a BufferedReader;
```java
public void parseData() {
String tleFilename = "ISS_Ephemeris.tle";
BufferedReader reader;
try {
    reader = new BufferedReader(new FileReader(tleFilename));
} catch (FileNotFoundException e) {
    e.printStackTrace();
}

TwoLineElementFile tleData = TwoLineElementParser.parseData(reader);
System.out.println(tleData.getSatelliteName());
}
```

With Strings;
```java
public void parseData() {
String header = "POLAR                   ";
String line1 = "1 23802U 96013A   19039.48429579  .00000202  00000-0  00000+0 0  9997";
String line2 = "2 23802  78.6744 257.3784 6839111 299.9661   9.8350  1.29844754109964";

TwoLineElementFile tleData = TwoLineElementParser.parseData(header, line1, line2);
System.out.println(tleData.getSatelliteName());
}
```

With the TwoLineElementFile returned from the Parser you can call the appropriate getter to return the parameters you require.
### Maven

To start using Two Line Element Utilities simply add the following dependency to your project POM.

```xml
<dependency>
	<groupId>uk.yetanother</groupId>
	<artifactId>TwoLineElementUtilities</artifactId>
	<version>0.0.1</version>
</dependency>
```

## Built With

* [Maven](https://maven.apache.org/) - Dependency Management

## Authors

* **Ashley Baker** - (https://github.com/ashleycbaker)

## License

This project is licensed under Apache License, Version 2.0 - see the [LICENSE.md](LICENSE.md) file for details
