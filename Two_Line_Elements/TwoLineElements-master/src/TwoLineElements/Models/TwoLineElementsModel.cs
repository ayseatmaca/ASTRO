namespace TwoLineElements.Models
{
    using LineParsers;

    public class TwoLineElementsModel
    {
        /// <summary>
        ///     Satellite name
        /// </summary>
        /// <seealso cref="TleLine0Parser" />
        public string Name { get; set; } = string.Empty;

        /// <summary>
        ///     <see cref="Line1Model" />
        ///     <see cref="TleLine1Parser" />
        /// </summary>
        public Line1Model Line1 { get; set; }

        /// <summary>
        ///     <see cref="Line2Model" />
        ///     <see cref="TleLine2Parser" />
        /// </summary>
        public Line2Model Line2 { get; set; }
    }
}