namespace TwoLineElements.Exceptions
{
    using System;

#pragma warning disable RCS1194 // Implement exception constructors.
    public class ChecksumException : Exception
#pragma warning restore RCS1194 // Implement exception constructors.
    {
        public ChecksumException(int expected, int actual)
            : base($"Invalid checksum expected {expected} but get {actual}")
        {
            Expected = expected;
            Actual = actual;
        }

        public int Expected { get; }
        public int Actual { get; }
    }
}