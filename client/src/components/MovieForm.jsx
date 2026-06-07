import { useState } from "react";

export default function MovieForm({ genres, onAdd, loading }) {
  const [title, setTitle] = useState("");
  const [genre, setGenre] = useState("Inne");

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedTitle = title.trim();

    if (trimmedTitle.length < 4) {
      return;
    }

    await onAdd({
      title: trimmedTitle,
      genre,
      done: false,
    });

    setTitle("");
    setGenre("Inne");
  }

  return (
    <form className="movie-form" onSubmit={handleSubmit} id="add">
      <div className="movie-form__group">
        <label>Tytuł filmu</label>
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Np. Interstellar"
          maxLength={80}
        />
      </div>

      <div className="movie-form__group">
        <label>Gatunek</label>
        <select value={genre} onChange={(event) => setGenre(event.target.value)}>
          {genres.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      <button className="btn btn--primary" disabled={loading}>
        {loading ? "Dodawanie..." : "Dodaj film"}
      </button>
    </form>
  );
}