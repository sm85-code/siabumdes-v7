"""Initial seed data: Chart of Accounts (Kepmendesa 136/2022) + 6 Unit Usaha + default users."""

# Chart of Accounts BUMDES sesuai Kepmendesa PDTT No 136 Tahun 2022
# Single source of truth for account validation and import templates.
# Keep these identifiers stable: reporting logic uses the subcategory values directly.
VALID_ACCOUNT_CATEGORIES = {
    "aset": ("kas_bank", "aset_lancar", "aset_tetap"),
    "kewajiban": ("kewajiban_jangka_pendek", "kewajiban_jangka_panjang"),
    "ekuitas": ("modal_desa", "modal_masyarakat", "saldo_laba", "bagi_hasil_desa", "bagi_hasil_masyarakat"),
    "pendapatan": ("pendapatan_operasional", "pendapatan_non_operasional"),
    "beban": ("beban_operasional", "beban_administrasi", "beban_lain_lain"),
}

# Compatibility name used by account template/import code.
VALID_CATEGORIES = VALID_ACCOUNT_CATEGORIES

# code, name, category, subcategory, normal_balance
CHART_OF_ACCOUNTS = [
    # ============ ASET (1) ============
    ("1.1.01.01", "Kas", "aset", "kas_bank", "debit"),
    ("1.1.01.02", "Bank", "aset", "kas_bank", "debit"),
    ("1.1.01.03", "Piutang Usaha", "aset", "aset_lancar", "debit"),
    ("1.1.01.04", "Piutang Mitra Peternak", "aset", "aset_lancar", "debit"),
    ("1.1.01.05", "Piutang Bagi Hasil", "aset", "aset_lancar", "debit"),
    ("1.1.01.06", "Persediaan Barang Dagangan", "aset", "aset_lancar", "debit"),
    ("1.1.01.07", "Persediaan Domba Bibit", "aset", "aset_lancar", "debit"),
    ("1.1.01.08", "Persediaan Bibit Ikan", "aset", "aset_lancar", "debit"),
    ("1.1.01.09", "Modal Yang Dititipkan ke Mitra", "aset", "aset_lancar", "debit"),
    ("1.1.01.10", "Uang Muka & Beban Dibayar Dimuka", "aset", "aset_lancar", "debit"),
    ("1.1.02.01", "Kendaraan Angkutan", "aset", "aset_tetap", "debit"),
    ("1.1.02.02", "Peralatan Kolam Bioflok", "aset", "aset_tetap", "debit"),
    ("1.1.02.03", "Peralatan Toko", "aset", "aset_tetap", "debit"),
    ("1.1.02.04", "Peralatan Kantor", "aset", "aset_tetap", "debit"),
    ("1.1.02.05", "Bangunan Kandang & Toko", "aset", "aset_tetap", "debit"),
    ("1.1.02.99", "Akumulasi Penyusutan Aset Tetap", "aset", "aset_tetap", "kredit"),

    # ============ KEWAJIBAN (2) ============
    ("2.1.01.01", "Utang Usaha", "kewajiban", "kewajiban_jangka_pendek", "kredit"),
    ("2.1.01.02", "Utang Bagi Hasil Pengelola", "kewajiban", "kewajiban_jangka_pendek", "kredit"),
    ("2.1.01.03", "Utang Bagi Hasil Mitra", "kewajiban", "kewajiban_jangka_pendek", "kredit"),
    ("2.1.01.04", "Beban Yang Masih Harus Dibayar", "kewajiban", "kewajiban_jangka_pendek", "kredit"),
    ("2.2.01.01", "Utang Jangka Panjang", "kewajiban", "kewajiban_jangka_panjang", "kredit"),

    # ============ EKUITAS (3) ============
    ("3.1.01.01", "Modal Penyertaan Desa", "ekuitas", "modal_desa", "kredit"),
    ("3.1.01.02", "Modal Penyertaan Masyarakat", "ekuitas", "modal_masyarakat", "kredit"),
    ("3.2.01.01", "Laba Ditahan", "ekuitas", "saldo_laba", "kredit"),
    ("3.2.01.02", "Laba/Rugi Tahun Berjalan", "ekuitas", "saldo_laba", "kredit"),
    ("3.2.01.03", "Cadangan Umum", "ekuitas", "saldo_laba", "kredit"),
    ("3.2.01.04", "Dana Sosial & CSR", "ekuitas", "saldo_laba", "kredit"),
    ("3.2.02.01", "Bagi Hasil untuk Desa", "ekuitas", "bagi_hasil_desa", "debit"),
    ("3.2.02.02", "Bagi Hasil untuk Masyarakat", "ekuitas", "bagi_hasil_masyarakat", "debit"),

    # ============ PENDAPATAN (4) - per unit usaha ============
    ("4.1.01.01", "Pendapatan Unit Pembibitan Domba", "pendapatan", "pendapatan_operasional", "kredit"),
    ("4.1.01.02", "Pendapatan Unit Ikan Mujaer Bioflok", "pendapatan", "pendapatan_operasional", "kredit"),
    ("4.1.01.03", "Pendapatan Unit Sewa Angkutan", "pendapatan", "pendapatan_operasional", "kredit"),
    ("4.1.01.04", "Pendapatan Unit Perdagangan & Produksi", "pendapatan", "pendapatan_operasional", "kredit"),
    ("4.1.01.05", "Pendapatan Unit Toko Offline", "pendapatan", "pendapatan_operasional", "kredit"),
    ("4.1.01.06", "Pendapatan Unit Toko Online", "pendapatan", "pendapatan_operasional", "kredit"),
    ("4.2.01.01", "Pendapatan Lain-lain", "pendapatan", "pendapatan_non_operasional", "kredit"),
    ("4.2.01.02", "Pendapatan Bunga Bank", "pendapatan", "pendapatan_non_operasional", "kredit"),

    # ============ BEBAN (5) ============
    ("5.1.01.01", "Beban Bagi Hasil Mitra Peternak Domba", "beban", "beban_operasional", "debit"),
    ("5.1.01.02", "Beban Bagi Hasil Mitra Peternak Ikan", "beban", "beban_operasional", "debit"),
    ("5.1.01.03", "Beban Bagi Hasil Pengelola Unit Usaha", "beban", "beban_operasional", "debit"),
    ("5.1.02.01", "Beban BBM & Transportasi Monitoring", "beban", "beban_operasional", "debit"),
    ("5.1.02.02", "Beban BBM Angkutan Barang", "beban", "beban_operasional", "debit"),
    ("5.1.02.03", "Beban ATK", "beban", "beban_operasional", "debit"),
    ("5.1.02.04", "Beban Packing", "beban", "beban_operasional", "debit"),
    ("5.1.02.05", "Beban Pickup Ekspedisi", "beban", "beban_operasional", "debit"),
    ("5.1.02.06", "Beban Gaji Karyawan Toko Online", "beban", "beban_operasional", "debit"),
    ("5.1.02.07", "Beban Listrik", "beban", "beban_operasional", "debit"),
    ("5.1.02.08", "Beban PDAM (Air)", "beban", "beban_operasional", "debit"),
    ("5.1.02.09", "Beban Wifi/Internet", "beban", "beban_operasional", "debit"),
    ("5.1.02.10", "Beban Pakan Ternak", "beban", "beban_operasional", "debit"),
    ("5.1.02.11", "Beban Pemeliharaan Kandang & Kolam", "beban", "beban_operasional", "debit"),
    ("5.1.02.12", "Harga Pokok Penjualan (HPP)", "beban", "beban_operasional", "debit"),
    ("5.2.01.01", "Beban Administrasi & Umum", "beban", "beban_administrasi", "debit"),
    ("5.2.01.02", "Beban Penyusutan Aset Tetap", "beban", "beban_administrasi", "debit"),
    ("5.2.01.03", "Beban Rapat & Konsumsi", "beban", "beban_administrasi", "debit"),
    ("5.3.01.01", "Beban Pajak", "beban", "beban_lain_lain", "debit"),
]

