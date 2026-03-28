namespace TwoLineElements.Models
{
    using System;

    public class Line1Model
    {
        /// <summary>
        ///     Line number
        /// </summary>
        public int Line { get; set; }

        /// <summary>
        ///     <a href="https://en.wikipedia.org/wiki/Satellite_Catalog_Number">Satellite Catalog Number</a>
        /// </summary>
        public double Number { get; set; }

        /// <summary>
        ///     Classification
        /// </summary>
        /// <seealso cref="Classification" />
        public Classification Classification { get; set; }

        /// <summary>
        ///     <a href="https://en.wikipedia.org/wiki/International_Designator">See International Designator</a>
        ///     <list type="bullet">
        ///         <item>
        ///             <description>last two digits of launch year</description>
        ///         </item>
        ///         <item>
        ///             <description>launch number of the year</description>
        ///         </item>
        ///         <item>
        ///             <description>piece of the launch</description>
        ///         </item>
        ///     </list>
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        ///     Launch date
        /// </summary>
        public DateTime Date { get; set; }

        /// <summary>
        ///     First derivative of mean motion; the ballistic coefficient
        ///     <a href="https://en.wikipedia.org/wiki/Mean_motion">See Mean Motion</a>
        ///     <a
        ///         href="https://web.archive.org/web/20000301052035/http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html">
        ///         See
        ///         tle def
        ///     </a>
        /// </summary>
        public double FirstDerivativeMeanMotion { get; set; }

        /// <summary>
        ///     Second derivative of mean motion (decimal point assumed)
        ///     <a href="https://en.wikipedia.org/wiki/Mean_motion">See Mean Motion</a>
        ///     <a
        ///         href="https://web.archive.org/web/20000301052035/http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html">
        ///         See
        ///         tle def
        ///     </a>
        /// </summary>
        public double SecondDerivativeMeanMotion { get; set; }

        /// <summary>
        ///     B*, the drag term, or radiation pressure coefficient (decimal point assumed)
        ///     <a href="https://en.wikipedia.org/wiki/BSTAR">See BSTAR</a>
        /// </summary>
        public double DragTermRadiationPressure { get; set; }

        /// <summary>
        ///     Ephemeris type (always zero; only used in undistributed Tle data)
        /// </summary>
        public int EphemerisType { get; set; }

        /// <summary>
        ///     Element set number. Incremented when a new Tle is generated for this object.
        /// </summary>
        public int ElementSetNumber { get; set; }
    }
}