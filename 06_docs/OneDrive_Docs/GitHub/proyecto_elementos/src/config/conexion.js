// Conexión a la base de datos PostgreSQL bd_elementos
import pkg from 'pg';
import dotenv from 'dotenv';

const { Pool } = pkg;

// Cargar variables de entorno
dotenv.config();

// Configuración del pool de conexiones
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'bd_elementos',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || '1',
  options: '-c search_path=bd_elementos,public'
});

// Evento para manejar errores de conexión
pool.on('error', (err, client) => {
  console.error('Error inesperado en el cliente de PostgreSQL', err);
  process.exit(-1);
});

// Función para verificar la conexión
const verificarConexion = async () => {
  try {
    const client = await pool.connect();
    console.log('Conexión exitosa a PostgreSQL');
    client.release();
    return true;
  } catch (error) {
    console.error('Error al conectar a PostgreSQL:', error.message);
    return false;
  }
};

export { pool, verificarConexion };
