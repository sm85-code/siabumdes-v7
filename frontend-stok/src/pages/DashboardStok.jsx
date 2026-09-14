import { Package, ArrowDownToLine, ArrowUpFromLine, AlertTriangle } from "lucide-react";

const STATS = [
  { label: "Total Produk", value: "—", icon: Package, tone: "text-brand-dark bg-brand-light" },
  { label: "Stok Masuk (bulan ini)", value: "—", icon: ArrowDownToLine, tone: "text-emerald-700 bg-emerald-50" },
  { label: "Stok Keluar (bulan ini)", value: "—", icon: ArrowUpFromLine, tone: "text-amber-700 bg-amber-50" },
  { label: "Stok Menipis", value: "—", icon: AlertTriangle, tone: "text-red-700 bg-red-50" },
];

export default function DashboardStok() {
  return (
    <section>
      <header className="mb-6">
        <h1 className="text-xl font-semibold">Dashboard Stok</h1>
        <p className="text-sm text-slate-500">Ringkasan pergerakan dan ketersediaan barang.</p>
      </header>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {STATS.map(({ label, value, icon: Icon, tone }) => (
          <div key={label} className="rounded-xl border border-slate-200 bg-white p-5">
            <div className={`mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg ${tone}`}>
              <Icon size={20} aria-hidden="true" />
            </div>
            <p className="text-2xl font-semibold">{value}</p>
            <p className="text-sm text-slate-500">{label}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">
        Data ringkasan akan tampil setelah endpoint stok backend terhubung.
      </div>
    </section>
  );
}
