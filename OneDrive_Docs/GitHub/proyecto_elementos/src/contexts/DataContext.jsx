import { createContext, useContext, useState, useEffect } from 'react'

const DataContext = createContext()
const API_URL = 'http://localhost:3001/api'

export const useData = () => {
  const context = useContext(DataContext)
  if (!context) {
    throw new Error('useData debe ser usado dentro de DataProvider')
  }
  return context
}

export const DataProvider = ({ children }) => {
  const [bienes, setBienes] = useState([])
  const [cuentadantes, setCuentadantes] = useState([])
  const [movimientos, setMovimientos] = useState([])
  const [stats, setStats] = useState({
    totalBienes: 0,
    entradasHoy: 0,
    salidasHoy: 0,
    alertas: 0
  })
  const [loading, setLoading] = useState(true)

  // Cargar datos desde la API
  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      
      // Cargar bienes
      const bienesRes = await fetch(`${API_URL}/bienes`)
      const bienesData = await bienesRes.json()
      setBienes(bienesData)
      
      // Cargar cuentadantes
      const cuentadantesRes = await fetch(`${API_URL}/cuentadantes`)
      const cuentadantesData = await cuentadantesRes.json()
      
      // Transformar datos para que coincidan con la estructura esperada por los componentes
      const cuentadantesTransformados = cuentadantesData.map(c => ({
        id: c.id || c.pers_documento,
        cedula: c.pers_documento,
        nombre: `${c.pers_nombres} ${c.pers_apellidos}`,
        cargo: c.roles && c.roles.length > 0 ? c.roles[0] : 'Sin rol',
        area: c.pers_direccion || 'Sin área',
        activo: true,
        correo: c.pers_correo,
        telefono: c.pers_telefono,
        pers_nombres: c.pers_nombres,
        pers_apellidos: c.pers_apellidos,
        pers_documento: c.pers_documento,
        pers_tipodoc: c.pers_tipodoc,
        roles: c.roles
      }))
      
      setCuentadantes(cuentadantesTransformados)
      
      // Cargar asignaciones
      const asignacionesRes = await fetch(`${API_URL}/asignaciones`)
      const asignacionesData = await asignacionesRes.json()
      setMovimientos(asignacionesData)
      
      // Actualizar stats
      setStats({
        totalBienes: bienesData.length,
        entradasHoy: 0,
        salidasHoy: 0,
        alertas: 0
      })
    } catch (error) {
      console.error('Error al cargar datos:', error)
      // Fallback a datos mock si falla la API
      loadMockData()
    } finally {
      setLoading(false)
    }
  }

  const loadMockData = () => {
    const mockBienes = [
      {
        id: 1,
        codigo: 'HP-2024-001',
        descripcion: 'Computador HP EliteBook 840',
        categoria: 'Computadores',
        estado: 'disponible',
        fechaIngreso: '2024-01-15',
        valor: 2500000,
        ubicacion: 'Almacén Principal'
      },
      {
        id: 2,
        codigo: 'EPSON-2023-045',
        descripcion: 'Proyector EPSON PowerLite',
        categoria: 'Proyectores',
        estado: 'asignado',
        fechaIngreso: '2023-08-20',
        valor: 1800000,
        ubicacion: 'Aula 201',
        cuentadante: 'María González',
        fechaAsignacion: '2024-10-15'
      },
      {
        id: 3,
        codigo: 'CANON-2024-012',
        descripcion: 'Impresora Canon ImageClass',
        categoria: 'Impresoras',
        estado: 'disponible',
        fechaIngreso: '2024-02-10',
        valor: 800000,
        ubicacion: 'Almacén Principal'
      },
      {
        id: 4,
        codigo: 'DELL-2024-015',
        descripcion: 'Monitor DELL UltraSharp 27"',
        categoria: 'Monitores',
        estado: 'disponible',
        fechaIngreso: '2024-03-05',
        valor: 1200000,
        ubicacion: 'Almacén Principal'
      },
      {
        id: 5,
        codigo: 'LOGITECH-2024-020',
        descripcion: 'Teclado y Mouse Logitech MK850',
        categoria: 'Periféricos',
        estado: 'disponible',
        fechaIngreso: '2024-03-10',
        valor: 250000,
        ubicacion: 'Almacén Principal'
      },
      {
        id: 6,
        codigo: 'CISCO-2024-008',
        descripcion: 'Router Cisco RV340',
        categoria: 'Redes',
        estado: 'disponible',
        fechaIngreso: '2024-02-20',
        valor: 1500000,
        ubicacion: 'Almacén Principal'
      },
      {
        id: 7,
        codigo: 'LENOVO-2024-003',
        descripcion: 'Tablet Lenovo Tab M10',
        categoria: 'Tablets',
        estado: 'disponible',
        fechaIngreso: '2024-01-25',
        valor: 800000,
        ubicacion: 'Almacén Principal'
      },
      {
        id: 8,
        codigo: 'HP-2023-089',
        descripcion: 'Laptop HP Pavilion 15',
        categoria: 'Computadores',
        estado: 'asignado',
        fechaIngreso: '2023-11-10',
        valor: 2200000,
        ubicacion: 'Oficina Instructores',
        cuentadante: 'Carlos Rodríguez',
        fechaAsignacion: '2024-09-20'
      }
    ]

    const mockCuentadantes = [
      {
        id: 1,
        cedula: '12345678',
        nombre: 'María González',
        cargo: 'Coordinadora Académica',
        area: 'Coordinación',
        activo: true,
        correo: 'maria.gonzalez@sena.edu.co',
        telefono: '3001234567'
      },
      {
        id: 2,
        cedula: '87654321',
        nombre: 'Carlos Rodríguez',
        cargo: 'Instructor',
        area: 'Sistemas',
        activo: true,
        correo: 'carlos.rodriguez@sena.edu.co',
        telefono: '3007654321'
      },
      {
        id: 3,
        cedula: '11223344',
        nombre: 'Ana Martínez',
        cargo: 'Instructora',
        area: 'Diseño',
        activo: true,
        correo: 'ana.martinez@sena.edu.co',
        telefono: '3009876543'
      },
      {
        id: 4,
        cedula: '55667788',
        nombre: 'Luis Pérez',
        cargo: 'Coordinador',
        area: 'Logística',
        activo: true,
        correo: 'luis.perez@sena.edu.co',
        telefono: '3005554321'
      }
    ]

    const mockMovimientos = [
      {
        id: 1,
        tipo: 'asignacion',
        fecha: '2024-10-15T10:30:00',
        bienes: [2],
        bienesInfo: ['EPSON-2023-045 - Proyector EPSON PowerLite'],
        cuentadante: 'María González',
        descripcion: 'Asignación de 1 bien a María González'
      },
      {
        id: 2,
        tipo: 'asignacion',
        fecha: '2024-09-20T14:15:00',
        bienes: [8],
        bienesInfo: ['HP-2023-089 - Laptop HP Pavilion 15'],
        cuentadante: 'Carlos Rodríguez',
        descripcion: 'Asignación de 1 bien a Carlos Rodríguez'
      }
    ]

    setBienes(mockBienes)
    setCuentadantes(mockCuentadantes)
    setMovimientos(mockMovimientos)
    
    setStats({
      totalBienes: mockBienes.length,
      entradasHoy: 125,
      salidasHoy: 98,
      alertas: 7
    })
  }

  const addBien = async (bien) => {
    try {
      const response = await fetch(`${API_URL}/bienes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bien)
      })
      
      if (response.ok) {
        const newBien = await response.json()
        setBienes(prev => [...prev, newBien])
        setStats(prev => ({ ...prev, totalBienes: prev.totalBienes + 1 }))
        return newBien
      }
    } catch (error) {
      console.error('Error al agregar bien:', error)
      throw error
    }
  }

  const updateBien = async (id, updates) => {
    try {
      const response = await fetch(`${API_URL}/bienes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Error al actualizar bien')
      }
      
      const updatedBien = await response.json()
      
      // Actualizar el estado local con el bien actualizado
      setBienes(prev => prev.map(bien => 
        bien.id === id ? { ...bien, ...updatedBien } : bien
      ))
      
      return updatedBien
    } catch (error) {
      console.error('Error al actualizar bien:', error)
      throw error
    }
  }

  const addCuentadante = async (cuentadante) => {
    try {
      const response = await fetch(`${API_URL}/cuentadantes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cuentadante)
      })
      
      if (response.ok) {
        const newCuentadante = await response.json()
        setCuentadantes(prev => [...prev, newCuentadante])
        return newCuentadante
      }
    } catch (error) {
      console.error('Error al agregar cuentadante:', error)
      throw error
    }
  }

  const assignBienes = async (bienesIds, cuentadanteId) => {
    try {
      const response = await fetch(`${API_URL}/asignaciones`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bienesIds, cuentadanteId })
      })
      
      if (response.ok) {
        // Recargar datos
        await loadData()
        return true
      }
      return false
    } catch (error) {
      console.error('Error al asignar bienes:', error)
      return false
    }
  }

  const desasignarBien = async (bienId) => {
    try {
      const response = await fetch(`${API_URL}/bienes/${bienId}/desasignar`, {
        method: 'POST'
      })
      
      if (response.ok) {
        // Recargar datos
        await loadData()
      }
    } catch (error) {
      console.error('Error al desasignar bien:', error)
      throw error
    }
  }

  const value = {
    bienes,
    cuentadantes,
    movimientos,
    stats,
    loading,
    addBien,
    updateBien,
    addCuentadante,
    assignBienes,
    desasignarBien,
    refreshData: loadData
  }

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  )
}