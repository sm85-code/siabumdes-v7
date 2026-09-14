import { ArrowLeftRight, ArrowDownToLine, ArrowUpFromLine } from "lucide-react";
import { fmtDateTime } from "@/lib/api.js";

export default function Mutasi() {
  const logs = [];

  return (
    <section>
      <header className="mb-6">
        <h1 className="text-xl font-semibold">Mutasi Stok</h1>
        <p className="text-sm text-slate-500">Riwayat stok masuk dan keluar.</p>
      </header>

      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">Waktu</th>
              <th className="px-4 py-3 font-medium">Produk</th>
              <th className="px-4 py-3 font-medium">Jenis</th>
              <th className="px-4 py-3 text-right font-medium">Jumlah</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {logs.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-12 text-center text-slate-500">
                  <ArrowLeftRight size={28} className="mx-auto mb-2 text-slate-300" aria-hidden="true" />
                  Belum ada mutasi. Data akan dimuat dari backend stok.
                </td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id}>
                  <td className="px-4 py-3 text-slate-600">{fmtDateTime(log.created_at)}</td>
                  <td className="px-4 py-3">{log.product_name}</td>
                  <td className="px-4 py-3">
                    {log.type === "in" ? (
                      <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-700">
                        <ArrowDownToLine size={12} aria-hidden="true" /> Masuk
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">
                        <ArrowUpFromLine size={12} aria-hidden="true" /> Keluar
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-right font-medium">{log.quantity}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
