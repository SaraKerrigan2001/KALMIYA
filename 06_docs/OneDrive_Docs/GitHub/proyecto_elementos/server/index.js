import express from 'express';
import cors from 'cors';
import { pool } from '../src/config/conexion.js';

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// ============ ENDPOINTS ROLES ============

// GET - Obtener todos los roles
app.get('/api/roles', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT rol_id, rol_nombre
      FROM bd_elementos.rol
      ORDER BY rol_nombre
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener roles:', error);
    res.status(500).json({ error: 'Error al obtener roles' });
  }
});

// POST - Crear nuevo rol
app.post('/api/roles', async (req, res) => {
  const { rol_nombre } = req.body;
  
  try {
    // Generar nuevo ID
    const maxIdResult = await pool.query('SELECT COALESCE(MAX(rol_id), 0) + 1 as new_id FROM bd_elementos.rol');
    const newId = maxIdResult.rows[0].new_id;
    
    const result = await pool.query(`
      INSERT INTO bd_elementos.rol (rol_id, rol_nombre)
      VALUES ($1, $2)
      RETURNING rol_id, rol_nombre
    `, [newId, rol_nombre]);
    
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Error al crear rol:', error);
    res.status(500).json({ error: 'Error al crear rol', details: error.message });
  }
});

// PUT - Actualizar rol
app.put('/api/roles/:id', async (req, res) => {
  const { id } = req.params;
  const { rol_nombre } = req.body;
  
  try {
    const result = await pool.query(`
      UPDATE bd_elementos.rol
      SET rol_nombre = $1
      WHERE rol_id = $2
      RETURNING rol_id, rol_nombre
    `, [rol_nombre, id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Rol no encontrado' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error al actualizar rol:', error);
    res.status(500).json({ error: 'Error al actualizar rol', details: error.message });
  }
});

// ============ ENDPOINTS SEDES ============

// GET - Obtener todas las sedes
app.get('/api/sedes', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT sede_id, sede_nombre
      FROM bd_elementos.sede
      ORDER BY sede_nombre
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener sedes:', error);
    res.status(500).json({ error: 'Error al obtener sedes' });
  }
});

// POST - Crear nueva sede
app.post('/api/sedes', async (req, res) => {
  const { sede_nombre } = req.body;
  
  try {
    // Generar nuevo ID
    const maxIdResult = await pool.query('SELECT COALESCE(MAX(sede_id), 0) + 1 as new_id FROM bd_elementos.sede');
    const newId = maxIdResult.rows[0].new_id;
    
    const result = await pool.query(`
      INSERT INTO bd_elementos.sede (sede_id, sede_nombre)
      VALUES ($1, $2)
      RETURNING sede_id, sede_nombre
    `, [newId, sede_nombre]);
    
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Error al crear sede:', error);
    res.status(500).json({ error: 'Error al crear sede', details: error.message });
  }
});

// PUT - Actualizar sede
app.put('/api/sedes/:id', async (req, res) => {
  const { id } = req.params;
  const { sede_nombre } = req.body;
  
  try {
    const result = await pool.query(`
      UPDATE bd_elementos.sede
      SET sede_nombre = $1
      WHERE sede_id = $2
      RETURNING sede_id, sede_nombre
    `, [sede_nombre, id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Sede no encontrada' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error al actualizar sede:', error);
    res.status(500).json({ error: 'Error al actualizar sede', details: error.message });
  }
});

// ============ ENDPOINTS MARCAS ============

// GET - Obtener todas las marcas
app.get('/api/marcas', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT marc_id, marc_nombre
      FROM bd_elementos.marca
      ORDER BY marc_nombre
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener marcas:', error);
    res.status(500).json({ error: 'Error al obtener marcas' });
  }
});

// ============ ENDPOINTS CUENTADANTES ============

