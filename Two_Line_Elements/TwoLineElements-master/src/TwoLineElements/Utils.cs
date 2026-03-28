namespace TwoLineElements
{
    using System;
    using System.Globalization;
    using System.Text.RegularExpressions;
    using Exceptions;
    using Extensions;

    internal static class Utils
    {
        /// <summary>
        ///     Checksum Calculate according https://en.wikipedia.org/wiki/Two-line_element_set
        /// </summary>
        /// <param name="line"></param>
        /// <param name="expected">expected checksum from 68-69 line position</param>
        /// <returns></returns>
        public static void Checksum(ReadOnlySpan<char> line, int expected)
        {
            var chak = Checksum(line);
            if (chak != expected)
            {
                throw new ChecksumException(expected, chak);
            }
        }

        public static int Checksum(ReadOnlySpan<char> line)
        {
            var sum = 0;
            foreach (var c in line.Slice(0, 68))
            {
                if (c == '-')
                {
                    sum++;
                }
                else if (char.IsDigit(c))
                {
                    sum += (byte) char.GetNumericValue(c);
                }
            }

            return sum % 10;
        }

        public static int ParseIntValue(ReadOnlySpan<char> value)
        {
            return Convert.ToInt32(value.ToString());
        }

        public static double ParseDoubleValue(ReadOnlySpan<char> value)
        {
            var pattern = @"([-])?([\.\d]+)([+-]\d+)?";
            var r = new Regex(pattern);
            var match = r.Match(value.ToString());
            return Convert.ToDouble(match.Value, CultureInfo.InvariantCulture);
        }

        public static double ParseFloatValue(ReadOnlySpan<char> value)
        {
            var val1 = value.Columns(1, 1).ToString();
            var val2 = value.Slice(1, value.Length - 3).ToString();
            var val3 = value.FromRight(2).ToString();
            var val = val1 + '.' + val2 + 'e' + val3;
            return Convert.ToDouble(val, CultureInfo.InvariantCulture);
        }

        public static DateTime JulianToDateTimeUtc(ReadOnlySpan<char> dateLine)
        {
            if (dateLine == null || dateLine.Length != 14)
            {
                throw new IndexOutOfRangeException("Julian date format need to be exactly 14 chars");
            }

            var epoch = ParseIntValue(dateLine.Slice(0, 2));
            var days = ParseDoubleValue(dateLine.Slice(2));

            var year = DateTime.Now.Year;
            var currentEpoch = year % 100;
            var century = year - currentEpoch;
            year = epoch > currentEpoch + 1 ? century - 100 + epoch : century + epoch;

            var day = (int) Math.Floor(days);
            var hours = 24 * (days - day);
            var hour = (int) Math.Floor(hours);
            var minutes = 60 * (hours - hour);
            var minute = (int) Math.Floor(minutes);
            var seconds = 60 * (minutes - minute);
            var second = (int) Math.Floor(seconds);
            var millSeconds = 1000 * (seconds - second);

            var date = new DateTime(year, 1, 1, hour, minute, second) + TimeSpan.FromDays(day) +
                       TimeSpan.FromMilliseconds(millSeconds);
            return DateTime.SpecifyKind(date.AddDays(-1), DateTimeKind.Utc);
        }
    }
}