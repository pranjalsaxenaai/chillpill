export function getUser(idToken: string) {
  return fetch(`http://127.0.0.1:8000/api/users`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${idToken}`,
    },
  });
}

export function createUser(idToken: string) {
  return fetch(`http://127.0.0.1:8000/api/users`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${idToken}`,
    },
  });
}
