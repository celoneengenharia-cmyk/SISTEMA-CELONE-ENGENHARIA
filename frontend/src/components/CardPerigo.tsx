import { useMemo, useState } from "react";
import {
  avaliarLocal, classificar, FACTOR_NAMES, FactorCode, fmtHRN, fmtN,
  NIVEIS_ISO, TABELAS,
} from "../lib/hrn";
import type { Perigo } from "../types";
import { api } from "../api/client";
import { EscalaHRN } from "./EscalaHRN";

const TIPOS = [
  "Mecânico — esmagamento", "Mecânico — corte / cisalhamento",
  "Mecânico — arrasto / enrolamento", "Elétrico", "Ruído", "Ergonômico",
  "Químico", "Térmico",
];
const FASES = [
  "Operação normal", "Preparação / setup", "Limpeza", "Manutenção", "Desobstrução",
];
const CODES: FactorCode[] = ["lo", "fe", "dph", "np"];

interface Medida { nivel: string; texto: string; }

interface Draft {
  tipo: string;
  fase_vida: string;
  descricao: string;
  antes: Record<FactorCode, number>;
  depois: Record<FactorCode, number>;
  justificativas: Record<string, string>;
  medidas: Medida[];
  normas: string;
}

function parseMedidas(medidas: string[]): Medida[] {
  return medidas.map((m) => {
    const match = /^(M[1-4])\s*[—-]\s*(.*)$/.exec(m);
    return match ? { nivel: match[1], texto: match[2] } : { nivel: "M2", texto: m };
  });
}

function fromPerigo(p: Perigo | null): Draft {
  if (!p) {
    return {
      tipo: TIPOS[0], fase_vida: FASES[0], descricao: "",
      antes: { lo: 8, fe: 2.5, dph: 8, np: 2 },
      depois: { lo: 0.5, fe: 2.5, dph: 8, np: 2 },
      justificativas: {}, medidas: [], normas: "",
    };
  }
  return {
    tipo: p.tipo ?? "", fase_vida: p.fase_vida ?? "", descricao: p.descricao ?? "",
    antes: { lo: p.lo, fe: p.fe, dph: p.dph, np: p.np },
    depois: {
      lo: p.lo_pos ?? p.lo, fe: p.fe_pos ?? p.fe,
      dph: p.dph_pos ?? p.dph, np: p.np_pos ?? p.np,
    },
    justificativas: p.justificativas ?? {},
    medidas: parseMedidas(p.medidas ?? []),
    normas: (p.normas_violadas ?? []).join("\n"),
  };
}

interface Props {
  laudoId: number;
  perigo: Perigo | null;
  onSaved: (p: Perigo) => void;
  onDeleted: (id: number) => void;
  onCancel?: () => void;
}

const VALID_CLASS: Record<string, string> = {
  ok: "v-ok", warn: "v-warn", bad: "v-bad", incompleto: "v-incompleto",
};
const VALID_ICON: Record<string, string> = { ok: "✓", warn: "~", bad: "!", incompleto: "·" };

