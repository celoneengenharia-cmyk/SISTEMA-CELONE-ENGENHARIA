export type Variante = "enxuto" | "detalhado";
export type Status = "rascunho" | "em_analise" | "concluido";
export type Parecer = "conforme" | "com_ressalvas" | "nao_conforme";

export interface Cliente {
  id: number;
  nome: string;
  cnpj?: string | null;
  endereco?: string | null;
  contato?: string | null;
}

export interface Maquina {
  id: number;
  tipo: string;
  fabricante?: string | null;
  modelo?: string | null;
  serie?: string | null;
  ano?: string | null;
  funcao?: string | null;
  localizacao?: string | null;
  anexo_nr12?: string | null;
}

export interface Laudo {
  id: number;
  cliente_id: number;
  maquina_id: number;
  variante: Variante;
  status: Status;
  parecer: Parecer | null;
  escala_fe: string | null;
  data_emissao: string | null;
  docx_key: string | null;
  cliente?: Cliente;
  maquina?: Maquina;
}

export interface Foto {
  id: number;
  laudo_id: number;
  storage_key: string;
  legenda: string | null;
  ordem: number;
  ponto_risco: string | null;
  url: string | null;
}

export interface Perigo {
  id: number;
  laudo_id: number;
  tipo: string | null;
  fase_vida: string | null;
  descricao: string | null;
  lo: number;
  fe: number;
  dph: number;
  np: number;
  justificativas: Record<string, string>;
  hrn_atual: number;
  classif_atual: string | null;
  medidas: string[];
  lo_pos: number | null;
  fe_pos: number | null;
  dph_pos: number | null;
  np_pos: number | null;
  hrn_pos: number | null;
  classif_pos: string | null;
  normas_violadas: string[];
  queda_faixas: number | null;
  nivel_validacao: string | null;
  mensagem_validacao: string | null;
  fatores_pendentes: string[];
}
