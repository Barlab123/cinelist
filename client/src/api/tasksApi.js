const API_URL = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();

  if (!response.ok) {
    let message = "Coś poszło nie tak.";

    try {
      const errorData = text ? JSON.parse(text) : null;
      message = errorData?.description || errorData?.message || message;
    } catch {
      message = text || message;
    }

    throw new Error(message);
  }

  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
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