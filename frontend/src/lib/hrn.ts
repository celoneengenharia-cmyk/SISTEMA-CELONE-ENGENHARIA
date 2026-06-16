// Espelho das tabelas e faixas do backend (app/services/hrn.py).
// O backend é a fonte da verdade; aqui replicamos só para o recálculo em tempo
// real na UI. Mantenha os valores idênticos aos do backend.

export type FactorCode = "lo" | "fe" | "dph" | "np";

export const FACTOR_NAMES: Record<FactorCode, string> = {
  lo: "Probabilidade de ocorrência",
  fe: "Frequência de exposição",
  dph: "Grau do possível dano",
  np: "Pessoas expostas",
};

export interface Opcao {
  valor: number;
  descricao: string;
}

export const TABELAS: Record<FactorCode, Opcao[]> = {
  lo: [
    { valor: 0.033, descricao: "Quase impossível — só em circunstâncias extremas" },
    { valor: 0.5, descricao: "Altamente improvável" },
    { valor: 1, descricao: "Improvável, embora possível" },
    { valor: 1.5, descricao: "Possível" },
    { valor: 2, descricao: "Alguma chance" },
    { valor: 5, descricao: "Provável" },
    { valor: 8, descricao: "Provável a alta" },
    { valor: 10, descricao: "Muito provável" },
    { valor: 15, descricao: "Certeza — já documentado" },
  ],
  fe: [
    { valor: 0.1, descricao: "Anualmente" },
    { valor: 0.2, descricao: "Mensalmente" },
    { valor: 1, descricao: "Semanalmente" },
    { valor: 1.5, descricao: "Diariamente" },
    { valor: 2.5, descricao: "Por hora" },
    { valor: 4, descricao: "Constantemente" },
    { valor: 5, descricao: "A cada minuto" },
  ],
  dph: [
    { valor: 0.1, descricao: "Arranhão / hematoma" },
    { valor: 0.5, descricao: "Corte / laceração leve" },
    { valor: 1, descricao: "Lesão leve, afastamento curto" },
    { valor: 2, descricao: "Afastamento — corte profundo, fratura simples" },
    { valor: 4, descricao: "Perda de 1 dedo / sequela menor" },
    { valor: 6, descricao: "Amputação parcial mão-pé · perda de visão (1 olho) · perda auditiva" },
    { valor: 8, descricao: "Amputação de membro · cegueira · fatalidade individual" },
    { valor: 10, descricao: "Múltiplas amputações · fatalidade" },
    { valor: 15, descricao: "Múltiplas fatalidades" },
  ],
  np: [
    { valor: 1, descricao: "1 pessoa" },
    { valor: 2, descricao: "2 pessoas" },
    { valor: 4, descricao: "3 a 7 pessoas" },
    { valor: 8, descricao: "8 a 15 pessoas" },
    { valor: 12, descricao: "Mais de 15 pessoas" },
  ],
};

export interface Band {
  indice: number;
  nome: string;
  min: number;
  max: number; // Infinity na última
  cor: string;
  txt: string;
  tratamento: string;
}

export const BANDS: Band[] = [
  { indice: 0, nome: "Aceitável", min: 0, max: 1, cor: "--b0", txt: "#fff", tratamento: "Sem ação obrigatória" },
  { indice: 1, nome: "Muito baixo", min: 1, max: 5, cor: "--b1", txt: "#fff", tratamento: "Monitoramento, melhoria contínua" },
  { indice: 2, nome: "Baixo", min: 5, max: 10, cor: "--b2", txt: "#16181D", tratamento: "Ação a planejar" },
  { indice: 3, nome: "Significativo", min: 10, max: 50, cor: "--b3", txt: "#16181D", tratamento: "Ação necessária" },
  { indice: 4, nome: "Alto", min: 50, max: 100, cor: "--b4", txt: "#16181D", tratamento: "Ação urgente" },
  { indice: 5, nome: "Muito alto", min: 100, max: 500, cor: "--b5", txt: "#fff", tratamento: "Ação imediata, condicionar operação" },
  { indice: 6, nome: "Extremo", min: 500, max: 1000, cor: "--b6", txt: "#fff", tratamento: "Parar a operação até mitigação" },
  { indice: 7, nome: "Inaceitável", min: 1000, max: Infinity, cor: "--b7", txt: "#fff", tratamento: "Parar imediatamente" },
];

