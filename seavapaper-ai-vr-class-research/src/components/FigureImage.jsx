export default function FigureImage({ src, alt, caption, half }) {
  return (
    <figure>
      <div className="figure-photo">
        <img
          src={src}
          alt={alt}
          className={half ? 'figure-img figure-img--half' : 'figure-img'}
          loading="lazy"
        />
      </div>
      {caption && <figcaption>{caption}</figcaption>}
    </figure>
  )
}