export function CardPerigo({ laudoId, perigo, onSaved, onDeleted, onCancel }: Props) {
  const [d, setD] = useState<Draft>(() => fromPerigo(perigo));
  const [saving, setSaving] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const av = useMemo(() => avaliarLocal(d.antes, d.depois), [d.antes, d.depois]);

  const setFactor = (side: "antes" | "depois", code: FactorCode, v: number) =>
    setD((p) => ({ ...p, [side]: { ...p[side], [code]: v } }));

  const pendentes = CODES.filter((c) => !(d.justificativas[c] ?? "").trim());

  async function salvar() {
    setSaving(true);
    setErro(null);
    const payload: Partial<Perigo> = {
      tipo: d.tipo, fase_vida: d.fase_vida, descricao: d.descricao,
      lo: d.antes.lo, fe: d.antes.fe, dph: d.antes.dph, np: d.antes.np,
      lo_pos: d.depois.lo, fe_pos: d.depois.fe, dph_pos: d.depois.dph, np_pos: d.depois.np,
      justificativas: d.justificativas,
      medidas: d.medidas.filter((m) => m.texto.trim()).map((m) => `${m.nivel} — ${m.texto.trim()}`),
      normas_violadas: d.normas.split("\n").map((s) => s.trim()).filter(Boolean),
    };
    try {
      const saved = perigo
        ? await api.updatePerigo(perigo.id, payload)
        : await api.createPerigo(laudoId, payload);
      onSaved(saved);
    } catch (e) {
      setErro((e as Error).message);
    } finally {
      setSaving(false);
    }
  }

  function renderFatores(side: "antes" | "depois") {
    return CODES.map((code) => {
      const isPend = side === "antes" && pendentes.includes(code);
      return (
        <div className="fac" key={code}>
          <div className="fac-head">
            <span className="fac-code">{code.toUpperCase()}</span>
            <span className="fac-name">{FACTOR_NAMES[code]}</span>
          </div>
          <select
            value={d[side][code]}
            onChange={(e) => setFactor(side, code, parseFloat(e.target.value))}
          >
            {TABELAS[code].map((o) => (
              <option key={o.valor} value={o.valor}>
                {fmtN(o.valor)} — {o.descricao}
              </option>
            ))}
          </select>
          {side === "antes" && (
            <div className={`just${isPend ? " pendente" : ""}`}>
              <input
                type="text"
                placeholder={`Justificativa do fator ${code.toUpperCase()} (nunca suponha)`}
                value={d.justificativas[code] ?? ""}
                onChange={(e) =>
                  setD((p) => ({ ...p, justificativas: { ...p.justificativas, [code]: e.target.value } }))
                }
              />
            </div>
          )}
        </div>
      );
    });
  }

  const bandDepois = av.bandDepois ?? classificar(av.hrnAntes);

  return (
    <div className="perigo-card crit">
      {erro && <div className="err">{erro}</div>}

      <div className="grid3" style={{ marginBottom: 16 }}>
        <div>
          <label className="fld">Perigo / modo de falha</label>
          <input value={d.descricao} onChange={(e) => setD({ ...d, descricao: e.target.value })}
            placeholder="Ex.: Esmagamento na zona de operação" />
        </div>
        <div>
          <label className="fld">Fase de vida</label>
          <select value={d.fase_vida} onChange={(e) => setD({ ...d, fase_vida: e.target.value })}>
            {FASES.map((f) => <option key={f}>{f}</option>)}
          </select>
        </div>
        <div>
          <label className="fld">Tipo de perigo</label>
          <select value={d.tipo} onChange={(e) => setD({ ...d, tipo: e.target.value })}>
            {TIPOS.map((t) => <option key={t}>{t}</option>)}
          </select>
        </div>
      </div>

      <EscalaHRN hrnAntes={av.hrnAntes} hrnDepois={av.hrnDepois} />

      <div className="cols">
        <div className="col">
          <h3>Antes <span className="when">situação atual</span></h3>
          <p className="desc">Risco como encontrado, com os dispositivos existentes.</p>
          {renderFatores("antes")}
          <div className="readout">
            <div className="hrn-val"><span className="eq">HRN</span>{fmtHRN(av.hrnAntes)}</div>
            <div>
              <span className="pill" style={{ background: `var(${av.bandAntes.cor})`, color: av.bandAntes.txt }}>
                {av.bandAntes.nome}
              </span>
              <div className="treat">{av.bandAntes.tratamento}</div>
            </div>
          </div>
        </div>

        <div className="col after">
          <h3>Depois <span className="when">após medidas</span></h3>
          <p className="desc">Risco residual depois das medidas de redução aplicadas.</p>
          {renderFatores("depois")}
          <div className="readout">
            <div className="hrn-val"><span className="eq">HRN</span>{fmtHRN(av.hrnDepois ?? 0)}</div>
            <div>
              <span className="pill" style={{ background: `var(${bandDepois.cor})`, color: bandDepois.txt }}>
                {bandDepois.nome}
              </span>
              <div className="treat">{bandDepois.tratamento}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="measures">
        <label className="fld">Medidas de redução — hierarquia ISO 12100</label>
        {d.medidas.map((m, i) => (
          <div className="m-row" key={i}>
            <select value={m.nivel}
              onChange={(e) => setD((p) => {
                const ms = [...p.medidas]; ms[i] = { ...ms[i], nivel: e.target.value }; return { ...p, medidas: ms };
              })}>
              {NIVEIS_ISO.map(([c, dsc]) => <option key={c} value={c}>{c} · {dsc}</option>)}
            </select>
            <input value={m.texto} placeholder="Descreva a medida de redução"
              onChange={(e) => setD((p) => {
                const ms = [...p.medidas]; ms[i] = { ...ms[i], texto: e.target.value }; return { ...p, medidas: ms };
              })} />
            <button className="x-btn" title="Remover"
              onClick={() => setD((p) => ({ ...p, medidas: p.medidas.filter((_, j) => j !== i) }))}>×</button>
          </div>
        ))}
        <button className="btn btn-ghost btn-sm"
          onClick={() => setD((p) => ({ ...p, medidas: [...p.medidas, { nivel: "M2", texto: "" }] }))}>
          + Adicionar medida
        </button>
      </div>

      <div className={`valid ${VALID_CLASS[av.nivel]}`}>
        <div className="ic">{VALID_ICON[av.nivel]}</div>
        <div><b>{av.mensagem}</b>
          {pendentes.length > 0 && (
            <span className="note">Fatores sem justificativa: {pendentes.map((c) => c.toUpperCase()).join(", ")}.</span>
          )}
        </div>
      </div>

      <div style={{ marginTop: 14 }}>
        <label className="fld">Normas violadas / aplicáveis (uma por linha)</label>
        <textarea rows={2} value={d.normas} onChange={(e) => setD({ ...d, normas: e.target.value })}
          placeholder={"NR-12 item 12.38\nABNT NBR ISO 13849-1"} />
      </div>

      <div className="row" style={{ marginTop: 14 }}>
        <button className="btn btn-primary" disabled={saving} onClick={salvar}>
          {saving ? "Salvando…" : perigo ? "Salvar perigo" : "Adicionar perigo"}
        </button>
        {onCancel && <button className="btn btn-ghost" onClick={onCancel}>Cancelar</button>}
        <div className="spacer" />
        {perigo && (
          <button className="btn btn-ghost btn-sm"
            onClick={() => { if (confirm("Remover este perigo?")) { api.deletePerigo(perigo.id).then(() => onDeleted(perigo.id)); } }}>
            Remover
          </button>
        )}
      </div>
    </div>
  );
}
