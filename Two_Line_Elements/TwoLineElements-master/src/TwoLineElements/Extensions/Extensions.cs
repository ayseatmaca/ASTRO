namespace TwoLineElements.Extensions
{
    using System;

    internal static class Extensions
    {
        public static ReadOnlySpan<char> FromRight(this ReadOnlySpan<char> value, int index)
        {
            return value.Slice(value.Length - index, index);
        }

        /// <summary>
        ///     Columns from string 1 based index
        /// </summary>
        /// <param name="value"></param>
        /// <param name="from"></param>
        /// <param name="to"></param>
        /// <returns></returns>
        public static ReadOnlySpan<char> Columns(this ReadOnlySpan<char> value, int from, int to)
        {
            if (from < 1)
            {
                throw new ArgumentOutOfRangeException(nameof(from));
            }

            return value.Slice(from - 1, to - from + 1);
        }
    }
}