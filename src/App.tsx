import { Routes, Route } from 'react-router'
import SiteHeader from './components/SiteHeader'
import Home from './pages/Home'
import DatabasePage from './pages/Database'
import PubChemPage from './pages/PubChem'
import KitchenPage from './pages/Kitchen'
import VitaminsPage from './pages/Vitamins'
import AminoAcidsPage from './pages/AminoAcids'
import TeachingPage from './pages/Teaching'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <SiteHeader />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/database" element={<DatabasePage />} />
        <Route path="/pubchem" element={<PubChemPage />} />
        <Route path="/kitchen" element={<KitchenPage />} />
        <Route path="/vitamins" element={<VitaminsPage />} />
        <Route path="/amino-acids" element={<AminoAcidsPage />} />
        <Route path="/teaching" element={<TeachingPage />} />
      </Routes>
      <footer className="border-t bg-white">
        <div className="mx-auto max-w-6xl px-4 py-6 text-center text-xs text-slate-400">
          生活中的化学 · 面向高中化学生活情境教学 · 内容为科普整理，涉及危险品操作请以产品说明与法规为准
        </div>
      </footer>
    </div>
  )
}
