import { Package } from "lucide-react";
import { fmtRp } from "@/lib/api.js";

export default function Products() {
  const products = [];

  return (
    <section>
      <header className="mb-6">
        <h1 className="text-xl font-semibold">Katalog Produk</h1>
        <p className="text-sm text-slate-500">Daftar barang beserta stok tersedia.</p>
      </header>

      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">Nama Produk</th>
              <th className="px-4 py-3 font-medium">Satuan</th>
              <th className="px-4 py-3 font-medium">Harga</th>
              <th className="px-4 py-3 text-right font-medium">Stok</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {products.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-12 text-center text-slate-500">
                  <Package size={28} className="mx-auto mb-2 text-slate-300" aria-hidden="true" />
                  Belum ada produk. Data akan dimuat dari backend stok.
                </td>
              </tr>
            ) : (
              products.map((p) => (
                <tr key={p.id}>
                  <td className="px-4 py-3">{p.name}</td>
                  <td className="px-4 py-3 text-slate-600">{p.unit}</td>
                  <td className="px-4 py-3">{fmtRp(p.price)}</td>
                  <td className="px-4 py-3 text-right font-medium">{p.stock}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
