const API_URL = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = "Coś poszło nie tak.";

    try {
      const errorData = await response.json();
      message = errorData.description || errorData.message || message;
    } catch {
      try {
        message = await response.text();
      } catch {
        message = "Błąd połączenia z API.";
      }
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const tasksApi = {
  getAll() {
    return request("/tasks");
  },

  create(data) {
    return request("/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  update(id, data) {
    return request(`/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  remove(id) {
    return request(`/tasks/${id}`, {
      method: "DELETE",
    });
  },
};