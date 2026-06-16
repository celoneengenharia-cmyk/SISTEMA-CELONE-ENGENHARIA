import type { Cliente, Foto, Laudo, Maquina, Perigo } from "../types";

const BASE = "/api";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(BASE + path, {
    headers: init?.body && !(init.body instanceof FormData)
      ? { "Content-Type": "application/json" }
      : undefined,
    ...init,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      detail = j.detail ?? detail;
    } catch { /* corpo não-JSON */ }
    throw new Error(`${res.status}: ${detail}`);
  }
  if (res.status === 204) return undefined as T;
  const ct = res.headers.get("content-type") ?? "";
  return (ct.includes("application/json") ? res.json() : res.blob()) as Promise<T>;
}

export const api = {
  // clientes
  listClientes: () => req<Cliente[]>("/clientes"),
  createCliente: (data: Partial<Cliente>) =>
    req<Cliente>("/clientes", { method: "POST", body: JSON.stringify(data) }),

  // maquinas
  listMaquinas: () => req<Maquina[]>("/maquinas"),
  createMaquina: (data: Partial<Maquina>) =>
    req<Maquina>("/maquinas", { method: "POST", body: JSON.stringify(data) }),

  // laudos
  listLaudos: () => req<Laudo[]>("/laudos"),
  getLaudo: (id: number) => req<Laudo>(`/laudos/${id}`),
  createLaudo: (data: Partial<Laudo>) =>
    req<Laudo>("/laudos", { method: "POST", body: JSON.stringify(data) }),
  updateLaudo: (id: number, data: Partial<Laudo>) =>
    req<Laudo>(`/laudos/${id}`, { method: "PATCH", body: JSON.stringify(data) }),

  // perigos
  listPerigos: (laudoId: number) => req<Perigo[]>(`/laudos/${laudoId}/perigos`),
  createPerigo: (laudoId: number, data: Partial<Perigo>) =>
    req<Perigo>(`/laudos/${laudoId}/perigos`, { method: "POST", body: JSON.stringify(data) }),
  updatePerigo: (id: number, data: Partial<Perigo>) =>
    req<Perigo>(`/perigos/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deletePerigo: (id: number) => req<void>(`/perigos/${id}`, { method: "DELETE" }),

  // fotos
  listFotos: (laudoId: number) => req<Foto[]>(`/laudos/${laudoId}/fotos`),
  uploadFotos: (laudoId: number, files: File[]) => {
    const fd = new FormData();
    files.forEach((f) => fd.append("arquivos", f));
    return req<Foto[]>(`/laudos/${laudoId}/fotos`, { method: "POST", body: fd });
  },
  updateFoto: (id: number, data: Partial<Foto>) =>
    req<Foto>(`/fotos/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  reorderFotos: (laudoId: number, ordemIds: number[]) =>
    req<Foto[]>(`/laudos/${laudoId}/fotos/ordem`, {
      method: "PUT", body: JSON.stringify({ ordem_ids: ordemIds }),
    }),
  deleteFoto: (id: number) => req<void>(`/fotos/${id}`, { method: "DELETE" }),

  // docx
  gerarDocx: (laudoId: number) =>
    req<Blob>(`/laudos/${laudoId}/docx`, { method: "POST" }),
};
