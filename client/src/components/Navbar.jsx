export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar__brand">
        <span className="brand-icon">🎬</span>
        <span>CINE</span>
        <strong>LIST</strong>
      </div>

      <div className="navbar__links">
        <a href="#home">Home</a>
        <a href="#movies">Filmy</a>
        <a href="#add">+ Dodaj</a>
      </div>
    </nav>
  );
}