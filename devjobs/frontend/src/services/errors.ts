export class HttpError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
    this.name = 'HttpError'
  }
}

export function validateRetry(nroReintentos: number) {
  // La fn que llama tanstack cada vez que incrementa intentos
  return function reintentar(failureCount: number, error: unknown) {
    // failureCount: el contador de tanstack lo maneja y se autoincrementa, empieza en 1
    if (nroReintentos < 1) return false
    if (
      error instanceof HttpError &&
      400 <= error.status &&
      error.status < 500
    ) {
      return false
    }
    return failureCount <= nroReintentos
  }
}