export function bandIndex(h: number): number {
  let i = 0;
  for (let k = 0; k < BANDS.length; k++) if (h >= BANDS[k].min) i = k;
  return i;
}

export function classificar(h: number): Band {
  return BANDS[bandIndex(h)];
}

export function calcularHRN(lo: number, fe: number, dph: number, np: number): number {
  return Math.round(lo * fe * dph * np * 100) / 100;
}

export const fmtN = (n: number) => String(n).replace(".", ",");

export function fmtHRN(h: number): string {
  if (!isFinite(h)) return "—";
  const r = Math.round(h * 100) / 100;
  return fmtN(Number.isInteger(r) ? r : parseFloat(r.toFixed(2)));
}

// Posição (%) do marcador na barra de faixas — replica o protótipo (escala log
// dentro de cada faixa, 12,5% por faixa).
export function scalePos(h: number): number {
  const i = bandIndex(h);
  const w = 12.5;
  const base = i * w;
  const clamp = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));
  let f: number;
  if (i === 0) f = clamp(h / 1, 0, 1);
  else if (i === 7) f = clamp((Math.log10(h) - 3) / (Math.log10(5000) - 3), 0, 1);
  else {
    const lo = BANDS[i].min;
    const hi = BANDS[i].max;
    f = clamp((Math.log10(h) - Math.log10(lo)) / (Math.log10(hi) - Math.log10(lo)), 0, 1);
  }
  return base + f * w;
}

export const NIVEIS_ISO: [string, string][] = [
  ["M1", "Projeto intrinsecamente seguro"],
  ["M2", "Proteção / dispositivo de segurança"],
  ["M3", "Informação para uso"],
  ["M4", "EPI"],
];

export interface AvaliacaoLocal {
  hrnAntes: number;
  hrnDepois: number | null;
  bandAntes: Band;
  bandDepois: Band | null;
  queda: number | null;
  nivel: "ok" | "warn" | "bad" | "incompleto";
  mensagem: string;
}

export function avaliarLocal(
  antes: Record<FactorCode, number>,
  depois: Record<FactorCode, number> | null,
): AvaliacaoLocal {
  const hrnAntes = calcularHRN(antes.lo, antes.fe, antes.dph, antes.np);
  const bandAntes = classificar(hrnAntes);
  if (!depois) {
    return {
      hrnAntes, hrnDepois: null, bandAntes, bandDepois: null, queda: null,
      nivel: "incompleto",
      mensagem: "Apreciação incompleta — defina os fatores após as medidas.",
    };
  }
  const hrnDepois = calcularHRN(depois.lo, depois.fe, depois.dph, depois.np);
  const bandDepois = classificar(hrnDepois);
  const queda = bandAntes.indice - bandDepois.indice;
  let nivel: AvaliacaoLocal["nivel"];
  let mensagem: string;
  if (bandDepois.indice > bandAntes.indice) {
    nivel = "bad";
    mensagem = "O risco aumentou após as medidas — o HRN de 'depois' não pode ser maior que o de 'antes'. Revise os fatores.";
  } else if (queda <= 0) {
    nivel = "warn";
    mensagem = "Sem redução de faixa. A apreciação só se completa quando o HRN cai pelo menos uma faixa; reforce as medidas.";
  } else {
    nivel = "ok";
    mensagem = `Risco reduzido em ${queda} faixa${queda > 1 ? "s" : ""} — de "${bandAntes.nome}" para "${bandDepois.nome}".`;
  }
  return { hrnAntes, hrnDepois, bandAntes, bandDepois, queda, nivel, mensagem };
}
