import styles from './ListaEmpleos.module.css'
import { EmpleoCard } from './EmpleoCard'
export function ListaEmpleos ({ data }) {
  return (
    <>
      <div className={styles.lista}>
        {data.length === 0 && (
          <p style={{ textAlign: 'center', padding: '1rem' }}>No se encontraron empleos</p>
        )}
        {data.map(empleo => (
          <EmpleoCard key={empleo.id} empleo={empleo} />
        ))}
      </div>
    </>
  )
}
