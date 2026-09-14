import { NavLink, Outlet, Navigate, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Package,
  ArrowLeftRight,
  LogOut,
  Store,
  ShieldAlert,
} from "lucide-react";
import { useAuth } from "@/lib/auth.jsx";
import { ROLE_LABELS } from "@/lib/api.js";

// Unit this operational console belongs to (Unit Toko Offline).
const UNIT_TOKO = "UU05";

// Roles with organization-wide access to the stock console.
const GLOBAL_ROLES = ["admin", "direktur", "bendahara"];

const NAV = [
  { to: "/", label: "Dashboard & Sinkronisasi", icon: LayoutDashboard, end: true },
  { to: "/produk", label: "Master Produk & Harga", icon: Package },
  { to: "/mutasi", label: "Log Mutasi Barang", icon: ArrowLeftRight },
];

// Access is granted to global roles, or to a pengelola assigned to UU05.
function hasUnitAccess(user) {
  if (!user) return false;
  if (GLOBAL_ROLES.includes(user.role)) return true;
  if (user.role === "pengelola") {
    const unit = String(user.unit_usaha_id ?? user.unit ?? "").toUpperCase();
    return unit === UNIT_TOKO;
  }
  return false;
}

function AccessDenied({ user, onLogout }) {
  return (
    <div className="flex min-h-full items-center justify-center bg-slate-50 p-6">
      <div className="w-full max-w-md rounded-2xl border border-red-200 bg-white p-8 text-center shadow-sm">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-red-50 text-red-600">
          <ShieldAlert size={28} aria-hidden="true" />
        </div>
        <h1 className="text-lg font-semibold text-slate-900">Akses Ditolak</h1>
        <p className="mt-2 text-sm text-slate-500">
          Akun Anda tidak memiliki hak akses ke Konsol Operasional Unit Toko Offline (UU05).
          Hubungi administrator jika ini sebuah kekeliruan.
        </p>
        <div className="mt-4 rounded-lg bg-slate-50 px-4 py-3 text-left text-xs text-slate-500">
          <p><span className="font-medium text-slate-700">Pengguna:</span> {user?.name || user?.username || "-"}</p>
          <p><span className="font-medium text-slate-700">Peran:</span> {ROLE_LABELS[user?.role] || user?.role || "-"}</p>
          <p><span className="font-medium text-slate-700">Unit:</span> {user?.unit_usaha_id || "Tidak ditetapkan"}</p>
        </div>
        <button
          type="button"
          onClick={onLogout}
          className="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-slate-700"
        >
          <LogOut size={16} aria-hidden="true" />
          Keluar
        </button>
      </div>
    </div>
  );
}

export default function Layout() {
  const { user, loading, logout } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-slate-500">
        Memeriksa sesi...
      </div>
    );
  }

  // Session enforced by the HttpOnly cookie; redirect unauthenticated users.
  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  // Role-based access control for the UU05 operational console.
  if (!hasUnitAccess(user)) {
    return <AccessDenied user={user} onLogout={logout} />;
  }

  return (
    <div className="flex min-h-full">
      <aside className="flex w-72 flex-col border-r border-slate-800 bg-slate-900 text-slate-100">
        <div className="flex items-start gap-3 border-b border-slate-800 px-5 py-4">
          <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-brand text-white">
            <Store size={18} aria-hidden="true" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-semibold">BUMDes Operasional</p>
            <p className="text-xs text-slate-400">Unit Toko Offline (UU05)</p>
          </div>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {NAV.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-brand text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <Icon size={18} aria-hidden="true" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-slate-800 p-3">
          <div className="mb-2 rounded-lg bg-slate-800/60 px-3 py-2">
            <p className="truncate text-sm font-medium text-white">
              {user.name || user.username}
            </p>
            <div className="mt-1 flex items-center gap-2">
              <span className="inline-flex items-center rounded-full bg-brand/20 px-2 py-0.5 text-[11px] font-medium text-brand-light">
                {ROLE_LABELS[user.role] || user.role}
              </span>
              {user.unit_usaha_id && (
                <span className="inline-flex items-center rounded-full bg-slate-700 px-2 py-0.5 text-[11px] font-medium text-slate-200">
                  {user.unit_usaha_id}
                </span>
              )}
            </div>
          </div>
          <button
            type="button"
            onClick={logout}
            className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-red-300 transition-colors hover:bg-red-500/10 hover:text-red-200"
          >
            <LogOut size={18} aria-hidden="true" />
            Keluar
          </button>
        </div>
      </aside>

      <div className="flex flex-1 flex-col bg-slate-50">
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
