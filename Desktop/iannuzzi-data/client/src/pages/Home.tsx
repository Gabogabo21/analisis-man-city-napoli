/**
 * Dirección de diseño: Cámara de datos — un informe táctico editorial en azul noche,
 * con módulos asimétricos, cristal sobrio, trazos de campo y azul de señal #38BDF8.
 */
import { useEffect, useState } from "react";
import {
  Activity,
  ArrowDown,
  ArrowUpRight,
  BarChart3,
  ChevronRight,
  Database,
  FileText,
  Menu,
  MoveRight,
  Radar,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  X,
} from "lucide-react";
import { toast } from "sonner";

const ASSETS = {
  mark: "/manus-storage/iannuzzi-vector-mark_0012d8b3.png",
  hero: "/manus-storage/iannuzzi-hero-tactical-stadium_70006062.png",
  monitor: "/manus-storage/iannuzzi-analysis-monitor_92f655da.png",
  orbit: "/manus-storage/iannuzzi-data-orbit_cf375031.png",
  dataset: "/manus-storage/iannuzzi-dataset-product_222194f0.png",
};

const standings = [
  { short: "INT", club: "Inter", real: 1, xpts: 2, delta: "+1", trend: "down" },
  { short: "NAP", club: "Napoli", real: 2, xpts: 1, delta: "−1", trend: "up" },
  { short: "JUV", club: "Juventus", real: 3, xpts: 4, delta: "+1", trend: "down" },
  { short: "ATA", club: "Atalanta", real: 4, xpts: 3, delta: "−1", trend: "up" },
  { short: "MIL", club: "Milan", real: 5, xpts: 6, delta: "+1", trend: "down" },
];

const matchReports = [
  {
    match: "Inter — Juventus",
    subtitle: "Derby d'Italia · análisis de flujo",
    stat: "0.84",
    label: "xG neto",
    state: "Listo para conectar",
    type: "señal",
  },
  {
    match: "Atalanta — Napoli",
    subtitle: "Secuencias de presión · PPDA",
    stat: "8.7",
    label: "PPDA",
    state: "En cola",
    type: "cola",
  },
  {
    match: "Milan — Roma",
    subtitle: "Balón parado · zonas de remate",
    stat: "31%",
    label: "amenaza SP",
    state: "Próximo informe",
    type: "next",
  },
];

const products = [
  {
    kind: "PDF / 86 PÁGS.",
    title: "Manual de Métricas Avanzadas en la Serie A",
    description:
      "Un marco práctico para leer xG, PPDA, progresiones y contexto táctico sin perder la narrativa del partido.",
    price: "€19",
    art: ASSETS.monitor,
    action: "Ver el manual",
  },
  {
    kind: "XLSX + CSV / ACTUALIZABLE",
    title: "Base de datos acumulada de la temporada",
    description:
      "Una estructura limpia para filtrar rendimiento, fases de juego y perfiles de equipo en tu propio flujo de trabajo.",
    price: "€29",
    art: ASSETS.dataset,
    action: "Explorar dataset",
  },
];