// GET - Obtener todos los cuentadantes (excluye aprendices)
app.get('/api/cuentadantes', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        p.pers_documento as id,
        p.pers_documento,
        p.pers_nombres,
        p.pers_apellidos,
        p.pers_correo,
        p.pers_telefono,
        p.pers_direccion,
        p.pers_tipodoc,
        ARRAY_AGG(DISTINCT r.rol_nombre) FILTER (WHERE r.rol_nombre IS NOT NULL) as roles
      FROM persona p
      LEFT JOIN rol_persona rp ON p.pers_documento = rp.PERSONA_pers_documento
      LEFT JOIN rol r ON rp.ROL_rol_id = r.rol_id
      WHERE p.pers_documento NOT IN (
        SELECT DISTINCT rp2.PERSONA_pers_documento
        FROM rol_persona rp2
        JOIN rol r2 ON rp2.ROL_rol_id = r2.rol_id
        WHERE LOWER(r2.rol_nombre) = 'aprendiz'
      )
      GROUP BY p.pers_documento, p.pers_nombres, p.pers_apellidos, 
               p.pers_correo, p.pers_telefono, p.pers_direccion, p.pers_tipodoc
      ORDER BY p.pers_nombres
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener cuentadantes:', error);
    res.status(500).json({ error: 'Error al obtener cuentadantes' });
  }
});

// POST - Crear nuevo cuentadante
app.post('/api/cuentadantes', async (req, res) => {
  const { 
    pers_documento, 
    pers_nombres, 
    pers_apellidos, 
    pers_direccion, 
    pers_telefono, 
    pers_tipodoc, 
    pers_correo,
    rol_id
  } = req.body;
  
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    // Insertar persona
    const personaResult = await client.query(`
      INSERT INTO persona (
        pers_documento, pers_nombres, pers_apellidos, 
        pers_direccion, pers_telefono, pers_tipodoc, 
        pers_password, pers_correo
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING 
        pers_documento as id,
        pers_documento,
        pers_nombres,
        pers_apellidos,
        pers_direccion,
        pers_telefono,
        pers_tipodoc,
        pers_correo
    `, [
      pers_documento, 
      pers_nombres, 
      pers_apellidos, 
      pers_direccion, 
      pers_telefono, 
      pers_tipodoc, 
      '123456', // password por defecto
      pers_correo
    ]);
    
    // Asignar rol si se proporcionó
    if (rol_id) {
      // Obtener la primera sede disponible
      const sedeResult = await client.query('SELECT sede_id FROM sede LIMIT 1');
      let sedeId = 1;
      
      if (sedeResult.rows.length > 0) {
        sedeId = sedeResult.rows[0].sede_id;
      }
      
      await client.query(`
        INSERT INTO rol_persona (ROL_rol_id, PERSONA_pers_documento, SEDE_sede_id)
        VALUES ($1, $2, $3)
      `, [rol_id, pers_documento, sedeId]);
    }
    
    await client.query('COMMIT');
    res.status(201).json(personaResult.rows[0]);
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Error al crear cuentadante:', error);
    res.status(500).json({ error: 'Error al crear cuentadante', details: error.message });
  } finally {
    client.release();
  }
});

// ============ ENDPOINTS BIENES ============

// GET - Obtener todos los bienes
app.get('/api/bienes', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        e.elem_placa as id,
        e.elem_placa as codigo,
        e.elem_descripcion as descripcion,
        m.marc_nombre as categoria,
        e.elem_modelo as modelo,
        e.elem_serial as serial,
        e.elem_fecha_compra as "fechaIngreso",
        e.elem_fecha_compra as "fechaCreacion",
        e.elem_costo as valor,
        e.elem_vida_util as "vidaUtil",
        COALESCE(amb.amb_nombre, 'Almacén Principal') as ubicacion,
        CASE 
          WHEN a.disponible = 1 THEN 'disponible'
          WHEN a.disponible = 0 THEN 'asignado'
          ELSE 'disponible'
        END as estado,
        CONCAT(p.pers_nombres, ' ', p.pers_apellidos) as cuentadante,
        a.asig_fecha_ini as "fechaAsignacion"
      FROM elemento e
      LEFT JOIN marca m ON e.MARCA_marc_id = m.marc_id
      LEFT JOIN asignacion a ON e.elem_placa = a.ELEMENTO_elem_placa
      LEFT JOIN ambiente amb ON a.AMBIENTE_amb_id = amb.amb_id
      LEFT JOIN persona p ON a.PERSONA_pers_documento = p.pers_documento
      ORDER BY e.elem_placa DESC
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener bienes:', error);
    res.status(500).json({ error: 'Error al obtener bienes' });
  }
});

