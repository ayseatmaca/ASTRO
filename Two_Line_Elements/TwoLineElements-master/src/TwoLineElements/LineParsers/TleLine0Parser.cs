namespace TwoLineElements.LineParsers
{
    using System;

    /// <summary>
    ///     Parse first 1 (or 0) line contains name
    ///     char [24]
    /// </summary>
    public static class TleLine0Parser
    {
        /// <summary>
        ///     Parse line 0 Tle
        /// </summary>
        /// <param name="line0">line length less than 24</param>
        /// <returns>Satellite name</returns>
        /// <exception cref="ArgumentNullException"></exception>
        /// <exception cref="ArgumentOutOfRangeException"></exception>
        public static string Parse(string line0)
        {
            if (string.IsNullOrEmpty(line0))
            {
                throw new ArgumentNullException(nameof(line0), @"line0 can't be empty");
            }

            if (line0.Length > 24)
            {
                throw new ArgumentOutOfRangeException(nameof(line0), @"line0 exceeds 24 chars");
            }

            return line0.Trim();
        }
    }
}