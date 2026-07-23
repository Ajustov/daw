import { SetURLSearchParams } from 'react-router'

// T, tiene que ser compatible con string
export function setFilterParam<T extends string>(
  nameParam: string,
  setSearchParams: SetURLSearchParams
) {
  return (value: T | null) => {
    setSearchParams(
      params => {
        if (value) {
          params.set(nameParam, value)
        } else {
          params.delete(nameParam)
        }
        params.set('pagina', '1')
        return params
      },
      { replace: true }
    )
  }
}
