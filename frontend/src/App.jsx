import { BrowserRouter, Routes, Route } from "react-router-dom";

import Welcome from "./pages/Welcome";
import Home from "./pages/Home";
import Status from "./pages/Status";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing page */}
        <Route path="/" element={<Welcome />} />

        {/* Main workspace */}
        <Route path="/home" element={<Home />} />

        {/* System status */}
        <Route path="/status" element={<Status />} />
      </Routes>
    </BrowserRouter>
  );
}
