export function formatDate(dateString) {
  if (!dateString) return "";

  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) {
    return dateString.slice(0, 10);
  }

  return date.toLocaleDateString("pl-PL", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

export function normalizeTask(task) {
  return {
    ...task,
    done: Boolean(task.done),
    genre: task.genre || "Inne",
  };
}