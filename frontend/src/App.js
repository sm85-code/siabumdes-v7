import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "@/lib/auth";
import Layout from "@/components/Layout";
import Login from "@/pages/Login";
import ChangePassword from "@/pages/ChangePassword";
import ProfilePage from "@/pages/ProfilePage";
import Landing from "@/pages/Landing";
import Dashboard from "@/pages/Dashboard";
import Transactions from "@/pages/Transactions";
import Reports from "@/pages/Reports";
import ReportsPerUnit from "@/pages/ReportsPerUnit";
import BukuBesar from "@/pages/BukuBesar";
import UnitUsahaPage from "@/pages/UnitUsahaPage";
import MitraPage from "@/pages/MitraPage";
import COAPage from "@/pages/COAPage";
import UsersPage from "@/pages/UsersPage";

const ROLES_REPORTS = ["admin", "direktur", "bendahara", "pengelola", "pengawas", "penasihat"];
const ROLES_LEDGER = ["admin", "direktur", "bendahara", "pengelola", "pengawas", "penasihat"];
const ROLES_COA = ["admin", "direktur", "bendahara", "pengawas", "penasihat"];
const ROLES_USERS = ["admin"];

function Protected({ children, roles }) {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) return <div className="min-h-screen flex items-center justify-center text-sm">Memuat...</div>;
  if (!user) return <Navigate to="/login" replace state={{ from: location }} />;
  if (user.must_change_password && location.pathname !== "/change-password") {
    return <Navigate to="/change-password" replace state={{ from: location }} />;
  }
  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />;
  return <Layout>{children}</Layout>;
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/change-password" element={<Protected><ChangePassword /></Protected>} />
            <Route path="/profile" element={<Protected><ProfilePage /></Protected>} />
            <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
            <Route path="/transactions" element={<Protected><Transactions /></Protected>} />
            <Route path="/reports" element={<Protected roles={ROLES_REPORTS}><Reports /></Protected>} />
            <Route path="/reports/per-unit" element={<Protected><ReportsPerUnit /></Protected>} />
            <Route path="/ledger" element={<Protected roles={ROLES_LEDGER}><BukuBesar /></Protected>} />
            <Route path="/unit-usaha" element={<Protected><UnitUsahaPage /></Protected>} />
            <Route path="/mitra" element={<Protected><MitraPage /></Protected>} />
            <Route path="/accounts" element={<Protected roles={ROLES_COA}><COAPage /></Protected>} />
            <Route path="/users" element={<Protected roles={ROLES_USERS}><UsersPage /></Protected>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
