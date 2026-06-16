import { BANDS, fmtHRN, scalePos } from "../lib/hrn";

interface Props {
  hrnAntes: number;
  hrnDepois: number | null;
}

/** Barra de faixas com os marcadores "antes" e "depois" (replica o protótipo). */
export function EscalaHRN({ hrnAntes, hrnDepois }: Props) {
  return (
    <div className="scale-card">
      <div className="scale-top">
        {hrnDepois !== null && (
          <div className="marker m-depois" style={{ left: `${scalePos(hrnDepois)}%` }}>
            <span className="lbl">depois {fmtHRN(hrnDepois)}</span>
            <span className="tri" />
          </div>
        )}
      </div>
      <div className="scale-bar">
        {BANDS.map((b) => (
          <div key={b.indice} className="seg" style={{ background: `var(${b.cor})` }} />
        ))}
      </div>
      <div className="seg-labels">
        {BANDS.map((b) => (
          <span key={b.indice}>{b.nome}</span>
        ))}
      </div>
      <div className="scale-bot">
        <div className="marker m-antes" style={{ left: `${scalePos(hrnAntes)}%` }}>
          <span className="tri" />
          <span className="lbl">antes {fmtHRN(hrnAntes)}</span>
        </div>
      </div>
    </div>
  );
}
