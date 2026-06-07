import { formatDate } from "../utils/movieUtils";

export default function MovieCard({ movie, onToggle, onDelete }) {
  return (
    <article className="movie-card">
      <button
        className={`movie-card__check ${movie.done ? "is-done" : ""}`}
        onClick={() => onToggle(movie)}
        title={movie.done ? "Oznacz jako nieobejrzany" : "Oznacz jako obejrzany"}
      >
        {movie.done ? "✓" : "○"}
      </button>

      <div className="movie-card__content">
        <h3 className={movie.done ? "is-watched" : ""}>{movie.title}</h3>

        <div className="movie-card__meta">
          <span>{movie.done ? "Obejrzany" : "Do obejrzenia"}</span>
          <span>•</span>
          <span>{formatDate(movie.created_at)}</span>
        </div>
      </div>

      <span className="movie-card__genre">{movie.genre}</span>

      <button className="movie-card__delete" onClick={() => onDelete(movie.id)}>
        Usuń
      </button>
    </article>
  );
}