// POST - Crear nuevo bien
app.post('/api/bienes', async (req, res) => {
  const { 
    codigo, 
    descripcion, 
    modelo, 
    categoria,  // marc_id
    serial, 
    fechaCompra, 
    vidaUtil, 
    costo 
  } = req.body;
  
  try {
    // Validar que categoria sea un marc_id válido existente en la tabla MARCA
    const marcaResult = await pool.query(
      'SELECT marc_id, marc_nombre FROM marca WHERE marc_id = $1',
      [categoria]
    );
    
    if (marcaResult.rows.length === 0) {
      return res.status(400).json({ 
        error: 'Categoría inválida', 
        details: 'El marc_id proporcionado no existe en la tabla MARCA' 
      });
    }
    
    // Insertar el bien con todos los campos
    const result = await pool.query(`
      INSERT INTO elemento (
        elem_placa, elem_descripcion, elem_modelo, 
        MARCA_marc_id, elem_serial, elem_fecha_compra, 
        elem_vida_util, elem_costo
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING 
        elem_placa as id,
        elem_placa as codigo,
        elem_descripcion as descripcion,
        elem_modelo as modelo,
        elem_serial as serial,
        elem_fecha_compra as "fechaIngreso",
        elem_vida_util as "vidaUtil",
        elem_costo as costo
    `, [codigo, descripcion, modelo, categoria, serial, fechaCompra, vidaUtil, costo]);
    
    // Retornar el bien creado con todos sus campos
    res.status(201).json({
      ...result.rows[0],
      categoria: marcaResult.rows[0].marc_nombre,
      valor: result.rows[0].costo,  // Alias para compatibilidad
      estado: 'disponible',
      ubicacion: 'Almacén Principal'
    });
  } catch (error) {
    console.error('Error al crear bien:', error);
    res.status(500).json({ 
      error: 'Error al crear bien', 
      details: error.message 
    });
  }
});

// PUT - Actualizar bien existente
app.put('/api/bienes/:id', async (req, res) => {
  const { id } = req.params;
  const { 
    descripcion, 
    modelo, 
    categoria,  // marc_id
    serial, 
    fechaCompra, 
    vidaUtil, 
    costo 
  } = req.body;
  
  try {
    // Validar que categoria sea un marc_id válido existente en la tabla MARCA
    const marcaResult = await pool.query(
      'SELECT marc_id, marc_nombre FROM marca WHERE marc_id = $1',
      [categoria]
    );
    
    if (marcaResult.rows.length === 0) {
      return res.status(400).json({ 
        error: 'Categoría inválida', 
        details: 'El marc_id proporcionado no existe en la tabla MARCA' 
      });
    }
    
    // Actualizar el registro en la tabla ELEMENTO usando elem_placa como identificador
    const result = await pool.query(`
      UPDATE elemento
      SET elem_descripcion = $1,
          elem_modelo = $2,
          MARCA_marc_id = $3,
          elem_serial = $4,
          elem_fecha_compra = $5,
          elem_vida_util = $6,
          elem_costo = $7
      WHERE elem_placa = $8
      RETURNING 
        elem_placa as id,
        elem_placa as codigo,
        elem_descripcion as descripcion,
        elem_modelo as modelo,
        elem_serial as serial,
        elem_fecha_compra as "fechaIngreso",
        elem_vida_util as "vidaUtil",
        elem_costo as costo
    `, [descripcion, modelo, categoria, serial, fechaCompra, vidaUtil, costo, id]);
    
    // Retornar error 404 si no existe
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Bien no encontrado' });
    }
    
    // Retornar el bien actualizado
    res.json({
      ...result.rows[0],
      categoria: marcaResult.rows[0].marc_nombre,
      valor: result.rows[0].costo,  // Alias para compatibilidad
      estado: 'disponible',
      ubicacion: 'Almacén Principal'
    });
  } catch (error) {
    console.error('Error al actualizar bien:', error);
    res.status(500).json({ 
      error: 'Error al actualizar bien', 
      details: error.message 
    });
  }
});

