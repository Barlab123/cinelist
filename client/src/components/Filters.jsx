export default function Filters({
  search,
  setSearch,
  statusFilter,
  setStatusFilter,
  genreFilter,
  setGenreFilter,
  genres,
}) {
  return (
    <section className="filters">
      <input
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder="Szukaj filmu..."
      />

      <select
        value={statusFilter}
        onChange={(event) => setStatusFilter(event.target.value)}
      >
        <option value="all">Wszystkie</option>
        <option value="watched">Obejrzane</option>
        <option value="unwatched">Do obejrzenia</option>
      </select>

      <select
        value={genreFilter}
        onChange={(event) => setGenreFilter(event.target.value)}
      >
        <option value="all">Każdy gatunek</option>
        {genres.map((genre) => (
          <option key={genre} value={genre}>
            {genre}
          </option>
        ))}
      </select>
    </section>
  );
}