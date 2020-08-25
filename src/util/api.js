import axios from 'axios'

// This will tell React to use localhost in development
const BASE_URL = process.env.REACT_APP_API_URL

export function testBackend(){
  return axios({
    method: 'get',
    url: `${BASE_URL}api/v1/`
  })
}