import axios from 'axios'

// This will tell React to use localhost in development
const BASE_URL = process.env.REACT_APP_API_URL

export function testBackend(){
  return axios({
    method: 'get',
    url: `${BASE_URL}api/v1/`
  })
}

export function verifyToken(token){
  return axios({
    method: 'post',
    url: `${BASE_URL}token/verify/`,
    data: {
      token,
    }
  })
}

export function getNewTokens(refresh){
  return axios({
    method: 'post',
    url: `${BASE_URL}token/refresh/`,
    data: {
      refresh,
    }
  })
}