// ============ ENDPOINTS ASIGNACIONES ============

// GET - Obtener todas las asignaciones
app.get('/api/asignaciones', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        a.asig_id as id,
        'asignacion' as tipo,
        a.asig_fecha_ini as fecha,
        ARRAY[a.ELEMENTO_elem_placa] as bienes,
        ARRAY[CONCAT(e.elem_placa, ' - ', e.elem_descripcion)] as "bienesInfo",
        CONCAT(p.pers_nombres, ' ', p.pers_apellidos) as cuentadante,
        CONCAT('Asignación de 1 bien a ', p.pers_nombres, ' ', p.pers_apellidos) as descripcion,
        jsonb_build_object(
          'cedula', p.pers_documento,
          'cargo', 'N/A',
          'area', p.pers_direccion
        ) as "cuentadanteInfo"
      FROM asignacion a
      JOIN elemento e ON a.ELEMENTO_elem_placa = e.elem_placa
      JOIN persona p ON a.PERSONA_pers_documento = p.pers_documento
      ORDER BY a.asig_fecha_ini DESC
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error al obtener asignaciones:', error);
    res.status(500).json({ error: 'Error al obtener asignaciones' });
  }
});

// POST - Crear nueva asignación
app.post('/api/asignaciones', async (req, res) => {
  const { bienesIds, cuentadanteId } = req.body;
  
  try {
    // Obtener ambiente por defecto (crear uno si no existe)
    let ambienteResult = await pool.query('SELECT amb_id FROM ambiente LIMIT 1');
    let ambienteId;
    
    if (ambienteResult.rows.length === 0) {
      // Crear ambiente por defecto
      const sedeResult = await pool.query('SELECT sede_id FROM sede LIMIT 1');
      let sedeId;
      
      if (sedeResult.rows.length === 0) {
        // Crear sede por defecto
        sedeId = 1;
        await pool.query(
          'INSERT INTO sede (sede_id, sede_nombre) VALUES ($1, $2) ON CONFLICT DO NOTHING',
          [sedeId, 'Sede Principal']
        );
      } else {
        sedeId = sedeResult.rows[0].sede_id;
      }
      
      ambienteId = 1;
      await pool.query(
        'INSERT INTO ambiente (amb_id, amb_nombre, SEDE_sede_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING',
        [ambienteId, 'Ambiente General', sedeId]
      );
    } else {
      ambienteId = ambienteResult.rows[0].amb_id;
    }
    
    // Crear asignaciones para cada bien
    for (const bienId of bienesIds) {
      await pool.query(`
        INSERT INTO asignacion (
          ELEMENTO_elem_placa, AMBIENTE_amb_id, 
          PERSONA_pers_documento, asig_fecha_ini, disponible
        )
        VALUES ($1, $2, $3, NOW(), 0)
      `, [bienId, ambienteId, cuentadanteId]);
    }
    
    res.status(201).json({ success: true });
  } catch (error) {
    console.error('Error al crear asignación:', error);
    res.status(500).json({ error: 'Error al crear asignación' });
  }
});

// POST - Desasignar bien
app.post('/api/bienes/:id/desasignar', async (req, res) => {
  const { id } = req.params;
  
  try {
    await pool.query(`
      UPDATE asignacion 
      SET disponible = 1 
      WHERE ELEMENTO_elem_placa = $1
    `, [id]);
    
    res.json({ success: true });
  } catch (error) {
    console.error('Error al desasignar bien:', error);
    res.status(500).json({ error: 'Error al desasignar bien' });
  }
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
});
