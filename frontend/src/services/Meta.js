
export default class MetaResource {
  constructor () {
    this._url = process.env.NODE_ENV === 'production' ? '' : 'http://127.0.0.1:8000'
  }

  getData = async (url) => {
    const response = await fetch(url)
    return await response.json()
  }

  getDoctorList = async (page) => {
    let url = `${this._url}/api/v0/catalog/`
    if (+page > 1) {
      url = url + `?page=${page}`
    }
    return this.getData(url)
  }

  getDoctor = async (id) => {
    const url = `${this._url}/api/v0/catalog/${id}/`
    return await this.getData(url)
  }

  getUpdate = async () => {
    return await this.getData(`${this._url}/api/v0/catalog/upload/data/`)
  }
}
