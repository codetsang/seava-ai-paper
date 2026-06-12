export default function FigureImage({ src, alt, caption }) {
  return (
    <figure>
      <div className="figure-photo">
        <img src={src} alt={alt} className="figure-img" loading="lazy" />
      </div>
      {caption && <figcaption>{caption}</figcaption>}
    </figure>
  )
}
