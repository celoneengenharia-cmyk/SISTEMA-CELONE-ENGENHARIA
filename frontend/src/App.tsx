import { EditorLaudo } from "./pages/EditorLaudo";

export default function App() {
  return (
    <div className="wrap">
      <div className="app-head">
        <div>
          <h1>Laudos de Apreciação de Riscos — NR-12</h1>
          <div className="sub">
            Motor HRN · galeria de fotos · geração de DOCX · escala ABNT NBR ISO/TR 14121-2
          </div>
        </div>
        <div className="tag">Celone Engenharia</div>
      </div>
      <EditorLaudo />
    </div>
  );
}