function scrollToId(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function VectorMark({ size = "small" }: { size?: "small" | "large" }) {
  return (
    <div className={`vector-mark vector-mark--${size}`} aria-label="Iannuzzi Data">
      <img className="vector-source" src={ASSETS.mark} alt="" />
      <svg className="vector-drawing" viewBox="0 0 48 48" aria-hidden="true">
        <path d="M8 37 20.5 11 31 23 41 8" />
        <path d="m9 13 11.5 24 10.5-12 9 15" />
        <circle cx="25" cy="24" r="3.1" />
      </svg>
    </div>
  );
}

function MetricSparkline({ color = "blue" }: { color?: "blue" | "green" | "gold" }) {
  return (
    <svg className={`sparkline sparkline--${color}`} viewBox="0 0 132 40" aria-hidden="true">
      <path d="M1 32C14 31 14 21 29 24C42 27 44 12 58 17C70 21 77 28 86 16C96 4 106 15 117 9C124 5 128 3 131 4" />
      <circle cx="131" cy="4" r="2.8" />
    </svg>
  );
}

export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setIsScrolled(window.scrollY > 18);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const navigate = (id: string) => {
    setIsMenuOpen(false);
    scrollToId(id);
  };

  const unavailableCheckout = (name: string) => {
    toast("Enlace de compra pendiente", {
      description: `${name}: conecta aquí tu URL de Gumroad o Payhip para habilitar el checkout.`,
    });
  };

  return (
    <div className="site-shell">
      <header className={`site-header ${isScrolled ? "site-header--scrolled" : ""}`}>
        <a className="brand" href="#inicio" aria-label="Iannuzzi Data, inicio">
          <VectorMark />
          <span className="brand-name">IANNUZZI <i>DATA</i></span>
        </a>

        <nav className="desktop-nav" aria-label="Navegación principal">
          <button onClick={() => navigate("clasificacion")}>Métricas</button>
          <button onClick={() => navigate("analisis")}>Análisis</button>
          <button onClick={() => navigate("productos")}>Productos</button>
        </nav>

        <div className="header-tools">
          <span className="data-status"><span /> SÉRIE A / LAYER 01</span>
          <button className="nav-cta" onClick={() => navigate("productos")}>Abrir datos <ArrowUpRight size={14} /></button>
          <button
            className="mobile-menu-button"
            aria-label={isMenuOpen ? "Cerrar menú" : "Abrir menú"}
            aria-expanded={isMenuOpen}
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X size={21} /> : <Menu size={21} />}
          </button>
        </div>

        <div className={`mobile-nav ${isMenuOpen ? "mobile-nav--open" : ""}`}>
          <button onClick={() => navigate("clasificacion")}>01 / Métricas</button>
          <button onClick={() => navigate("analisis")}>02 / Análisis</button>
          <button onClick={() => navigate("productos")}>03 / Productos</button>
          <span>IANNUZZI DATA · SERIE A INTELLIGENCE</span>
        </div>
      </header>

      <main id="inicio">
        <section className="hero-section section-frame">
          <div className="hero-image-wrap" aria-hidden="true">
            <img className="hero-image" src={ASSETS.hero} alt="" />
            <div className="hero-scrim" />
            <div className="hero-grid" />
          </div>
          <div className="hero-content">
            <div className="eyebrow hero-eyebrow"><span className="live-dot" /> INTELIGENCIA DE PARTIDO / SERIE A</div>
            <h1>El partido que viste.<br /><em>Los patrones que no.</em></h1>
            <p className="hero-copy">Métricas de xG, presión, mapas de calor y rendimiento acumulado. Una capa de lectura táctica para ver más allá del resultado.</p>
            <div className="hero-actions">
              <button className="button button--signal" onClick={() => navigate("productos")}>Descargar dataset <MoveRight size={17} /></button>
              <button className="text-action" onClick={() => navigate("analisis")}>Ver predicciones <ArrowDown size={16} /></button>
            </div>
          </div>

          <div className="hero-telemetry glass-panel">
            <div className="telemetry-topline"><span>SESIÓN ACTIVA</span><span>01 / 04</span></div>
            <div className="telemetry-score">
              <div><small>ÍNDICE DE LECTURA</small><strong>94<span>.6</span></strong></div>
              <MetricSparkline />
            </div>
            <div className="telemetry-footer"><span>MODELO TÁCTICO</span><b>ESTRUCTURA</b></div>
          </div>

          <div className="delivery-badge"><Sparkles size={13} /> ENTREGA DIGITAL GLOBAL · GRATIS</div>
          <a className="scroll-cue" href="#clasificacion" aria-label="Ir a clasificación comparada"><span>SCROLL TO EXPLORE</span><i><ArrowDown size={14} /></i></a>
        </section>

        <section id="clasificacion" className="comparison-section section-frame">
          <div className="section-intro intro-offset">
            <div className="eyebrow"><span>01</span> / DISTORSIÓN DE TABLA</div>
            <h2>Clasificación real<br />vs. <em>expected points.</em></h2>
            <p>Una lectura comparada de posiciones para revelar rendimiento sostenible y ventaja transitoria. Los valores que aparecen son una vista demostrativa de la interfaz.</p>
          </div>
          <div className="section-side-note">
            <span>VISTA DE PRODUCTO</span>
            <p>Conecta tu proveedor de datos para mostrar la clasificación y las métricas activas de cada jornada.</p>
          </div>

          <div className="comparison-board glass-panel">
            <div className="board-header">
              <div><span className="board-kicker">SERIE A / TABLA COMPARADA</span><h3>Rendimiento vs. resultado</h3></div>
              <div className="legend"><span><i className="legend-up" /> adelanta expectativa</span><span><i className="legend-down" /> queda por debajo</span></div>
            </div>
            <div className="table-head"><span>EQUIPO</span><span>REAL</span><span>xPTS</span><span>Δ</span></div>
            <div className="standing-list">
              {standings.map((team, index) => (
                <div className="standing-row" key={team.short}>
                  <span className="position">0{index + 1}</span>
                  <div className="team-cell"><i className={`club-chip club-chip--${index}`}>{team.short}</i><b>{team.club}</b></div>
                  <span className="numeric">{team.real}</span>
                  <span className="numeric numeric--muted">{team.xpts}</span>
                  <span className={`delta delta--${team.trend}`}>{team.delta}<TrendingUp size={13} /></span>
                </div>
              ))}
            </div>
            <button className="board-footer" onClick={() => navigate("analisis")}>Abrir lectura de la jornada <ChevronRight size={15} /></button>
          </div>
        </section>

        <section className="metrics-section section-frame">
          <div className="metrics-header">
            <div className="eyebrow"><span>02</span> / FOTOGRAMA DE TEMPORADA</div>
            <h2>Tres señales. <em>Una lectura más clara.</em></h2>
            <div className="metric-date">CORTE DE DATOS / CONFIGURABLE<br /><b>SEASON LAYER</b></div>
          </div>
          <div className="metrics-layout">
            <article className="metric-card metric-card--large glass-panel">
              <div className="metric-card-top"><span>EFICIENCIA EFICAZ</span><Activity size={18} /></div>
              <div className="metric-value"><strong>+<small>1.42</small></strong><span>xG DIFF</span></div>
              <div className="metric-team"><i className="club-chip club-chip--0">INT</i><b>Inter</b><span>ÍNDICE DE REFERENCIA</span></div>
              <div className="radial-graphic"><span /><i /><b>+</b></div>
              <MetricSparkline color="blue" />
            </article>
            <article className="metric-card glass-panel">
              <div className="metric-card-top"><span>PRESIÓN ALTA</span><Radar size={18} /></div>
              <div className="metric-value metric-value--small"><strong>8<small>.7</small></strong><span>PPDA</span></div>
              <p>Menos pases permitidos por acción defensiva. Una señal de intensidad, no una sentencia aislada.</p>
              <div className="mini-bars"><i /><i /><i /><i /><i /></div>
              <div className="metric-foot"><span>RANGO DE LIGA</span><b>TOP 4%</b></div>
            </article>
            <article className="metric-card glass-panel metric-card--gold">
              <div className="metric-card-top"><span>BALÓN PARADO</span><Target size={18} /></div>
              <div className="metric-value metric-value--small"><strong>31<small>%</small></strong><span>GOLES SP</span></div>
              <p>Proporción del impacto ofensivo originado en córners y tiros libres.</p>
              <div className="pitch-mini"><span /><span /><span /></div>
              <div className="metric-foot"><span>ESTADO</span><b>ALTA AMENAZA</b></div>
            </article>
          </div>
        </section>

        <section id="analisis" className="analysis-section section-frame">
          <div className="analysis-art" aria-hidden="true"><img src={ASSETS.orbit} alt="" /></div>
          <div className="analysis-copy">
            <div className="eyebrow"><span>03</span> / REGISTRO DE PARTIDOS</div>
            <h2>Del partido<br />al <em>patrón.</em></h2>
            <p>Un feed diseñado para ordenar los informes de tu flujo n8n + Gemini: contexto, hipótesis, gráficas y acciones que merecen volver a mirar.</p>
            <div className="engine-note"><span><Database size={15} /> PIPELINE READY</span><span><ShieldCheck size={15} /> FUENTES TRAZABLES</span></div>
          </div>
          <div className="reports-stack">
            {matchReports.map((report, index) => (
              <button className={`report-card report-card--${report.type}`} key={report.match} onClick={() => toast("Informe por conectar", { description: `El módulo «${report.match}» está preparado para recibir la salida de tu automatización.` })}>
                <span className="report-index">0{index + 1}</span>
                <div className="report-info"><b>{report.match}</b><span>{report.subtitle}</span></div>
                <div className="report-stat"><strong>{report.stat}</strong><span>{report.label}</span></div>
                <div className="report-state"><i />{report.state}</div>
                <ArrowUpRight className="report-arrow" size={17} />
              </button>
            ))}
            <p className="report-caption">Los informes y resultados se activan al conectar el origen de datos y el flujo de automatización.</p>
          </div>
        </section>

        <section id="productos" className="products-section section-frame">
          <div className="products-intro">
            <div className="eyebrow"><span>04</span> / PRODUCTOS DIGITALES</div>
            <h2>Tu lectura,<br /><em>en tu sistema.</em></h2>
            <p>Guías y datos para convertir observación en un método propio, en el formato que se adapta a tu flujo.</p>
          </div>
          <div className="product-list">
            {products.map((product, index) => (
              <article className="product-card" key={product.title}>
                <div className={`product-image product-image--${index}`}><img src={product.art} alt="" /><span>{product.kind}</span><div className="image-number">0{index + 1}</div></div>
                <div className="product-content">
                  <h3>{product.title}</h3>
                  <p>{product.description}</p>
                  <div className="product-bottom"><strong>{product.price}</strong><button onClick={() => unavailableCheckout(product.title)}>{product.action}<ArrowUpRight size={16} /></button></div>
                </div>
              </article>
            ))}
          </div>
          <div className="product-note"><FileText size={16} /><span>LICENCIA PERSONAL · ENTREGA DIGITAL INMEDIATA · FORMATO EDITABLE DONDE SE INDIQUE</span></div>
        </section>

        <section className="closing-section section-frame">
          <div className="closing-line" />
          <VectorMark size="large" />
          <p>El fútbol tiene demasiadas cosas ocurriendo a la vez.<br /><b>Iannuzzi Data te ayuda a decidir qué merece tu atención.</b></p>
          <button className="button button--ghost" onClick={() => scrollToId("inicio")}>Volver al inicio <ArrowUpRight size={17} /></button>
        </section>
      </main>

      <footer className="site-footer section-frame">
        <div className="footer-brand"><VectorMark /><span>IANNUZZI DATA</span></div>
        <span>© 2026 · FOOTBALL INTELLIGENCE SYSTEM</span>
        <span>BUILT FOR THE NEXT READ</span>
      </footer>
    </div>
  );
}
