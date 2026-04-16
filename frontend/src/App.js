import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import TrackQuote from "./pages/TrackQuote";
import QuoteStatus from "./pages/QuoteStatus";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/track" element={<TrackQuote />} />
          <Route path="/track/:quoteNumber" element={<QuoteStatus />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
