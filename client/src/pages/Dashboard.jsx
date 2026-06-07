import { useEffect, useMemo, useState } from "react";

import { tasksApi } from "../api/tasksApi";
import { DEFAULT_GENRES } from "../constants/genres";
import { normalizeTask } from "../utils/movieUtils";

import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import MovieForm from "../components/MovieForm";
import Filters from "../components/Filters";
import MovieCard from "../components/MovieCard";


export default function Dashboard() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [genreFilter, setGenreFilter] = useState("all");
  const [showForm, setShowForm] = useState(false);

  async function loadMovies() {
    try {
      setError("");
      setLoading(true);

      const data = await tasksApi.getAll();
      setMovies(Array.isArray(data) ? data.map(normalizeTask) : []);
    } catch (err) {
      setError(err.message || "Nie udało się pobrać filmów.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMovies();
  }, []);

  const genres = useMemo(() => {
    const fromMovies = movies.map((movie) => movie.genre).filter(Boolean);
    return Array.from(new Set([...DEFAULT_GENRES, ...fromMovies]));
  }, [movies]);

  const stats = useMemo(() => {
    const total = movies.length;
    const watched = movies.filter((movie) => movie.done).length;

    return {
      total,
      watched,
      unwatched: total - watched,
    };
  }, [movies]);

  const filteredMovies = useMemo(() => {
    return movies.filter((movie) => {
      const matchesSearch = movie.title
        .toLowerCase()
        .includes(search.trim().toLowerCase());

      const matchesStatus =
        statusFilter === "all" ||
        (statusFilter === "watched" && movie.done) ||
        (statusFilter === "unwatched" && !movie.done);

      const matchesGenre = genreFilter === "all" || movie.genre === genreFilter;

      return matchesSearch && matchesStatus && matchesGenre;
    });
  }, [movies, search, statusFilter, genreFilter]);

  const recentMovies = useMemo(() => {
    return [...movies]
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .slice(0, 3);
  }, [movies]);

  async function handleAddMovie(data) {
    try {
      setError("");
      setActionLoading(true);

      await tasksApi.create(data);
      await loadMovies();
      setShowForm(false);
    } catch (err) {
      setError(err.message || "Nie udało się dodać filmu.");
    } finally {
      setActionLoading(false);
    }
  }

  async function handleToggleMovie(movie) {
    try {
      setError("");

      await tasksApi.update(movie.id, {
        done: !movie.done,
      });

      setMovies((currentMovies) =>
        currentMovies.map((item) =>
          item.id === movie.id ? { ...item, done: !item.done } : item
        )
      );
    } catch (err) {
      setError(err.message || "Nie udało się zaktualizować filmu.");
    }
  }

  async function handleDeleteMovie(id) {
    const confirmed = window.confirm("Na pewno usunąć ten film?");

    if (!confirmed) return;

    try {
      setError("");
      await tasksApi.remove(id);

      setMovies((currentMovies) =>
        currentMovies.filter((movie) => movie.id !== id)
      );
    } catch (err) {
      setError(err.message || "Nie udało się usunąć filmu.");
    }
  }

  return (
    <>
      <Navbar />

      <main className="page" id="home">
        <section className="hero">
          <p className="eyebrow">Twoja prywatna watchlista</p>

          <h1>
            CINE<span>LIST</span>
          </h1>

          <p className="hero__subtitle">
            Prosta aplikacja do zapisywania filmów, które chcesz obejrzeć.
          </p>

          <div className="hero__actions">
            <button
              className="btn btn--primary"
              onClick={() => setShowForm((value) => !value)}
            >
              {showForm ? "Ukryj formularz" : "Dodaj film"}
            </button>

            <a className="btn btn--secondary" href="#movies">
              Zobacz wszystko
            </a>
          </div>
        </section>

        <section className="stats-grid">
          <StatCard value={stats.total} label="Wszystkich filmów" variant="all" />
          <StatCard value={stats.watched} label="Obejrzanych" variant="done" />
          <StatCard value={stats.unwatched} label="Do obejrzenia" variant="todo" />
        </section>

        {showForm && (
          <MovieForm
            genres={genres}
            onAdd={handleAddMovie}
            loading={actionLoading}
          />
        )}

        {error && <div className="alert">{error}</div>}

        <section className="section">
          <div className="section__header">
            <h2>Ostatnio dodane</h2>
          </div>

          {loading ? (
            <p className="muted">Ładowanie filmów...</p>
          ) : recentMovies.length > 0 ? (
            <div className="compact-list">
              {recentMovies.map((movie) => (
                <MovieCard
                  key={movie.id}
                  movie={movie}
                  onToggle={handleToggleMovie}
                  onDelete={handleDeleteMovie}
                />
              ))}
            </div>
          ) : (
            <EmptyState />
          )}
        </section>

        <section className="section" id="movies">
          <div className="section__header section__header--wide">
            <div>
              <h2>Wszystkie filmy</h2>
              <p>Przeglądaj, filtruj i oznaczaj obejrzane tytuły.</p>
            </div>
          </div>

          <Filters
            search={search}
            setSearch={setSearch}
            statusFilter={statusFilter}
            setStatusFilter={setStatusFilter}
            genreFilter={genreFilter}
            setGenreFilter={setGenreFilter}
            genres={genres}
          />

          {loading ? (
            <p className="muted">Ładowanie filmów...</p>
          ) : filteredMovies.length > 0 ? (
            <div className="movie-list">
              {filteredMovies.map((movie) => (
                <MovieCard
                  key={movie.id}
                  movie={movie}
                  onToggle={handleToggleMovie}
                  onDelete={handleDeleteMovie}
                />
              ))}
            </div>
          ) : (
        <section className="empty-state">
        <div>🎥</div>
        <h3>Brak filmów</h3>
        <p>Dodaj pierwszy film do swojej listy.</p>
        </section>
    )}
        </section>
      </main>
    </>
  );
}