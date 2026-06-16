import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import type { Foto } from "../types";

interface Props {
  laudoId: number;
}

export function GaleriaFotos({ laudoId }: Props) {
  const [fotos, setFotos] = useState<Foto[]>([]);
  const [drag, setDrag] = useState(false);
  const [busy, setBusy] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const dragId = useRef<number | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { api.listFotos(laudoId).then(setFotos).catch((e) => setErro(e.message)); }, [laudoId]);

  async function enviar(files: FileList | null) {
    if (!files || files.length === 0) return;
    setBusy(true);
    setErro(null);
    try {
      const novas = await api.uploadFotos(laudoId, Array.from(files));
      setFotos((f) => [...f, ...novas]);
    } catch (e) {
      setErro((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  // Salva legenda/ponto de risco ao sair do campo (onBlur).
  function patchLocal(id: number, patch: Partial<Foto>) {
    setFotos((f) => f.map((x) => (x.id === id ? { ...x, ...patch } : x)));
  }
  async function salvarMeta(foto: Foto) {
    try {
      await api.updateFoto(foto.id, { legenda: foto.legenda, ponto_risco: foto.ponto_risco });
    } catch (e) {
      setErro((e as Error).message);
    }
  }

  // Reordenação por arrastar entre cards.
  async function soltarSobre(alvoId: number) {
    const origem = dragId.current;
    dragId.current = null;
    if (origem == null || origem === alvoId) return;
    const ids = fotos.map((f) => f.id);
    const from = ids.indexOf(origem);
    const to = ids.indexOf(alvoId);
    ids.splice(to, 0, ids.splice(from, 1)[0]);
    setFotos((f) => ids.map((id, i) => ({ ...f.find((x) => x.id === id)!, ordem: i })));
    try {
      const atualizadas = await api.reorderFotos(laudoId, ids);
      setFotos(atualizadas);
    } catch (e) {
      setErro((e as Error).message);
    }
  }

  async function remover(id: number) {
    if (!confirm("Remover esta foto?")) return;
    await api.deleteFoto(id);
    setFotos((f) => f.filter((x) => x.id !== id));
  }

  return (
    <div>
      {erro && <div className="err">{erro}</div>}
      <div
        className={`dropzone${drag ? " drag" : ""}`}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => { e.preventDefault(); setDrag(false); enviar(e.dataTransfer.files); }}
      >
        {busy ? "Enviando…" : "Arraste imagens aqui ou clique para selecionar (upload em lote)"}
        <input ref={inputRef} type="file" accept="image/*" multiple hidden
          onChange={(e) => enviar(e.target.files)} />
      </div>

      {fotos.length > 0 && (
        <div className="gallery" style={{ marginTop: 16 }}>
          {fotos.map((f) => (
            <div
              className="foto" key={f.id} draggable
              onDragStart={() => { dragId.current = f.id; }}
              onDragOver={(e) => e.preventDefault()}
              onDrop={() => soltarSobre(f.id)}
            >
              {f.url && <img src={`/api${f.url}`} alt={f.legenda ?? ""} />}
              <div className="meta">
                <div className="ord">Figura {f.ordem + 1} · arraste para reordenar</div>
                <input value={f.legenda ?? ""} placeholder="Legenda"
                  onChange={(e) => patchLocal(f.id, { legenda: e.target.value })}
                  onBlur={() => salvarMeta(f)} />
                <input value={f.ponto_risco ?? ""} placeholder="Ponto de risco apontado"
                  onChange={(e) => patchLocal(f.id, { ponto_risco: e.target.value })}
                  onBlur={() => salvarMeta(f)} />
                <button className="btn btn-ghost btn-sm" onClick={() => remover(f.id)}>Remover</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