UNIT_USAHA_SEED = [
    ("UU01", "Pembibitan Domba Garut",
     "Kerjasama dengan ~15 mitra peternak domba di desa. Pengelola monitoring bulanan.",
     "Anakan dijual: 30% mitra, 70% BUMDES. Akumulasi 70% dikurangi op-cost, sisa dibagi 30% pengelola / 70% BUMDES."),
    ("UU02", "Ternak Ikan Mujaer Bioflok",
     "Kerjasama dengan ~24 mitra peternak ikan mujaer sistem bioflok.",
     "Mitra setor Rp3.000/kg ikan panen. Akumulasi dikurangi op-cost, sisa dibagi 30% pengelola / 70% BUMDES."),
    ("UU03", "Sewa Kendaraan Angkutan Barang",
     "Antar barang dari penjual online (affiliasi) dan pihak lain di lingkup Kec. Pangandaran.",
     "Uang jasa dikurangi op-cost BBM, sisa dibagi 30% pengelola / 70% BUMDES."),
    ("UU04", "Perdagangan & Produksi Barang Jadi",
     "Kerjasama ~15 mitra usaha (tukang kayu, pengrajin bambu, sapu lidi/ijuk, tanaman hias, supplier makanan, produk rumah tangga, penjual online).",
     "Mitra dititipi modal 1-17 juta, setor imbal hasil 3%/bulan. Akumulasi dibagi 30% pengelola / 70% BUMDES."),
    ("UU05", "Toko Offline BUMDES",
     "Menyediakan produk untuk masyarakat & penjual online.",
     "Laba bersih dikurangi op-cost ATK, sisa dibagi 30% pengelola / 70% BUMDES."),
    ("UU06", "Toko Online BUMDES",
     "Kanal digital: Shopee, Tokopedia, TikTokShop, Lazada, Blibli.",
     "Laba bersih dikurangi op-cost (ATK, packing, pickup, gaji, listrik, PDAM, wifi), sisa dibagi 30% pengelola / 70% BUMDES."),
]
