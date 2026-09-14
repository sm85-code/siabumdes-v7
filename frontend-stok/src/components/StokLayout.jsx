import { NavLink, Outlet, Navigate, useLocation } from "react-router-dom";
import { LayoutDashboard, Package, ArrowLeftRight, LogOut, Boxes } from "lucide-react";
import { useAuth } from "@/lib/auth.jsx";
import { ROLE_LABELS } from "@/lib/api.js";

const NAV = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/produk", label: "Produk", icon: Package },
  { to: "/mutasi", label: "Mutasi Stok", icon: ArrowLeftRight },
];

export default function StokLayout() {
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

  return (
    <div className="flex min-h-full">
      <aside className="flex w-64 flex-col border-r border-slate-200 bg-white">
        <div className="flex items-center gap-2 border-b border-slate-200 px-5 py-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand text-white">
            <Boxes size={20} aria-hidden="true" />
          </div>
          <div>
            <p className="text-sm font-semibold leading-tight">Manajemen Stok</p>
            <p className="text-xs text-slate-500">BUMDes Karya Raharja</p>
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
                    ? "bg-brand-light text-brand-dark"
                    : "text-slate-600 hover:bg-slate-100"
                }`
              }
            >
              <Icon size={18} aria-hidden="true" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-slate-200 p-3">
          <div className="mb-2 px-2">
            <p className="truncate text-sm font-medium">{user.full_name || user.username}</p>
            <p className="text-xs text-slate-500">{ROLE_LABELS[user.role] || user.role}</p>
          </div>
          <button
            type="button"
            onClick={logout}
            className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-red-600 transition-colors hover:bg-red-50"
          >
            <LogOut size={18} aria-hidden="true" />
            Keluar
          </button>
        </div>
      </aside>

      <div className="flex flex-1 flex-col">
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
