namespace TwoLineElements.LineParsers
{
    using System;
    using Extensions;
    using Models;

    public static class TleLine2Parser
    {
        /// <summary>
        ///     Parse second line of Tle
        /// </summary>
        /// <param name="line2"></param>
        /// <returns>
        ///     <see cref="Line2Model" />
        /// </returns>
        /// <exception cref="ArgumentNullException"></exception>
        /// <exception cref="ArgumentOutOfRangeException"></exception>
        public static Line2Model Parse(ReadOnlySpan<char> line2)
        {
            if (line2 == null || line2.Length < 1)
            {
                throw new ArgumentNullException(nameof(line2), @"line1 can't be empty");
            }

            if (line2.Length > 69)
            {
                throw new ArgumentOutOfRangeException(nameof(line2), @"line0 exceeds 69 chars");
            }

            var checkSum = Convert.ToInt32(line2.Slice(68, 1).ToString());
            Utils.Checksum(line2, checkSum);

            var result = new Line2Model
            {
                Line = Utils.ParseIntValue(line2.Columns(1, 1)),
                Number = Utils.ParseDoubleValue(line2.Columns(3, 7)),
                Inclination = Utils.ParseDoubleValue(line2.Columns(9, 16)),
                Ascension = Utils.ParseDoubleValue(line2.Columns(18, 25)),
                Eccentricity = Utils.ParseDoubleValue(line2.Columns(27, 33)),
                Perigee = Utils.ParseDoubleValue(line2.Columns(35, 42)),
                Anomaly = Utils.ParseDoubleValue(line2.Columns(44, 51)),
                Motion = Utils.ParseDoubleValue(line2.Columns(53, 63)),
                Revolution = Utils.ParseDoubleValue(line2.Columns(64, 68))
            };

            return result;
        }
    }
}