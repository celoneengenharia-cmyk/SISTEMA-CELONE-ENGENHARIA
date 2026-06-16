import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Cliente, Laudo, Maquina, Parecer, Perigo, Status } from "../types";
import { CardPerigo } from "../components/CardPerigo";
import { GaleriaFotos } from "../components/GaleriaFotos";

function Secao({ n, titulo, children }: { n: number; titulo: string; children: React.ReactNode }) {
  return (
    <>
      <div className="section-title"><span className="n">{n}</span>{titulo}</div>
      {children}
    </>
  );
}

export function EditorLaudo() {
  const [laudo, setLaudo] = useState<Laudo | null>(null);
  const [perigos, setPerigos] = useState<Perigo[]>([]);
  const [novo, setNovo] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  // Ao abrir/criar um laudo, carrega os perigos associados.
  useEffect(() => {
    if (laudo) api.listPerigos(laudo.id).then(setPerigos).catch((e) => setErro(e.message));
  }, [laudo?.id]);

  if (!laudo) return <SetupLaudo onCriado={(l) => { setLaudo(l); setPerigos([]); }} erro={erro} />;

  const maq = laudo.maquina;
  const cli = laudo.cliente;

  async function gerarDocx() {
    setErro(null);
    try {
      const blob = await api.gerarDocx(laudo!.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `laudo-${laudo!.id}.docx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setErro((e as Error).message);
    }
  }

  async function patchLaudo(patch: Partial<Laudo>) {
    const l = await api.updateLaudo(laudo!.id, patch);
    setLaudo(l);
  }

  return (
    <div>
      {erro && <div className="err">{erro}</div>}

      <div className="banner">
        Laudo #{laudo.id} · <b>{cli?.nome}</b> · {maq?.tipo}
        {maq?.modelo ? ` ${maq.modelo}` : ""} · variante {laudo.variante}
        {" "}<a href="#" onClick={(e) => { e.preventDefault(); setLaudo(null); }}>trocar laudo</a>
      </div>

      <Secao n={1} titulo="Identificação">
        <div className="card grid2">
          <div><label className="fld">Cliente</label><input value={cli?.nome ?? ""} disabled /></div>
          <div><label className="fld">Máquina</label><input value={`${maq?.tipo ?? ""} ${maq?.modelo ?? ""}`} disabled /></div>
          <div>
            <label className="fld">Data de emissão</label>
            <input type="date" value={laudo.data_emissao ?? ""}
              onChange={(e) => patchLaudo({ data_emissao: e.target.value || null })} />
          </div>
          <div>
            <label className="fld">Escala de FE adotada (documentar é exigência da metodologia)</label>
            <input value={laudo.escala_fe ?? ""} placeholder="Ex.: FE da ABNT NBR ISO/TR 14121-2"
              onChange={(e) => patchLaudo({ escala_fe: e.target.value })} />
          </div>
        </div>
      </Secao>

      <Secao n={2} titulo="Registro fotográfico">
        <div className="card"><GaleriaFotos laudoId={laudo.id} /></div>
      </Secao>

      <Secao n={3} titulo="Apreciação de riscos — motor HRN">
        {perigos.map((p) => (
          <CardPerigo
            key={p.id}
            laudoId={laudo.id}
            perigo={p}
            onSaved={(sp) => setPerigos((ps) => ps.map((x) => (x.id === sp.id ? sp : x)))}
            onDeleted={(id) => setPerigos((ps) => ps.filter((x) => x.id !== id))}
          />
        ))}
        {novo ? (
          <CardPerigo
            laudoId={laudo.id}
            perigo={null}
            onSaved={(sp) => { setPerigos((ps) => [...ps, sp]); setNovo(false); }}
            onDeleted={() => setNovo(false)}
            onCancel={() => setNovo(false)}
          />
        ) : (
          <button className="btn btn-primary" onClick={() => setNovo(true)}>+ Novo perigo</button>
        )}
      </Secao>

      <Secao n={4} titulo="Parecer e geração">
        <div className="card">
          <p className="muted">
            O parecer de conformidade é decisão explícita do engenheiro — nunca derivado
            automaticamente do HRN.
          </p>
          <div className="grid2">
            <div>
              <label className="fld">Status</label>
              <select value={laudo.status} onChange={(e) => patchLaudo({ status: e.target.value as Status })}>
                <option value="rascunho">Rascunho</option>
                <option value="em_analise">Em análise</option>
                <option value="concluido">Concluído</option>
              </select>
            </div>
            <div>
              <label className="fld">Parecer de conformidade</label>
              <select value={laudo.parecer ?? ""}
                onChange={(e) => patchLaudo({ parecer: (e.target.value || null) as Parecer | null })}>
                <option value="">— a decidir —</option>
                <option value="conforme">Conforme</option>
                <option value="com_ressalvas">Com ressalvas</option>
                <option value="nao_conforme">Não conforme</option>
              </select>
            </div>
          </div>
          <div className="row" style={{ marginTop: 16 }}>
            <button className="btn btn-primary" onClick={gerarDocx}>Gerar DOCX (padrão Celone)</button>
          </div>
        </div>
      </Secao>
    </div>
  );
}

// --- Setup inicial: cria/seleciona cliente, máquina e o laudo ---------------

function SetupLaudo({ onCriado, erro }: { onCriado: (l: Laudo) => void; erro: string | null }) {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [maquinas, setMaquinas] = useState<Maquina[]>([]);
  const [laudos, setLaudos] = useState<Laudo[]>([]);
  const [cliId, setCliId] = useState<number | "">("");
  const [maqId, setMaqId] = useState<number | "">("");
  const [novoCli, setNovoCli] = useState("");
  const [novaMaq, setNovaMaq] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    api.listClientes().then(setClientes);
    api.listMaquinas().then(setMaquinas);
    api.listLaudos().then(setLaudos);
  }, []);

  async function criar() {
    setMsg(null);
    try {
      let cliente = cliId;
      if (!cliente && novoCli.trim()) {
        const c = await api.createCliente({ nome: novoCli.trim() });
        cliente = c.id;
      }
      let maquina = maqId;
      if (!maquina && novaMaq.trim()) {
        const m = await api.createMaquina({ tipo: novaMaq.trim() });
        maquina = m.id;
      }
      if (!cliente || !maquina) { setMsg("Escolha (ou crie) um cliente e uma máquina."); return; }
      const l = await api.createLaudo({ cliente_id: Number(cliente), maquina_id: Number(maquina) });
      onCriado(await api.getLaudo(l.id));
    } catch (e) {
      setMsg((e as Error).message);
    }
  }

  return (
    <div>
      {(erro || msg) && <div className="err">{erro ?? msg}</div>}

      {laudos.length > 0 && (
        <div className="card">
          <label className="fld">Abrir laudo existente</label>
          <div className="row">
            {laudos.map((l) => (
              <button key={l.id} className="btn btn-ghost btn-sm"
                onClick={() => api.getLaudo(l.id).then(onCriado)}>
                #{l.id} · {l.variante} · {l.status}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <label className="fld">Novo laudo</label>
        <div className="grid2">
          <div>
            <label className="fld">Cliente existente</label>
            <select value={cliId} onChange={(e) => setCliId(e.target.value ? Number(e.target.value) : "")}>
              <option value="">— selecionar —</option>
              {clientes.map((c) => <option key={c.id} value={c.id}>{c.nome}</option>)}
            </select>
            <div style={{ marginTop: 8 }}>
              <label className="fld">…ou novo cliente</label>
              <input value={novoCli} onChange={(e) => setNovoCli(e.target.value)} placeholder="Nome do cliente" />
            </div>
          </div>
          <div>
            <label className="fld">Máquina existente</label>
            <select value={maqId} onChange={(e) => setMaqId(e.target.value ? Number(e.target.value) : "")}>
              <option value="">— selecionar —</option>
              {maquinas.map((m) => <option key={m.id} value={m.id}>{m.tipo} {m.modelo ?? ""}</option>)}
            </select>
            <div style={{ marginTop: 8 }}>
              <label className="fld">…ou nova máquina</label>
              <input value={novaMaq} onChange={(e) => setNovaMaq(e.target.value)} placeholder="Tipo da máquina" />
            </div>
          </div>
        </div>
        <div className="row" style={{ marginTop: 16 }}>
          <button className="btn btn-primary" onClick={criar}>Criar laudo</button>
        </div>
      </div>
    </div>
  );
}
